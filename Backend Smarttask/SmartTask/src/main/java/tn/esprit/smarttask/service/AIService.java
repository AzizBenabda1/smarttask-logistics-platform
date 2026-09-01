package tn.esprit.smarttask.service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import tn.esprit.smarttask.client.SmartTaskAIClient;
import tn.esprit.smarttask.config.AIProperties;
import tn.esprit.smarttask.dto.ai.*;
import tn.esprit.smarttask.dto.request.OrderRequest;
import tn.esprit.smarttask.dto.response.TaskAIAnalysisResponse;
import tn.esprit.smarttask.entity.*;
import tn.esprit.smarttask.exception.AIServiceUnavailableException;
import tn.esprit.smarttask.exception.TaskNotFoundException;
import tn.esprit.smarttask.repository.DriverProfileRepository;
import tn.esprit.smarttask.repository.IncidentRepository;
import tn.esprit.smarttask.repository.OrderRepository;
import tn.esprit.smarttask.repository.ProductTypeRepository;
import tn.esprit.smarttask.repository.TaskRepository;
import tn.esprit.smarttask.repository.UserRepository;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
@RequiredArgsConstructor
@Slf4j
@Transactional(readOnly = true, noRollbackFor = AIServiceUnavailableException.class)
public class AIService {

    private final SmartTaskAIClient aiClient;
    private final AIProperties aiProperties;
    private final TaskRepository taskRepository;
    private final UserRepository userRepository;
    private final DriverProfileRepository driverProfileRepository;
    private final OrderRepository orderRepository;
    private final IncidentRepository incidentRepository;
    private final ProductTypeRepository productTypeRepository;

    public AIDelayPredictionResponse predictDelay(Long taskId) {
        Task task = findTask(taskId);
        return aiClient.predictDelay(buildDelayRequest(task));
    }

    public AIDeliveryTimePredictionResponse predictDeliveryTime(Long taskId) {
        Task task = findTask(taskId);
        return aiClient.predictDeliveryTime(buildDeliveryTimeRequest(task));
    }

    public AITaskPrioritizationResponse prioritizeTask(Long taskId) {
        Task task = findTask(taskId);
        AIDelayPredictionResponse delay = predictDelay(taskId);
        AITaskPrioritizationRequest request = new AITaskPrioritizationRequest();
        request.setTaskId(taskId);
        request.setDeadlineMinutes(minutesUntilDeadline(task));
        request.setPriority(task.getPriority().name());
        request.setDelayProbability(delay.getDelayProbability());
        request.setDistanceKm(estimateDistanceKm(task));
        request.setEstimatedDuration(estimateDuration(task));
        request.setDriverCurrentTasks(driverCurrentTasks(task.getDriver()));
        return aiClient.prioritizeTask(request);
    }

    public AIDriverRecommendationResponse recommendDriver(Long taskId) {
        Task task = findTask(taskId);
        AIDriverRecommendationRequest request = new AIDriverRecommendationRequest();
        request.setTaskId(taskId);
        request.setDistanceKm(estimateDistanceKm(task));
        request.setPriority(task.getPriority().name());
        request.setDeadlineMinutes(minutesUntilDeadline(task));
        request.setDrivers(buildDriverCandidates(task));
        return aiClient.recommendDriver(request);
    }

    public AIAnomalyDetectionResponse detectAnomaly(Long taskId) {
        Task task = findTask(taskId);
        Map<String, Object> payload = new HashMap<>();
        payload.put("taskId", taskId);
        payload.put("actualDeliveryTime", task.getActualMinutes());
        payload.put("expectedDeliveryTime", task.getEstimatedMinutes());
        payload.put("driverCurrentTasks", driverCurrentTasks(task.getDriver()));
        return aiClient.detectAnomaly(payload);
    }

    public AIDeliverySuccessPredictionResponse predictDeliverySuccess(Long taskId) {
        Task task = findTask(taskId);
        return callDeliverySuccess(buildDeliverySuccessRequest(task));
    }

    public AIDeliverySuccessPredictionResponse previewDeliverySuccess(OrderRequest orderRequest) {
        return callDeliverySuccess(buildDeliverySuccessPreview(orderRequest));
    }

    private AIDeliverySuccessPredictionResponse callDeliverySuccess(AIDeliverySuccessPredictionRequest request) {
        try {
            return aiClient.predictDeliverySuccess(request);
        } catch (AIServiceUnavailableException ex) {
            log.warn("Delivery success AI unavailable, using Java fallback: {}", ex.getMessage());
            return buildRuleBasedDeliverySuccess(request);
        }
    }

