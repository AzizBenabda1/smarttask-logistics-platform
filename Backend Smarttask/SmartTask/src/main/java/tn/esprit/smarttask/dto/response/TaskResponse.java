package tn.esprit.smarttask.dto.response;

import lombok.Builder;
import lombok.Getter;
import tn.esprit.smarttask.entity.Priority;
import tn.esprit.smarttask.entity.TaskStatus;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;

@Getter
@Builder
public class TaskResponse {
    private Long id;
    private String title;
    private String description;
    private Long clientId;
    private String clientName;
    private Long driverId;
    private String driverName;
    private String deliveryAddress;
    private String zone;
    private LocalDate scheduledDate;
    private LocalTime scheduledTime;
    private LocalDateTime deadline;
    private Priority priority;
    private TaskStatus status;
    private String deliveryType;
    private String weightQuantity;
    private String instructions;
    private Integer estimatedMinutes;
    private Integer actualMinutes;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
    private boolean delayed;
    private Long orderId;
    private boolean clientConfirmed;
    private boolean hasProofOfDelivery;
    private String clientPhone;
    private String products;
    private LocalDateTime deliveredAt;
    private BigDecimal latitude;
    private BigDecimal longitude;
}
