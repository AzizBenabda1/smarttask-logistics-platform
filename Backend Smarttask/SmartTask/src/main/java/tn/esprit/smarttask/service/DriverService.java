package tn.esprit.smarttask.service;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import tn.esprit.smarttask.dto.request.IncidentRequest;
import tn.esprit.smarttask.dto.response.*;
import tn.esprit.smarttask.entity.*;
import tn.esprit.smarttask.exception.*;
import tn.esprit.smarttask.mapper.TaskMapper;
import tn.esprit.smarttask.repository.*;
import tn.esprit.smarttask.service.driver.DriverRouteOptimizationService;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.List;

@Service
@RequiredArgsConstructor
public class DriverService {

    private final TaskRepository taskRepository;
    private final TaskHistoryRepository taskHistoryRepository;
    private final DriverProfileRepository driverProfileRepository;
    private final IncidentRepository incidentRepository;
    private final NotificationRepository notificationRepository;
    private final TaskMapper taskMapper;
    private final NotificationHelper notificationHelper;
    private final RealTimeEventService realTimeEventService;
    private final DriverRouteOptimizationService routeOptimizationService;

    @Transactional(readOnly = true)
    public DriverRouteOptimizationResponse getOptimizedRoute(User driver) {
        return routeOptimizationService.optimizeRoute(driver);
    }

    @Transactional(readOnly = true)
    public DriverDashboardResponse getDashboard(User driver) {
        List<Task> myTasks = taskRepository.findByDriverId(driver.getId());
        LocalDate today = LocalDate.now();
        return DriverDashboardResponse.builder()
                .missionsToday(myTasks.stream().filter(t -> t.getScheduledDate() != null && t.getScheduledDate().equals(today)).count())
                .toAccept(myTasks.stream().filter(t -> t.getStatus() == TaskStatus.ASSIGNED).count())
                .accepted(myTasks.stream().filter(t -> t.getStatus() == TaskStatus.ACCEPTED).count())
                .inProgress(myTasks.stream().filter(t -> t.getStatus() == TaskStatus.IN_PROGRESS || t.getStatus() == TaskStatus.IN_DELIVERY).count())
                .completed(myTasks.stream().filter(t -> t.getStatus() == TaskStatus.COMPLETED).count())
                .delayed(myTasks.stream().filter(t -> t.getStatus() == TaskStatus.DELAYED).count())
                .notifications(notificationRepository.findByUserIdOrderByCreatedAtDesc(driver.getId())
                        .stream().limit(5).map(taskMapper::toNotificationResponse).toList())
                .build();
    }

    @Transactional(readOnly = true)
    public List<TaskResponse> getMyTasks(User driver) {
        return taskRepository.findByDriverId(driver.getId()).stream()
                .filter(t -> t.getStatus() != TaskStatus.CANCELLED)
                .map(taskMapper::toResponse).toList();
    }

    @Transactional(readOnly = true)
    public TaskResponse getTask(Long id, User driver) {
        return taskMapper.toResponse(getOwnedTask(id, driver));
    }

    @Transactional
    public TaskResponse acceptTask(Long id, User driver) {
        Task task = getOwnedTask(id, driver);
        transition(task, TaskStatus.ASSIGNED, TaskStatus.ACCEPTED, driver, "Mission acceptée");
        notificationHelper.notifyUser(task.getClient(), NotificationType.NEW_TASK,
                "Mission acceptée", "Le chauffeur a accepté votre livraison", task, Priority.MEDIUM);
        Task saved = taskRepository.save(task);
        realTimeEventService.publishTaskUpdate(saved, "Mission acceptée");
        return taskMapper.toResponse(saved);
    }

    @Transactional
    public TaskResponse startTask(Long id, User driver) {
        Task task = getOwnedTask(id, driver);
        transition(task, TaskStatus.ACCEPTED, TaskStatus.IN_PROGRESS, driver, "Livraison démarrée");
        Task saved = taskRepository.save(task);
        realTimeEventService.publishTaskUpdate(saved, "Livraison démarrée");
        return taskMapper.toResponse(saved);
    }

