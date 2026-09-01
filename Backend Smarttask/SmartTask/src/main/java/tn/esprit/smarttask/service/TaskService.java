package tn.esprit.smarttask.service;

import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.domain.Specification;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.util.StringUtils;
import tn.esprit.smarttask.dto.request.PriorityUpdateRequest;
import tn.esprit.smarttask.dto.request.TaskRequest;
import tn.esprit.smarttask.dto.request.TaskStatusUpdateRequest;
import tn.esprit.smarttask.dto.response.PageResponse;
import tn.esprit.smarttask.dto.response.TaskHistoryResponse;
import tn.esprit.smarttask.dto.response.TaskResponse;
import tn.esprit.smarttask.entity.*;
import tn.esprit.smarttask.exception.InvalidAssignmentException;
import tn.esprit.smarttask.exception.TaskNotFoundException;
import tn.esprit.smarttask.exception.UserNotFoundException;
import tn.esprit.smarttask.mapper.TaskMapper;
import tn.esprit.smarttask.repository.*;
import tn.esprit.smarttask.service.ai.AIRecommendationService;

import jakarta.persistence.criteria.Predicate;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.List;

@Service
@RequiredArgsConstructor
public class TaskService {

    private final TaskRepository taskRepository;
    private final TaskHistoryRepository taskHistoryRepository;
    private final UserRepository userRepository;
    private final DriverProfileRepository driverProfileRepository;
    private final NotificationRepository notificationRepository;
    private final TaskMapper taskMapper;
    private final AIRecommendationService aiRecommendationService;

    @Transactional(readOnly = true)
    public PageResponse<TaskResponse> getPage(TaskStatus status, Priority priority, Long driverId, Long clientId,
                                              LocalDate date, Boolean delayedOnly, String search, Pageable pageable) {
        Specification<Task> spec = buildSpec(status, priority, driverId, clientId, date, delayedOnly, search);
        Page<Task> page = taskRepository.findAll(spec, pageable);
        return PageResponse.of(page.map(taskMapper::toResponse));
    }

    @Transactional(readOnly = true)
    public List<TaskResponse> getAll(TaskStatus status, Priority priority, Long driverId, Long clientId,
                                     LocalDate date, Boolean delayedOnly, String search) {
        Specification<Task> spec = buildSpec(status, priority, driverId, clientId, date, delayedOnly, search);
        return taskRepository.findAll(spec).stream().map(taskMapper::toResponse).toList();
    }

    @Transactional(readOnly = true)
    public TaskResponse getById(Long id) {
        return taskMapper.toResponse(findTask(id));
    }

    @Transactional(readOnly = true)
    public List<TaskHistoryResponse> getHistory(Long id) {
        findTask(id);
        return taskHistoryRepository.findByTaskIdOrderByCreatedAtAsc(id).stream()
                .map(taskMapper::toHistoryResponse).toList();
    }

    @Transactional
    public TaskResponse create(TaskRequest request, User manager) {
        User client = userRepository.findById(request.getClientId())
                .orElseThrow(() -> new UserNotFoundException("Client not found"));
        if (client.getRole() != Role.CLIENT) {
            throw new InvalidAssignmentException("Selected user is not a client");
        }
        Task task = taskMapper.buildNewTask(request, client, manager);
        Task saved = taskRepository.save(task);
        addHistory(saved, "CREATED", null, TaskStatus.PENDING, manager, "Task created");
        notifyManager(manager, NotificationType.NEW_TASK, "New task", "Task #" + saved.getId() + " created", saved);
        return taskMapper.toResponse(saved);
    }

    @Transactional
    public TaskResponse update(Long id, TaskRequest request, User manager) {
        Task task = findTask(id);
        User client = userRepository.findById(request.getClientId())
                .orElseThrow(() -> new UserNotFoundException("Client not found"));
        task.setClient(client);
        taskMapper.updateTaskFromRequest(task, request);
        Task saved = taskRepository.save(task);
        addHistory(saved, "UPDATED", task.getStatus(), task.getStatus(), manager, "Task updated");
        return taskMapper.toResponse(saved);
    }

    @Transactional
    public void delete(Long id) {
        if (!taskRepository.existsById(id)) throw new TaskNotFoundException("Task not found: " + id);
        taskRepository.deleteById(id);
    }

    @Transactional
    public TaskResponse updateStatus(Long id, TaskStatusUpdateRequest request, User manager) {
        Task task = findTask(id);
        TaskStatus old = task.getStatus();
        task.setStatus(request.getStatus());
        if (request.getStatus() == TaskStatus.DELAYED || (task.getDeadline().isBefore(LocalDateTime.now())
                && request.getStatus() != TaskStatus.COMPLETED && request.getStatus() != TaskStatus.CANCELLED)) {
            task.setStatus(TaskStatus.DELAYED);
        }
        Task saved = taskRepository.save(task);
        addHistory(saved, "STATUS_CHANGED", old, saved.getStatus(), manager, null);
        return taskMapper.toResponse(saved);
    }

