package tn.esprit.smarttask.service.automation;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import tn.esprit.smarttask.config.ExpressAutomationProperties;
import tn.esprit.smarttask.dto.ai.AIDeliveryTimePredictionResponse;
import tn.esprit.smarttask.dto.ai.AITaskPrioritizationResponse;
import tn.esprit.smarttask.dto.response.AIRecommendationResponse;
import tn.esprit.smarttask.dto.response.AutomationLogResponse;
import tn.esprit.smarttask.dto.response.ExpressChainResultResponse;
import tn.esprit.smarttask.entity.*;
import tn.esprit.smarttask.exception.AIServiceUnavailableException;
import tn.esprit.smarttask.exception.InvalidAssignmentException;
import tn.esprit.smarttask.exception.OrderNotFoundException;
import tn.esprit.smarttask.repository.*;
import tn.esprit.smarttask.service.AIService;
import tn.esprit.smarttask.service.NotificationHelper;
import tn.esprit.smarttask.service.TaskService;
import tn.esprit.smarttask.service.ai.AIRecommendationService;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.UUID;

@Service
@RequiredArgsConstructor
@Slf4j
public class ExpressDeliveryAutomationService {

    public static final String CHAIN_TYPE = "EXPRESS_DELIVERY";

    private final OrderRepository orderRepository;
    private final TaskRepository taskRepository;
    private final TaskHistoryRepository taskHistoryRepository;
    private final UserRepository userRepository;
    private final AutomationLogRepository automationLogRepository;
    private final ExpressAutomationProperties properties;
    private final AIService aiService;
    private final AIRecommendationService aiRecommendationService;
    private final TaskService taskService;
    private final NotificationHelper notificationHelper;