    public TaskAIAnalysisResponse analyzeTask(Long taskId) {
        AIDelayPredictionResponse delay = predictDelay(taskId);
        AIDeliveryTimePredictionResponse delivery = predictDeliveryTime(taskId);
        AITaskPrioritizationResponse priority = prioritizeTask(taskId);

        List<String> explanation = new ArrayList<>();
        if (delay.getExplanation() != null) explanation.addAll(delay.getExplanation());
        if (delivery.getExplanation() != null) {
            delivery.getExplanation().stream()
                    .filter(e -> !explanation.contains(e))
                    .forEach(explanation::add);
        }

        return TaskAIAnalysisResponse.builder()
                .taskId(taskId)
                .delayProbability(delay.getDelayProbability())
                .riskLevel(delay.getRiskLevel())
                .estimatedDeliveryTimeMinutes(delivery.getEstimatedDeliveryTime())
                .deliveryTimeUnit(delivery.getUnit())
                .priorityScore(priority.getPriorityScore())
                .recommendedPriority(priority.getRecommendedPriority() != null
                        ? priority.getRecommendedPriority().name() : null)
                .explanation(explanation)
                .delayModelVersion(delay.getModelVersion())
                .deliveryTimeModelVersion(delivery.getModelVersion())
                .aiServiceAvailable(aiProperties.isEnabled())
                .build();
    }

    public Map<String, Object> health() {
        return aiClient.health();
    }

    public Map<String, Object> modelStatus() {
        return aiClient.modelStatus();
    }

    public boolean isEnabled() {
        return aiProperties.isEnabled();
    }

    private Task findTask(Long id) {
        return taskRepository.findById(id)
                .orElseThrow(() -> new TaskNotFoundException("Task not found: " + id));
    }

    AIDelayPredictionRequest buildDelayRequest(Task task) {
        AIDelayPredictionRequest req = new AIDelayPredictionRequest();
        req.setTaskId(task.getId());
        req.setDistanceKm(estimateDistanceKm(task));
        req.setEstimatedDuration(estimateDuration(task));
        req.setDeadlineMinutes(minutesUntilDeadline(task));
        req.setPriority(task.getPriority().name());
        req.setHour(task.getDeadline().getHour());
        req.setDayOfWeek(task.getDeadline().getDayOfWeek().getValue() - 1);
        req.setDriverCurrentTasks(driverCurrentTasks(task.getDriver()));
        req.setDriverDelayRate(driverDelayRate(task.getDriver()));
        req.setTrafficLevel(trafficLevel(task.getDeadline()).name());
        return req;
    }

    AIDeliveryTimePredictionRequest buildDeliveryTimeRequest(Task task) {
        AIDeliveryTimePredictionRequest req = new AIDeliveryTimePredictionRequest();
        req.setTaskId(task.getId());
        req.setDistanceKm(estimateDistanceKm(task));
        req.setEstimatedDuration(estimateDuration(task));
        req.setPriority(task.getPriority().name());
        req.setHour(task.getDeadline().getHour());
        req.setDayOfWeek(task.getDeadline().getDayOfWeek().getValue() - 1);
        req.setDriverCurrentTasks(driverCurrentTasks(task.getDriver()));
        req.setDriverPerformance(driverPerformance(task.getDriver()));
        req.setTrafficLevel(trafficLevel(task.getDeadline()).name());
        req.setZone(task.getZone());
        return req;
    }

    AIDeliverySuccessPredictionRequest buildDeliverySuccessRequest(Task task) {
        AIDeliverySuccessPredictionRequest req = new AIDeliverySuccessPredictionRequest();
        req.setTaskId(task.getId());
        req.setClientId(task.getClient() != null ? task.getClient().getId() : null);
        req.setDeliveryAddress(task.getDeliveryAddress());
        req.setDistanceKm(estimateDistanceKm(task));
        req.setEstimatedDuration(estimateDuration(task));
        req.setDeadlineMinutes(minutesUntilDeadline(task));
        req.setPriority(task.getPriority().name());
        req.setHour(task.getDeadline().getHour());
        req.setDayOfWeek(task.getDeadline().getDayOfWeek().getValue() - 1);
        req.setAddressCompletenessScore(scoreAddress(task.getDeliveryAddress()));
        if (task.getClient() != null) {
            req.setClientIncidentRate(clientIncidentRate(task.getClient().getId()));
            req.setClientFailedDeliveryRate(clientFailedDeliveryRate(task.getClient().getId()));
        } else {
            req.setClientIncidentRate(0.05);
            req.setClientFailedDeliveryRate(0.05);
        }
        req.setProductFragileScore(productFragileScoreFromOrder(task.getOrder()));
        req.setDriverCurrentTasks(driverCurrentTasks(task.getDriver()));
        req.setDriverDelayRate(driverDelayRate(task.getDriver()));
        req.setTrafficLevel(trafficLevel(task.getDeadline()).name());
        return req;
    }

