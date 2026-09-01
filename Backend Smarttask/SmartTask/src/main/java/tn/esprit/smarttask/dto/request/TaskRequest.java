package tn.esprit.smarttask.dto.request;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.Getter;
import lombok.Setter;
import tn.esprit.smarttask.entity.Priority;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;

@Getter
@Setter
public class TaskRequest {

    @NotBlank @Size(max = 200)
    private String title;

    private String description;

    @NotNull
    private Long clientId;

    private Long driverId;

    @NotBlank @Size(max = 500)
    private String deliveryAddress;

    @Size(max = 100)
    private String zone;

    private LocalDate scheduledDate;
    private LocalTime scheduledTime;

    @NotNull
    private LocalDateTime deadline;

    @NotNull
    private Priority priority;

    @Size(max = 50)
    private String deliveryType;

    @Size(max = 100)
    private String weightQuantity;

    private String instructions;
    private Integer estimatedMinutes;
}
