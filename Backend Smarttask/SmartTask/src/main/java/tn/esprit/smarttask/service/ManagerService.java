package tn.esprit.smarttask.service;

import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import tn.esprit.smarttask.dto.response.*;
import tn.esprit.smarttask.entity.*;
import tn.esprit.smarttask.exception.InvalidStateTransitionException;
import tn.esprit.smarttask.exception.OrderNotFoundException;
import tn.esprit.smarttask.exception.UserNotFoundException;
import tn.esprit.smarttask.mapper.OrderMapper;
import tn.esprit.smarttask.mapper.TaskMapper;
import tn.esprit.smarttask.repository.*;
import tn.esprit.smarttask.service.ai.AIRecommendationService;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.util.ArrayList;
import java.util.List;

@Service
@RequiredArgsConstructor
public class ManagerService {

    private final TaskRepository taskRepository;
    private final OrderRepository orderRepository;
    private final UserRepository userRepository;
    private final DriverProfileRepository driverProfileRepository;
    private final NotificationRepository notificationRepository;
    private final IncidentRepository incidentRepository;
    private final TaskHistoryRepository taskHistoryRepository;
    private final TaskMapper taskMapper;
    private final OrderMapper orderMapper;
    private final NotificationHelper notificationHelper;
    private final AIRecommendationService aiRecommendationService;

    @Transactional(readOnly = true)
    public ManagerDashboardResponse getDashboard(User manager) {
        LocalDateTime now = LocalDateTime.now();
        long pending = taskRepository.countByStatus(TaskStatus.PENDING);
        long assigned = taskRepository.countByStatus(TaskStatus.ASSIGNED);
        long inProgress = taskRepository.countByStatus(TaskStatus.IN_PROGRESS);
        long inDelivery = taskRepository.countByStatus(TaskStatus.IN_DELIVERY);
        long completed = taskRepository.countByStatus(TaskStatus.COMPLETED);
        long delayed = taskRepository.countDelayedTasks(now, TaskStatus.COMPLETED, TaskStatus.CANCELLED);
        long total = taskRepository.count();
        long deliveriesToday = taskRepository.countByScheduledDate(LocalDate.now());
        long available = driverProfileRepository.countByStatus(DriverStatus.AVAILABLE);
        long busy = driverProfileRepository.countByStatus(DriverStatus.BUSY);
        long totalDrivers = userRepository.countByRole(Role.DRIVER);

        double onTimeRate = total > 0 ? (completed * 100.0 / total) : 0;
        double delayRate = total > 0 ? (delayed * 100.0 / total) : 0;

        List<NotificationResponse> alerts = notificationRepository.findByUserIdOrderByCreatedAtDesc(manager.getId())
                .stream().limit(5).map(taskMapper::toNotificationResponse).toList();

        return ManagerDashboardResponse.builder()
                .totalTasks(total)
                .pendingTasks(pending)
                .inProgressTasks(inProgress + inDelivery + assigned)
                .completedTasks(completed)
                .delayedTasks(delayed)
                .deliveriesToday(deliveriesToday)
                .availableDrivers(available)
                .busyDrivers(busy)
                .totalDrivers(totalDrivers)
                .totalOperators(userRepository.countByRole(Role.OPERATOR))
                .totalClients(userRepository.countByRole(Role.CLIENT))
                .aiRecommendations(aiRecommendationService.getRecommendationsForManager())
                .alerts(alerts)
                .tasksByStatus(taskMapper.toStatusChart(pending, assigned, inProgress, inDelivery, completed, delayed))
                .onTimeRate(onTimeRate)
                .delayRate(delayRate)
                .build();
    }

    @Transactional(readOnly = true)
    public List<DriverResponse> getDrivers() {
        return userRepository.findByRole(Role.DRIVER).stream()
                .map(u -> {
                    DriverProfile p = driverProfileRepository.findByUserId(u.getId()).orElse(null);
                    int active = taskRepository.findByDriverId(u.getId()).size();
                    return taskMapper.toDriverResponse(u, p, active);
                }).toList();
    }