    @Transactional
    public TaskResponse markInDelivery(Long id, User driver) {
        Task task = getOwnedTask(id, driver);
        transition(task, TaskStatus.IN_PROGRESS, TaskStatus.IN_DELIVERY, driver, "En livraison");
        notificationHelper.notifyUser(task.getClient(), NotificationType.NEW_TASK,
                "En livraison", "Votre commande est en cours de livraison", task, Priority.MEDIUM);
        if (task.getOrder() != null) {
            task.getOrder().setStatus(OrderStatus.IN_DELIVERY);
        }
        Task saved = taskRepository.save(task);
        realTimeEventService.publishTaskUpdate(saved, "En livraison");
        return taskMapper.toResponse(saved);
    }

    @Transactional
    public TaskResponse completeDelivery(Long id, User driver) {
        Task task = getOwnedTask(id, driver);
        transition(task, TaskStatus.IN_DELIVERY, TaskStatus.COMPLETED, driver, "Livraison terminée");
        task.setDeliveredAt(LocalDateTime.now());
        if (task.getActualMinutes() == null && task.getCreatedAt() != null) {
            task.setActualMinutes((int) ChronoUnit.MINUTES.between(task.getCreatedAt(), LocalDateTime.now()));
        }
        if (task.getOrder() != null) {
            task.getOrder().setStatus(OrderStatus.DELIVERED);
        }
        DriverProfile profile = driverProfileRepository.findByUserId(driver.getId()).orElse(null);
        if (profile != null) {
            profile.setTotalDeliveries(profile.getTotalDeliveries() + 1);
            profile.setCurrentLoad(Math.max(0, profile.getCurrentLoad() - 1));
            if (profile.getCurrentLoad() == 0) profile.setStatus(DriverStatus.AVAILABLE);
            driverProfileRepository.save(profile);
        }
        notificationHelper.notifyUser(task.getClient(), NotificationType.NEW_TASK,
                "Livraison effectuée", "Votre commande a été livrée. Merci de confirmer la réception.", task, Priority.MEDIUM);
        notificationHelper.notifyManagers(NotificationType.NEW_TASK, "Livraison terminée",
                "Tâche #" + id + " livrée par " + driver.getFirstName(), task);
        Task saved = taskRepository.save(task);
        realTimeEventService.publishTaskUpdate(saved, "Livraison terminée");
        return taskMapper.toResponse(saved);
    }

    @Transactional
    public TaskResponse updateLocation(Long id, java.math.BigDecimal latitude, java.math.BigDecimal longitude, User driver) {
        Task task = getOwnedTask(id, driver);
        if (task.getStatus() != TaskStatus.IN_DELIVERY && task.getStatus() != TaskStatus.IN_PROGRESS
                && task.getStatus() != TaskStatus.ACCEPTED) {
            throw new tn.esprit.smarttask.exception.InvalidStateTransitionException(
                    "Location updates allowed only during active delivery");
        }
        task.setLatitude(latitude);
        task.setLongitude(longitude);
        Task saved = taskRepository.save(task);
        realTimeEventService.publishTaskUpdate(saved, "Position GPS mise à jour");
        return taskMapper.toResponse(saved);
    }

    @Transactional
    public TaskResponse uploadProofOfDelivery(Long id, tn.esprit.smarttask.dto.request.ProofOfDeliveryRequest request, User driver) {
        Task task = getOwnedTask(id, driver);
        if (task.getStatus() != TaskStatus.IN_DELIVERY && task.getStatus() != TaskStatus.IN_PROGRESS) {
            throw new InvalidStateTransitionException("Proof allowed only during active delivery");
        }
        task.setProofOfDeliveryImage(request.getImageBase64());
        Task saved = taskRepository.save(task);
        realTimeEventService.publishTaskUpdate(saved, "Preuve de livraison ajoutée");
        return taskMapper.toResponse(saved);
    }

