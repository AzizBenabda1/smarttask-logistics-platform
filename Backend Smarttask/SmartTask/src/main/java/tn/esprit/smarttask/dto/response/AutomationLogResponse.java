package tn.esprit.smarttask.dto.response;

import lombok.Builder;
import lombok.Getter;

import java.time.LocalDateTime;

@Getter
@Builder
public class AutomationLogResponse {
    private Long id;
    private String runId;
    private String chainType;
    private Long orderId;
    private Long taskId;
    private int stepNumber;
    private String stepName;
    private String status;
    private String message;
    private LocalDateTime createdAt;
}
