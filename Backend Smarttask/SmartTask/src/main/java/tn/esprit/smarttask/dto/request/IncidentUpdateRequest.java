package tn.esprit.smarttask.dto.request;

import jakarta.validation.constraints.NotNull;
import lombok.Getter;
import lombok.Setter;
import tn.esprit.smarttask.entity.IncidentStatus;

@Getter
@Setter
public class IncidentUpdateRequest {
    @NotNull
    private IncidentStatus status;
    private String resolutionNote;
}