    @Transactional(readOnly = true)
    public DriverResponse getDriver(Long id) {
        User u = userRepository.findById(id).orElseThrow(() -> new UserNotFoundException("Driver not found"));
        DriverProfile p = driverProfileRepository.findByUserId(id).orElse(null);
        return taskMapper.toDriverResponse(u, p, taskRepository.findByDriverId(id).size());
    }

    @Transactional(readOnly = true)
    public List<ClientResponse> getClients() {
        return userRepository.findByRole(Role.CLIENT).stream()
                .map(c -> taskMapper.toClientResponse(c, taskRepository.countByClient_Id(c.getId())))
                .toList();
    }

    @Transactional(readOnly = true)
    public List<OperatorResponse> getOperators() {
        return userRepository.findByRole(Role.OPERATOR).stream()
                .map(o -> taskMapper.toOperatorResponse(o, 0))
                .toList();
    }

    @Transactional(readOnly = true)
    public List<DelayedTaskResponse> getDelays() {
        LocalDateTime now = LocalDateTime.now();
        return taskRepository.findDelayedTasks(now, List.of(TaskStatus.COMPLETED, TaskStatus.CANCELLED))
                .stream()
                .map(t -> {
                    long dm = TaskService.delayMinutes(t);
                    return taskMapper.toDelayedResponse(t, TaskService.computeRisk(dm, t.getPriority()), dm);
                }).toList();
    }

    @Transactional(readOnly = true)
    public List<NotificationResponse> getNotifications(User manager) {
        return notificationRepository.findByUserIdOrderByCreatedAtDesc(manager.getId())
                .stream().map(taskMapper::toNotificationResponse).toList();
    }

    @Transactional
    public void markNotificationRead(Long id, User manager) {
        Notification n = notificationRepository.findById(id)
                .orElseThrow(() -> new UserNotFoundException("Notification not found"));
        if (!n.getUser().getId().equals(manager.getId())) {
            throw new org.springframework.security.access.AccessDeniedException("Not your notification");
        }
        n.setReadFlag(true);
        notificationRepository.save(n);
    }

    @Transactional(readOnly = true)
    public AnalyticsResponse getAnalytics() {
        LocalDateTime now = LocalDateTime.now();
        long total = taskRepository.count();
        long completed = taskRepository.countByStatus(TaskStatus.COMPLETED);
        long delayed = taskRepository.countDelayedTasks(now, TaskStatus.COMPLETED, TaskStatus.CANCELLED);
        long openIncidents = incidentRepository.countByStatus(IncidentStatus.OPEN)
                + incidentRepository.countByStatus(IncidentStatus.IN_PROGRESS);

        List<ChartPoint> byStatus = taskMapper.toStatusChart(
                taskRepository.countByStatus(TaskStatus.PENDING),
                taskRepository.countByStatus(TaskStatus.ASSIGNED),
                taskRepository.countByStatus(TaskStatus.IN_PROGRESS),
                taskRepository.countByStatus(TaskStatus.IN_DELIVERY),
                completed, delayed);

        List<ChartPoint> byPriority = List.of(
                ChartPoint.builder().label("LOW").value(taskRepository.countByPriority(Priority.LOW)).build(),
                ChartPoint.builder().label("MEDIUM").value(taskRepository.countByPriority(Priority.MEDIUM)).build(),
                ChartPoint.builder().label("HIGH").value(taskRepository.countByPriority(Priority.HIGH)).build(),
                ChartPoint.builder().label("CRITICAL").value(taskRepository.countByPriority(Priority.CRITICAL)).build()
        );

        Pageable last7 = PageRequest.of(0, 7, Sort.by(Sort.Direction.DESC, "scheduledDate"));
        List<ChartPoint> deliveriesByDay = toChartPoints(
                taskRepository.countByScheduledDateGrouped(TaskStatus.COMPLETED, last7));
        List<ChartPoint> delaysByDay = toChartPoints(
                taskRepository.countDelayedByDay(TaskStatus.DELAYED, last7));

        return AnalyticsResponse.builder()
                .totalDeliveries(total)
                .completedDeliveries(completed)
                .onTimeDeliveries(Math.max(0, completed - taskRepository.countByStatus(TaskStatus.DELAYED)))
                .delayedDeliveries(taskRepository.countByStatus(TaskStatus.DELAYED))
                .averageDeliveryMinutes(taskRepository.avgActualMinutesByStatus(TaskStatus.COMPLETED))
                .incidents(openIncidents)
                .averagePerformance(taskRepository.avgDriverPerformance())
                .deliveriesByDay(deliveriesByDay)
                .deliveriesByStatus(byStatus)
                .delaysByDay(delaysByDay)
                .tasksByPriority(byPriority)
                .build();
    }

