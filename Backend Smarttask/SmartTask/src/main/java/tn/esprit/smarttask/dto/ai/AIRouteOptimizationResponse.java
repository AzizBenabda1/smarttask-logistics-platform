package tn.esprit.smarttask.dto.ai;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Getter;
import lombok.Setter;

import java.util.List;

@Getter
@Setter
@JsonIgnoreProperties(ignoreUnknown = true)
public class AIRouteOptimizationResponse {
    private Long driverId;
    private List<AIRouteStopResult> stops;
    private int manualTotalMinutes;
    private int optimizedTotalMinutes;
    private int estimatedTimeSavedMinutes;
    private String scoringMethod;
    private String summary;
}
