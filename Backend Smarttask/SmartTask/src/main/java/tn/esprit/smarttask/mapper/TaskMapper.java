package tn.esprit.smarttask.mapper;

import org.springframework.stereotype.Component;
import tn.esprit.smarttask.dto.request.TaskRequest;
import tn.esprit.smarttask.dto.response.*;
import tn.esprit.smarttask.entity.*;

import java.time.LocalDateTime;
import java.util.List;

@Component
public class TaskMapper {

    public TaskResponse toResponse(Task task) {
        boolean delayed = task.getStatus() != TaskStatus.COMPLETED
                && task.getStatus() != TaskStatus.CANCELLED
                && task.getDeadline().isBefore(LocalDateTime.now());

        return TaskResponse.builder()
                .id(task.getId())
                .title(task.getTitle())
                .description(task.getDescription())
                .clientId(task.getClient().getId())
                .clientName(task.getClient().getFirstName() + " " + task.getClient().getLastName())
                .driverId(task.getDriver() != null ? task.getDriver().getId() : null)
                .driverName(task.getDriver() != null ? task.getDriver().getFirstName() + " " + task.getDriver().getLastName() : null)
                .deliveryAddress(task.getDeliveryAddress())
                .zone(task.getZone())
                .scheduledDate(task.getScheduledDate())
                .scheduledTime(task.getScheduledTime())
                .deadline(task.getDeadline())
                .priority(task.getPriority())
                .status(task.getStatus())
                .deliveryType(task.getDeliveryType())
                .weightQuantity(task.getWeightQuantity())
                .instructions(task.getInstructions())
                .estimatedMinutes(task.getEstimatedMinutes())
                .actualMinutes(task.getActualMinutes())
                .createdAt(task.getCreatedAt())
                .updatedAt(task.getUpdatedAt())
                .delayed(delayed)
                .orderId(task.getOrder() != null ? task.getOrder().getId() : null)
                .clientConfirmed(task.isClientConfirmed())
                .hasProofOfDelivery(task.getProofOfDeliveryImage() != null && !task.getProofOfDeliveryImage().isBlank())
                .clientPhone(task.getClient().getPhone())
                .products(task.getOrder() != null ? task.getOrder().getProducts() : null)
                .deliveredAt(task.getDeliveredAt())
                .latitude(task.getLatitude())
                .longitude(task.getLongitude())
                .build();
    }

    public TaskHistoryResponse toHistoryResponse(TaskHistory h) {
        return TaskHistoryResponse.builder()
                .id(h.getId())
                .action(h.getAction())
                .oldStatus(h.getOldStatus())
                .newStatus(h.getNewStatus())
                .performedByName(h.getPerformedBy() != null ? h.getPerformedBy().getFirstName() + " " + h.getPerformedBy().getLastName() : null)
                .notes(h.getNotes())
                .createdAt(h.getCreatedAt())
                .build();
    }

    public DriverResponse toDriverResponse(User user, DriverProfile profile, int activeTasks) {
        return DriverResponse.builder()
                .id(user.getId())
                .firstName(user.getFirstName())
                .lastName(user.getLastName())
                .email(user.getEmail())
                .phone(user.getPhone())
                .status(profile != null ? profile.getStatus() : DriverStatus.OFFLINE)
                .zone(profile != null ? profile.getZone() : null)
                .currentLoad(profile != null ? profile.getCurrentLoad() : 0)
                .totalDeliveries(profile != null ? profile.getTotalDeliveries() : 0)
                .activeTasks(activeTasks)
                .performanceScore(profile != null ? profile.getPerformanceScore() : null)
                .build();
    }

    public ClientResponse toClientResponse(User user, long deliveryCount) {
        return ClientResponse.builder()
                .id(user.getId())
                .firstName(user.getFirstName())
                .lastName(user.getLastName())
                .email(user.getEmail())
                .phone(user.getPhone())
                .deliveryCount(deliveryCount)
                .build();
    }

    public OperatorResponse toOperatorResponse(User user, long taskCount) {
        return OperatorResponse.builder()
                .id(user.getId())
                .firstName(user.getFirstName())
                .lastName(user.getLastName())
                .email(user.getEmail())
                .phone(user.getPhone())
                .active(user.isActive())
                .taskCount(taskCount)
                .build();
    }

    public NotificationResponse toNotificationResponse(Notification n) {
        return NotificationResponse.builder()
                .id(n.getId())
                .type(n.getType().name())
                .title(n.getTitle())
                .message(n.getMessage())
                .priority(n.getPriority())
                .read(n.isReadFlag())
                .relatedTaskId(n.getRelatedTask() != null ? n.getRelatedTask().getId() : null)
                .createdAt(n.getCreatedAt())
                .build();
    }

    public void updateTaskFromRequest(Task task, TaskRequest request) {
        task.setTitle(request.getTitle());
        task.setDescription(request.getDescription());
        task.setDeliveryAddress(request.getDeliveryAddress());
        task.setZone(request.getZone());
        task.setScheduledDate(request.getScheduledDate());
        task.setScheduledTime(request.getScheduledTime());
        task.setDeadline(request.getDeadline());
        task.setPriority(request.getPriority());
        task.setDeliveryType(request.getDeliveryType());
        task.setWeightQuantity(request.getWeightQuantity());
        task.setInstructions(request.getInstructions());
        task.setEstimatedMinutes(request.getEstimatedMinutes());
    }

    public Task buildNewTask(TaskRequest request, User client, User manager) {
        return Task.builder()
                .title(request.getTitle())
                .description(request.getDescription())
                .client(client)
                .createdBy(manager)
                .deliveryAddress(request.getDeliveryAddress())
                .zone(request.getZone())
                .scheduledDate(request.getScheduledDate())
                .scheduledTime(request.getScheduledTime())
                .deadline(request.getDeadline())
                .priority(request.getPriority())
                .status(TaskStatus.PENDING)
                .deliveryType(request.getDeliveryType())
                .weightQuantity(request.getWeightQuantity())
                .instructions(request.getInstructions())
                .estimatedMinutes(request.getEstimatedMinutes())
                .build();
    }

    public DelayedTaskResponse toDelayedResponse(Task task, RiskLevel risk, long delayMinutes) {
        return DelayedTaskResponse.builder()
                .taskId(task.getId())
                .title(task.getTitle())
                .driverName(task.getDriver() != null ? task.getDriver().getFirstName() + " " + task.getDriver().getLastName() : null)
                .deadline(task.getDeadline())
                .delayMinutes(delayMinutes)
                .riskLevel(risk)
                .status(task.getStatus())
                .priority(task.getPriority())
                .build();
    }

    public List<ChartPoint> toStatusChart(long pending, long assigned, long inProgress, long inDelivery, long completed, long delayed) {
        return List.of(
                ChartPoint.builder().label("PENDING").value(pending).build(),
                ChartPoint.builder().label("ASSIGNED").value(assigned).build(),
                ChartPoint.builder().label("IN_PROGRESS").value(inProgress).build(),
                ChartPoint.builder().label("IN_DELIVERY").value(inDelivery).build(),
                ChartPoint.builder().label("COMPLETED").value(completed).build(),
                ChartPoint.builder().label("DELAYED").value(delayed).build()
        );
    }
}
