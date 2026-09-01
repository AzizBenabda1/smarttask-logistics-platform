package tn.esprit.smarttask.dto.ai;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@JsonIgnoreProperties(ignoreUnknown = true)
public class AIRouteStopResult {
    private int order;
    private Long taskId;
    private String title;
    private String zone;
    private String deliveryAddress;
    private String priority;
    private int estimatedMinutes;
    private String urgencyLabel;
}