    AIDeliverySuccessPredictionRequest buildDeliverySuccessPreview(OrderRequest order) {
        AIDeliverySuccessPredictionRequest req = new AIDeliverySuccessPredictionRequest();
        req.setReferenceId("preview");
        req.setClientId(order.getClientId());
        req.setDeliveryAddress(order.getDeliveryAddress());
        int estimated = 30;
        req.setDistanceKm(Math.max(1.0, order.getDeliveryAddress().length() * 0.08));
        req.setEstimatedDuration(estimated);
        LocalDateTime deadline = resolveOrderDeadline(order);
        req.setDeadlineMinutes((int) Math.max(30,
                ChronoUnit.MINUTES.between(LocalDateTime.now(), deadline)));
        req.setPriority(order.getPriority().name());
        req.setHour(deadline.getHour());
        req.setDayOfWeek(deadline.getDayOfWeek().getValue() - 1);
        req.setAddressCompletenessScore(scoreAddress(order.getDeliveryAddress()));
        req.setClientIncidentRate(clientIncidentRate(order.getClientId()));
        req.setClientFailedDeliveryRate(clientFailedDeliveryRate(order.getClientId()));
        req.setProductFragileScore(productFragileScore(order.getProductTypeId(), order.getCustomProductType()));
        req.setDriverCurrentTasks(0);
        req.setDriverDelayRate(0.1);
        req.setTrafficLevel(trafficLevel(deadline).name());
        return req;
    }

    AIDeliverySuccessPredictionResponse buildRuleBasedDeliverySuccess(
            AIDeliverySuccessPredictionRequest req) {
        double score = 0.35 * req.getAddressCompletenessScore()
                + 0.15 * (1 - Math.min(req.getClientIncidentRate(), 0.5))
                + 0.15 * (1 - Math.min(req.getClientFailedDeliveryRate(), 0.5))
                - 0.08 * priorityScore(req.getPriority())
                - 0.07 * Math.min(req.getDriverCurrentTasks(), 5) / 5.0
                - 0.1 * req.getDriverDelayRate()
                - 0.05 * req.getProductFragileScore();
        if (req.getEstimatedDuration() >= req.getDeadlineMinutes() * 0.92) {
            score -= 0.12;
        }
        double proba = Math.max(0.05, Math.min(0.95, score));
        AIDeliverySuccessPredictionResponse res = new AIDeliverySuccessPredictionResponse();
        res.setTaskId(req.getTaskId());
        res.setReferenceId(req.getReferenceId());
        res.setSuccessProbability(proba);
        res.setRiskLevel(successRiskLevel(proba));
        res.setFactors(List.of(proba >= 0.6 ? "Conditions favorables (fallback regles)"
                : "Risque modere (fallback regles)"));
        res.setSuggestedActions(proba < 0.55
                ? List.of("Confirmer l'adresse avec le client", "Valider manuellement")
                : List.of("Poursuivre le workflow standard"));
        res.setExplanation(res.getFactors());
        res.setModelVersion("1.0.0-rules-java");
        res.setRuleBased(true);
        return res;
    }

    double scoreAddress(String address) {
        if (address == null || address.isBlank()) return 0.2;
        double score = Math.min(1.0, address.trim().length() / 45.0);
        if (address.matches(".*\\d.*")) score += 0.15;
        if (address.contains(",")) score += 0.1;
        return Math.min(1.0, score);
    }

    double clientIncidentRate(Long clientId) {
        long orders = Math.max(1, orderRepository.countByClient_Id(clientId));
        long incidents = incidentRepository.countByReporterId(clientId);
        return Math.min(0.9, incidents / (double) orders);
    }

    double clientFailedDeliveryRate(Long clientId) {
        long orders = Math.max(1, orderRepository.countByClient_Id(clientId));
        long cancelled = orderRepository.findByClientIdOrderByCreatedAtDesc(clientId).stream()
                .filter(o -> o.getStatus() == OrderStatus.CANCELLED)
                .count();
        return Math.min(0.9, cancelled / (double) orders);
    }

    double productFragileScoreFromOrder(Order order) {
        if (order == null || order.getProductType() == null) return 0.0;
        return fragileCode(order.getProductType().getCode()) ? 1.0 : 0.0;
    }

    double productFragileScore(Long productTypeId, String customProductType) {
        if (productTypeId != null) {
            return productTypeRepository.findById(productTypeId)
                    .map(pt -> fragileCode(pt.getCode()) ? 1.0 : 0.0)
                    .orElse(0.0);
        }
        if (customProductType != null) {
            String lower = customProductType.toLowerCase();
            if (lower.contains("fragile") || lower.contains("medic") || lower.contains("medical")) {
                return 1.0;
            }
        }
        return 0.0;
    }

