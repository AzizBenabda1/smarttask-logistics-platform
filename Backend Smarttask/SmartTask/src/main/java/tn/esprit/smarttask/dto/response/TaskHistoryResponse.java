package tn.esprit.smarttask.dto.response;

import lombok.Builder;
import lombok.Getter;
import tn.esprit.smarttask.entity.TaskStatus;

import java.time.LocalDateTime;

@Getter
@Builder
public class TaskHistoryResponse {
    private Long id;
    private String action;
    private TaskStatus oldStatus;
    private TaskStatus newStatus;
    private String performedByName;
    private String notes;
    private LocalDateTime createdAt;
}
