package tn.esprit.smarttask.dto.response;

import lombok.Builder;
import lombok.Getter;
import tn.esprit.smarttask.entity.OrderStatus;
import tn.esprit.smarttask.entity.Priority;
import tn.esprit.smarttask.entity.TaskStatus;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;

@Getter
@Builder
public class OrderResponse {
    private Long id;
    private Long clientId;
    private String clientName;
    private String clientPhone;
    private Long productTypeId;
    private String productTypeName;
    private String productTypeCode;
    private String products;
    private int quantity;
    private BigDecimal amount;
    private String phone;
    private String deliveryAddress;
    private LocalDate scheduledDate;
    private LocalTime scheduledTime;
    private String instructions;
    private Priority priority;
    private OrderStatus status;
    private Long taskId;
    private TaskStatus taskStatus;
    private Boolean clientConfirmed;
    private LocalDateTime createdAt;
}
