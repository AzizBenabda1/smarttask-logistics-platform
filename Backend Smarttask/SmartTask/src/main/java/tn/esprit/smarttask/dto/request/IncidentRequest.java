package tn.esprit.smarttask.dto.request;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Getter;
import lombok.Setter;
import tn.esprit.smarttask.entity.IncidentType;
import tn.esprit.smarttask.entity.Priority;

@Getter
@Setter
public class IncidentRequest {

    private Long taskId;
    private Long orderId;

    @NotNull
    private IncidentType type;

    @NotBlank
    private String description;

    @NotNull
    private Priority priority;
}