    @Transactional
    public IncidentResponse createIncident(IncidentRequest request, User driver) {
        Task task = request.getTaskId() != null ? getOwnedTask(request.getTaskId(), driver) : null;
        Incident incident = Incident.builder()
                .reporter(driver).task(task)
                .type(request.getType()).description(request.getDescription())
                .priority(request.getPriority()).status(IncidentStatus.OPEN).build();
        Incident saved = incidentRepository.save(incident);
        notificationHelper.notifyManagers(NotificationType.DELIVERY_ISSUE, "Problème chauffeur", request.getDescription(), task);
        notificationHelper.notifyOperators(NotificationType.DELIVERY_ISSUE, "Problème chauffeur", request.getDescription(), task);
        return IncidentResponse.builder()
                .id(saved.getId()).type(saved.getType()).description(saved.getDescription())
                .priority(saved.getPriority()).status(saved.getStatus())
                .taskId(task != null ? task.getId() : null)
                .reporterName(driver.getFirstName() + " " + driver.getLastName())
                .createdAt(saved.getCreatedAt()).build();
    }

    @Transactional(readOnly = true)
    public List<TaskResponse> getHistory(User driver) {
        return taskRepository.findByDriverIdAndStatusIn(driver.getId(),
                List.of(TaskStatus.COMPLETED, TaskStatus.CANCELLED, TaskStatus.DELAYED))
                .stream().map(taskMapper::toResponse).toList();
    }

    @Transactional(readOnly = true)
    public DriverPerformanceResponse getPerformance(User driver) {
        List<Task> completed = taskRepository.findByDriverIdAndStatusIn(driver.getId(), List.of(TaskStatus.COMPLETED));
        long delayed = completed.stream().filter(t -> t.getDeliveredAt() != null && t.getDeliveredAt().isAfter(t.getDeadline())).count();
        long onTime = completed.size() - delayed;
        double avg = completed.stream().filter(t -> t.getActualMinutes() != null)
                .mapToInt(Task::getActualMinutes).average().orElse(0);
        long incidents = incidentRepository.findByReporterIdOrderByCreatedAtDesc(driver.getId()).size();
        return DriverPerformanceResponse.builder()
                .totalDeliveries(completed.size())
                .onTimeDeliveries(onTime)
                .delayedDeliveries(delayed)
                .successRate(completed.isEmpty() ? 0 : (onTime * 100.0 / completed.size()))
                .averageMinutes(avg)
                .incidents(incidents)
                .build();
    }

    @Transactional(readOnly = true)
    public List<TaskResponse> getRouteTasks(User driver) {
        return taskRepository.findByDriverIdAndStatusIn(driver.getId(),
                List.of(TaskStatus.ACCEPTED, TaskStatus.IN_PROGRESS, TaskStatus.IN_DELIVERY, TaskStatus.ASSIGNED))
                .stream().map(taskMapper::toResponse).toList();
    }

    private Task getOwnedTask(Long id, User driver) {
        Task task = taskRepository.findById(id).orElseThrow(() -> new TaskNotFoundException("Task not found"));
        if (task.getDriver() == null || !task.getDriver().getId().equals(driver.getId())) {
            throw new AccessDeniedResourceException("This task is not assigned to you");
        }
        return task;
    }

    private void transition(Task task, TaskStatus expected, TaskStatus next, User driver, String notes) {
        if (task.getStatus() != expected) {
            throw new InvalidStateTransitionException(
                    "Invalid transition from " + task.getStatus() + " (expected " + expected + ")");
        }
        TaskStatus old = task.getStatus();
        task.setStatus(next);
        taskHistoryRepository.save(TaskHistory.builder()
                .task(task).action("STATUS_CHANGED").oldStatus(old).newStatus(next)
                .performedBy(driver).notes(notes).build());
    }
}
