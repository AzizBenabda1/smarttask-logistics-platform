package tn.esprit.smarttask.dto.response;

import lombok.Builder;
import lombok.Getter;

import java.util.List;

@Getter
@Builder
public class DriverRouteOptimizationResponse {
    private Long driverId;
    private List<DriverRouteStopResponse> stops;
    private int manualTotalMinutes;
    private int optimizedTotalMinutes;
    private int estimatedTimeSavedMinutes;
    private boolean aiPowered;
    private String summary;
}
