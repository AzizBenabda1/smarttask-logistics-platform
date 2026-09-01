package tn.esprit.smarttask.dto.response;

import lombok.Builder;
import lombok.Getter;

import java.util.List;

@Getter
@Builder
public class ExpressChainResultResponse {
    private String runId;
    private Long orderId;
    private Long taskId;
    private boolean success;
    private String summary;
    private List<AutomationLogResponse> steps;
}