    @Transactional
    public TaskResponse updatePriority(Long id, PriorityUpdateRequest request, User manager) {
        Task task = findTask(id);
        task.setPriority(request.getPriority());
        Task saved = taskRepository.save(task);
        addHistory(saved, "PRIORITY_CHANGED", saved.getStatus(), saved.getStatus(), manager, "Priority -> " + request.getPriority());
        return taskMapper.toResponse(saved);
    }

    @Transactional
    public TaskResponse assignDriver(Long taskId, Long driverId, User manager) {
        Task task = findTask(taskId);
        User driver = userRepository.findById(driverId)
                .orElseThrow(() -> new UserNotFoundException("Driver not found"));
        if (driver.getRole() != Role.DRIVER) {
            throw new InvalidAssignmentException("Selected user is not a driver");
        }
        DriverProfile profile = driverProfileRepository.findByUserId(driverId)
                .orElseGet(() -> driverProfileRepository.save(DriverProfile.builder().user(driver).build()));

        if (profile.getStatus() == DriverStatus.UNAVAILABLE || profile.getStatus() == DriverStatus.OFFLINE) {
            throw new InvalidAssignmentException("Driver is not available for assignment");
        }

        TaskStatus old = task.getStatus();
        task.setDriver(driver);
        task.setStatus(TaskStatus.ASSIGNED);
        Task saved = taskRepository.save(task);

        profile.setStatus(DriverStatus.BUSY);
        profile.setCurrentLoad(profile.getCurrentLoad() + 1);
        driverProfileRepository.save(profile);

        addHistory(saved, "ASSIGNED", old, TaskStatus.ASSIGNED, manager, "Assigned to " + driver.getFirstName());
        return taskMapper.toResponse(saved);
    }

    @Transactional
    public TaskResponse assignRecommendedDriver(Long taskId, User manager) {
        Task task = findTask(taskId);
        var recommendation = aiRecommendationService.recommendDriver(task);
        if (recommendation.getRecommendedDriverId() == null) {
            throw new InvalidAssignmentException("No suitable driver found for this task");
        }
        return assignDriver(taskId, recommendation.getRecommendedDriverId(), manager);
    }

    private Task findTask(Long id) {
        return taskRepository.findById(id).orElseThrow(() -> new TaskNotFoundException("Task not found: " + id));
    }

    private void addHistory(Task task, String action, TaskStatus oldStatus, TaskStatus newStatus, User by, String notes) {
        taskHistoryRepository.save(TaskHistory.builder()
                .task(task).action(action).oldStatus(oldStatus).newStatus(newStatus)
                .performedBy(by).notes(notes).build());
    }

    private void notifyManager(User manager, NotificationType type, String title, String message, Task task) {
        notificationRepository.save(Notification.builder()
                .user(manager).type(type).title(title).message(message)
                .priority(Priority.MEDIUM).readFlag(false).relatedTask(task).build());
    }

    private Specification<Task> buildSpec(TaskStatus status, Priority priority, Long driverId, Long clientId,
                                          LocalDate date, Boolean delayedOnly, String search) {
        return (root, query, cb) -> {
            List<Predicate> preds = new ArrayList<>();
            if (status != null) preds.add(cb.equal(root.get("status"), status));
            if (priority != null) preds.add(cb.equal(root.get("priority"), priority));
            if (driverId != null) preds.add(cb.equal(root.get("driver").get("id"), driverId));
            if (clientId != null) preds.add(cb.equal(root.get("client").get("id"), clientId));
            if (date != null) preds.add(cb.equal(root.get("scheduledDate"), date));
            if (Boolean.TRUE.equals(delayedOnly)) {
                preds.add(cb.lessThan(root.get("deadline"), LocalDateTime.now()));
                preds.add(cb.not(root.get("status").in(TaskStatus.COMPLETED, TaskStatus.CANCELLED)));
            }
            if (StringUtils.hasText(search)) {
                String p = "%" + search.toLowerCase() + "%";
                preds.add(cb.or(
                        cb.like(cb.lower(root.get("title")), p),
                        cb.like(cb.lower(root.get("deliveryAddress")), p),
                        cb.like(cb.lower(root.get("zone")), p)
                ));
            }
            return cb.and(preds.toArray(new Predicate[0]));
        };
    }

    public static RiskLevel computeRisk(long delayMinutes, Priority priority) {
        if (delayMinutes > 120 || priority == Priority.CRITICAL) return RiskLevel.CRITICAL;
        if (delayMinutes > 60 || priority == Priority.HIGH) return RiskLevel.HIGH;
        if (delayMinutes > 30) return RiskLevel.MEDIUM;
        return RiskLevel.LOW;
    }

    public static long delayMinutes(Task task) {
        if (task.getDeadline().isAfter(LocalDateTime.now())) return 0;
        return ChronoUnit.MINUTES.between(task.getDeadline(), LocalDateTime.now());
    }
}
