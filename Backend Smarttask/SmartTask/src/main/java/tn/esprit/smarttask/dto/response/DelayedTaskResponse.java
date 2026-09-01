package tn.esprit.smarttask.dto.response;

import lombok.Builder;
import lombok.Getter;
import tn.esprit.smarttask.entity.Priority;
import tn.esprit.smarttask.entity.RiskLevel;
import tn.esprit.smarttask.entity.TaskStatus;

import java.time.LocalDateTime;

@Getter
@Builder
public class DelayedTaskResponse {
    private Long taskId;
    private String title;
    private String driverName;
    private LocalDateTime deadline;
    private long delayMinutes;
    private RiskLevel riskLevel;
    private TaskStatus status;
    private Priority priority;
}
