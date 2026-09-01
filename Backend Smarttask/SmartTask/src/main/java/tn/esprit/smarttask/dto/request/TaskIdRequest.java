package tn.esprit.smarttask.dto.request;

import jakarta.validation.constraints.NotNull;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class TaskIdRequest {
    @NotNull
    private Long taskId;
}