    private List<ChartPoint> toChartPoints(List<Object[]> rows) {
        List<ChartPoint> points = new ArrayList<>();
        for (Object[] row : rows) {
            points.add(ChartPoint.builder()
                    .label(row[0] != null ? row[0].toString() : "?")
                    .value(((Number) row[1]).longValue())
                    .build());
        }
        return points;
    }

    @Transactional(readOnly = true)
    public List<OrderResponse> getVerifiedOrdersPendingPrepare() {
        return orderRepository.findByStatusAndTaskIdIsNullOrderByCreatedAtDesc(OrderStatus.VERIFIED).stream()
                .map(orderMapper::toResponse).toList();
    }

    @Transactional
    public TaskResponse prepareTask(Long orderId, User manager) {
        Order order = orderRepository.findById(orderId)
                .orElseThrow(() -> new OrderNotFoundException("Order not found: " + orderId));
        if (order.getStatus() != OrderStatus.VERIFIED && order.getStatus() != OrderStatus.PREPARING) {
            throw new InvalidStateTransitionException("Order must be verified before preparation");
        }
        if (order.getTaskId() != null) {
            throw new InvalidStateTransitionException("Task already created for this order");
        }

        LocalDateTime deadline = order.getScheduledDate() != null
                ? order.getScheduledDate().atTime(order.getScheduledTime() != null ? order.getScheduledTime() : LocalTime.of(18, 0))
                : LocalDateTime.now().plusDays(1);

        Task task = Task.builder()
                .title("Livraison commande #" + order.getId())
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
        Task saved = taskRepository.save(task);
        order.setTaskId(saved.getId());
        order.setStatus(OrderStatus.READY);
        orderRepository.save(order);

        taskHistoryRepository.save(TaskHistory.builder()
                .task(saved).action("PREPARED").newStatus(TaskStatus.PREPARED)
                .performedBy(manager).notes("Task prepared from order #" + orderId).build());

        notificationHelper.notifyUser(order.getClient(), NotificationType.NEW_TASK, "Commande prête",
                "Votre commande #" + orderId + " est prête pour affectation chauffeur", saved, Priority.MEDIUM);
        return taskMapper.toResponse(saved);
    }

    @Transactional(readOnly = true)
    public String exportAnalyticsCsv() {
        AnalyticsResponse analytics = getAnalytics();
        StringBuilder csv = new StringBuilder();
        csv.append("Indicateur,Valeur\n");
        csv.append("Total livraisons,").append(analytics.getTotalDeliveries()).append('\n');
        csv.append("Terminees,").append(analytics.getCompletedDeliveries()).append('\n');
        csv.append("A l'heure,").append(analytics.getOnTimeDeliveries()).append('\n');
        csv.append("Retardees,").append(analytics.getDelayedDeliveries()).append('\n');
        csv.append("Duree moyenne (min),").append(analytics.getAverageDeliveryMinutes()).append('\n');
        csv.append("Incidents ouverts,").append(analytics.getIncidents()).append('\n');
        csv.append("Performance moyenne,").append(analytics.getAveragePerformance()).append('\n');
        csv.append("\nLivraisons par jour\nJour,Nombre\n");
        analytics.getDeliveriesByDay().forEach(p -> csv.append(p.getLabel()).append(',').append(p.getValue()).append('\n'));
        csv.append("\nPar priorite\nPriorite,Nombre\n");
        analytics.getTasksByPriority().forEach(p -> csv.append(p.getLabel()).append(',').append(p.getValue()).append('\n'));
        return csv.toString();
    }
}
