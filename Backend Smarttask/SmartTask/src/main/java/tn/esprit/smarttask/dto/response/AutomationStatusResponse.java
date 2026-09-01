package tn.esprit.smarttask.dto.response;

import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class AutomationStatusResponse {
    private boolean expressEnabled;
    private int minDriverScore;
    private String autoTriggerPriorities;
    private String chainName;
    private int stepCount;
}
