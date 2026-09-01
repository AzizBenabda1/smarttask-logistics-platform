package tn.esprit.smarttask.dto.request;

import jakarta.validation.constraints.NotNull;
import lombok.Getter;
import lombok.Setter;
import tn.esprit.smarttask.entity.TaskStatus;

@Getter
@Setter
public class TaskStatusUpdateRequest {
    @NotNull
    private TaskStatus status;
}