    boolean fragileCode(String code) {
        return code != null && (code.contains("FRAGILE") || code.contains("MEDICAMENT"));
    }

    LocalDateTime resolveOrderDeadline(OrderRequest order) {
        LocalDate date = order.getScheduledDate() != null ? order.getScheduledDate() : LocalDate.now();
        LocalTime time = order.getScheduledTime() != null ? order.getScheduledTime() : LocalTime.of(18, 0);
        LocalDateTime dt = LocalDateTime.of(date, time);
        if (dt.isBefore(LocalDateTime.now())) {
            dt = LocalDateTime.now().plusHours(2);
        }
        return dt;
    }

    int priorityScore(String priority) {
        return switch (priority) {
            case "LOW" -> 0;
            case "HIGH" -> 2;
            case "CRITICAL" -> 3;
            default -> 1;
        };
    }

    RiskLevel successRiskLevel(double successProbability) {
        if (successProbability >= 0.75) return RiskLevel.LOW;
        if (successProbability >= 0.55) return RiskLevel.MEDIUM;
        if (successProbability >= 0.35) return RiskLevel.HIGH;
        return RiskLevel.CRITICAL;
    }

    List<AIDriverCandidate> buildDriverCandidates(Task task) {
        List<User> drivers = userRepository.findByRole(Role.DRIVER);
        List<AIDriverCandidate> candidates = new ArrayList<>();
        for (User driver : drivers) {
            if (!driver.isActive()) continue;
            DriverProfile profile = driverProfileRepository.findByUserId(driver.getId()).orElse(null);
            AIDriverCandidate c = new AIDriverCandidate();
            c.setId(driver.getId());
            c.setDistanceFromClient(estimateDriverDistance(task, profile));
            c.setCurrentTasks(profile != null ? profile.getCurrentLoad() : driverActiveTasks(driver.getId()));
            c.setPerformanceScore(profile != null
                    ? profile.getPerformanceScore().doubleValue() / 100.0
                    : driverPerformance(driver));
            c.setDelayRate(driverDelayRate(driver));
            c.setAvailable(profile == null || profile.getStatus() == DriverStatus.AVAILABLE);
            candidates.add(c);
        }
        return candidates;
    }

    double estimateDistanceKm(Task task) {
        if (task.getEstimatedMinutes() != null && task.getEstimatedMinutes() > 0) {
            return Math.max(1.0, task.getEstimatedMinutes() * 0.35);
        }
        return 10.0;
    }

    int estimateDuration(Task task) {
        return task.getEstimatedMinutes() != null ? task.getEstimatedMinutes() : 30;
    }

    int minutesUntilDeadline(Task task) {
        long minutes = ChronoUnit.MINUTES.between(LocalDateTime.now(), task.getDeadline());
        return (int) Math.max(5, minutes);
    }

    enum TrafficLevel { LOW, MEDIUM, HIGH }

    TrafficLevel trafficLevel(LocalDateTime deadline) {
        int hour = deadline.getHour();
        if ((hour >= 8 && hour <= 10) || (hour >= 17 && hour <= 19)) return TrafficLevel.HIGH;
        if (hour >= 11 && hour <= 16) return TrafficLevel.MEDIUM;
        return TrafficLevel.LOW;
    }

    int driverCurrentTasks(User driver) {
        if (driver == null) return 0;
        return driverActiveTasks(driver.getId());
    }

    int driverActiveTasks(Long driverId) {
        return (int) taskRepository.findByDriverIdAndStatusIn(driverId,
                List.of(TaskStatus.ASSIGNED, TaskStatus.ACCEPTED, TaskStatus.IN_PROGRESS, TaskStatus.IN_DELIVERY)).size();
    }

    double driverDelayRate(User driver) {
        if (driver == null) return 0.1;
        List<Task> completed = taskRepository.findByDriverIdAndStatusIn(driver.getId(), List.of(TaskStatus.COMPLETED));
        if (completed.isEmpty()) return 0.1;
        long delayed = completed.stream()
                .filter(t -> t.getDeliveredAt() != null && t.getDeliveredAt().isAfter(t.getDeadline()))
                .count();
        return delayed / (double) completed.size();
    }

    double driverPerformance(User driver) {
        if (driver == null) return 0.75;
        return driverProfileRepository.findByUserId(driver.getId())
                .map(p -> p.getPerformanceScore().doubleValue() / 100.0)
                .orElse(0.75);
    }

    double estimateDriverDistance(Task task, DriverProfile profile) {
        if (profile != null && task.getZone() != null && task.getZone().equalsIgnoreCase(profile.getZone())) {
            return 3.0;
        }
        return 12.0;
    }
}