    @Transactional(noRollbackFor = {AIServiceUnavailableException.class, InvalidAssignmentException.class})
    public ExpressChainResultResponse execute(Long orderId) {
        String runId = UUID.randomUUID().toString();
        List<AutomationLogResponse> steps = new ArrayList<>();
        Long taskId = null;
        boolean success = true;

        try {
            Order order = orderRepository.findById(orderId)
                    .orElseThrow(() -> new OrderNotFoundException("Order not found: " + orderId));
            steps.add(logStep(runId, orderId, null, 1, "READ_ORDER", AutomationLog.StepStatus.SUCCESS,
                    "Commande #" + orderId + " — " + order.getProducts() + " — priorité " + order.getPriority()));

            if (order.getTaskId() != null) {
                return buildResult(runId, orderId, order.getTaskId(), false, steps,
                        "Commande déjà traitée (tâche #" + order.getTaskId() + ")");
            }

            if (order.getStatus() == OrderStatus.PENDING) {
                order.setStatus(OrderStatus.VERIFIED);
                orderRepository.save(order);
                steps.add(logStep(runId, orderId, null, 2, "AUTO_VERIFY", AutomationLog.StepStatus.SUCCESS,
                        "Commande auto-validée → VERIFIED"));
            } else {
                steps.add(logStep(runId, orderId, null, 2, "AUTO_VERIFY", AutomationLog.StepStatus.SKIPPED,
                        "Statut déjà " + order.getStatus()));
            }

            User manager = userRepository.findByRole(Role.MANAGER).stream().findFirst()
                    .orElse(order.getOperator());
            LocalDateTime deadline = order.getScheduledDate() != null
                    ? order.getScheduledDate().atTime(order.getScheduledTime() != null
                    ? order.getScheduledTime() : java.time.LocalTime.of(18, 0))
                    : LocalDateTime.now().plusHours(4);

            Task task = Task.builder()
                    .title("Livraison express commande #" + order.getId())
                    .description(order.getProducts())
                    .client(order.getClient())
                    .createdBy(manager)
                    .order(order)
                    .deliveryAddress(order.getDeliveryAddress())
                    .scheduledDate(order.getScheduledDate())
                    .scheduledTime(order.getScheduledTime())
                    .deadline(deadline)
                    .priority(order.getPriority())
                    .status(TaskStatus.PREPARED)
                    .instructions(order.getInstructions())
                    .weightQuantity(order.getQuantity() + " unité(s)")
                    .build();
            task = taskRepository.save(task);
            taskId = task.getId();

            order.setTaskId(taskId);
            order.setStatus(OrderStatus.READY);
            orderRepository.save(order);

            taskHistoryRepository.save(TaskHistory.builder()
                    .task(task).action("AUTO_PREPARED").newStatus(TaskStatus.PREPARED)
                    .performedBy(manager).notes("Chaîne Express Autonome — instruction 3").build());

            steps.add(logStep(runId, orderId, taskId, 3, "CREATE_TASK", AutomationLog.StepStatus.SUCCESS,
                    "Tâche #" + taskId + " créée — statut PREPARED"));

            try {
                AITaskPrioritizationResponse priority = aiService.prioritizeTask(taskId);
                if (priority.getRecommendedPriority() != null) {
                    task.setPriority(priority.getRecommendedPriority());
                    taskRepository.save(task);
                }
                steps.add(logStep(runId, orderId, taskId, 4, "AI_PRIORITIZE", AutomationLog.StepStatus.SUCCESS,
                        "Score priorité " + priority.getPriorityScore() + " → " + priority.getRecommendedPriority()));
            } catch (Exception ex) {
                steps.add(logStep(runId, orderId, taskId, 4, "AI_PRIORITIZE", AutomationLog.StepStatus.FAILED,
                        "Priorisation IA : " + ex.getMessage()));
            }

            task = taskRepository.findById(taskId).orElseThrow();
            AIRecommendationResponse rec = aiRecommendationService.recommendDriver(task);
            int score = rec.getScorePercent();
            if (rec.getRecommendedDriverId() != null && score >= properties.getMinDriverScore()) {
                try {
                    taskService.assignDriver(taskId, rec.getRecommendedDriverId(), manager);
                    steps.add(logStep(runId, orderId, taskId, 5, "AI_ASSIGN_DRIVER", AutomationLog.StepStatus.SUCCESS,
                            rec.getRecommendedDriverName() + " assigné (score " + score + "%)"));
                } catch (InvalidAssignmentException ex) {
                    success = false;
                    steps.add(logStep(runId, orderId, taskId, 5, "AI_ASSIGN_DRIVER", AutomationLog.StepStatus.SKIPPED,
                            "Assignation impossible : " + ex.getMessage()));
                    notificationHelper.notifyManagers(NotificationType.NEW_TASK, "Automation — assignation manuelle",
                            "Commande #" + orderId + " : " + ex.getMessage(), task);
                }
            } else {
                success = false;
                steps.add(logStep(runId, orderId, taskId, 5, "AI_ASSIGN_DRIVER", AutomationLog.StepStatus.SKIPPED,
                        "Score " + score + "% < seuil " + properties.getMinDriverScore() + "%"));
                notificationHelper.notifyManagers(NotificationType.NEW_TASK, "Automation — assignation manuelle",
                        "Commande #" + orderId + " : score chauffeur " + score + "%", task);
            }

            task = taskRepository.findById(taskId).orElseThrow();
            int etaMinutes = 30;
            try {
                AIDeliveryTimePredictionResponse delivery = aiService.predictDeliveryTime(taskId);
                etaMinutes = delivery.getEstimatedDeliveryTime();
            } catch (Exception ex) {
                log.warn("ETA prediction failed: {}", ex.getMessage());
            }

            notificationHelper.notifyUser(order.getClient(), NotificationType.NEW_TASK,
                    "Livraison express lancée",
                    "Commande #" + orderId + " — ETA ~" + etaMinutes + " min (IA)", task, order.getPriority());

            if (task.getDriver() != null) {
                notificationHelper.notifyUser(task.getDriver(), NotificationType.NEW_TASK,
                        "Nouvelle mission express",
                        "Mission #" + taskId + " — ETA ~" + etaMinutes + " min", task, order.getPriority());
            }

            steps.add(logStep(runId, orderId, taskId, 6, "ESTIMATE_AND_NOTIFY", AutomationLog.StepStatus.SUCCESS,
                    "ETA ~" + etaMinutes + " min — notifications envoyées"));

            String summary = success
                    ? "Chaîne terminée — commande #" + orderId + " → tâche #" + taskId
                    : "Chaîne partielle — assignation manuelle requise";
            steps.add(logStep(runId, orderId, taskId, 7, "LOG_COMPLETE", AutomationLog.StepStatus.SUCCESS, summary));

            return buildResult(runId, orderId, taskId, success, steps, summary);

        } catch (Exception ex) {
            log.error("Express chain failed for order {}: {}", orderId, ex.getMessage(), ex);
            steps.add(logStep(runId, orderId, taskId, 7, "LOG_COMPLETE", AutomationLog.StepStatus.FAILED,
                    "Échec : " + ex.getMessage()));
            return buildResult(runId, orderId, taskId, false, steps, "Échec : " + ex.getMessage());
        }
    }

    public boolean shouldAutoTrigger(Priority priority) {
        if (!properties.isEnabled()) return false;
        List<String> allowed = Arrays.stream(properties.getAutoTriggerPriorities().split(","))
                .map(String::trim).map(String::toUpperCase).toList();
        return allowed.contains(priority.name());
    }

    private AutomationLogResponse logStep(String runId, Long orderId, Long taskId, int step, String name,
                                          AutomationLog.StepStatus status, String message) {
        AutomationLog saved = automationLogRepository.save(AutomationLog.builder()
                .runId(runId).chainType(CHAIN_TYPE).orderId(orderId).taskId(taskId)
                .stepNumber(step).stepName(name).status(status).message(message).build());
        return toResponse(saved);
    }

    private ExpressChainResultResponse buildResult(String runId, Long orderId, Long taskId, boolean success,
                                                   List<AutomationLogResponse> steps, String summary) {
        return ExpressChainResultResponse.builder()
                .runId(runId).orderId(orderId).taskId(taskId)
                .success(success).summary(summary).steps(steps).build();
    }

    private AutomationLogResponse toResponse(AutomationLog log) {
        return AutomationLogResponse.builder()
                .id(log.getId()).runId(log.getRunId()).chainType(log.getChainType())
                .orderId(log.getOrderId()).taskId(log.getTaskId())
                .stepNumber(log.getStepNumber()).stepName(log.getStepName())
                .status(log.getStatus().name()).message(log.getMessage())
                .createdAt(log.getCreatedAt()).build();
    }
}
