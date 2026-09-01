package tn.esprit.smarttask.mapper;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;
import tn.esprit.smarttask.dto.response.OrderResponse;
import tn.esprit.smarttask.entity.Order;
import tn.esprit.smarttask.entity.Task;
import tn.esprit.smarttask.repository.TaskRepository;

@Component
@RequiredArgsConstructor
public class OrderMapper {

    private final TaskRepository taskRepository;

    public OrderResponse toResponse(Order order) {
        OrderResponse.OrderResponseBuilder builder = OrderResponse.builder()
                .id(order.getId())
                .clientId(order.getClient().getId())
                .clientName(order.getClient().getFirstName() + " " + order.getClient().getLastName())
                .clientPhone(order.getClient().getPhone())
                .productTypeId(order.getProductType() != null ? order.getProductType().getId() : null)
                .productTypeName(order.getProductType() != null ? order.getProductType().getName() : null)
                .productTypeCode(order.getProductType() != null ? order.getProductType().getCode() : null)
                .products(order.getProducts())
                .quantity(order.getQuantity())
                .amount(order.getAmount())
                .phone(order.getPhone())
                .deliveryAddress(order.getDeliveryAddress())
                .scheduledDate(order.getScheduledDate())
                .scheduledTime(order.getScheduledTime())
                .instructions(order.getInstructions())
                .priority(order.getPriority())
                .status(order.getStatus())
                .taskId(order.getTaskId())
                .createdAt(order.getCreatedAt());
        if (order.getTaskId() != null) {
            taskRepository.findById(order.getTaskId()).ifPresent(task -> enrichWithTask(builder, task));
        }
        return builder.build();
    }

    private void enrichWithTask(OrderResponse.OrderResponseBuilder builder, Task task) {
        builder.taskStatus(task.getStatus()).clientConfirmed(task.isClientConfirmed());
    }
}
