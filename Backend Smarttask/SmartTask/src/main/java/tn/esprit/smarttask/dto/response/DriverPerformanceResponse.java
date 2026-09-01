package tn.esprit.smarttask.dto.response;

import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class DriverPerformanceResponse {
    private long totalDeliveries;
    private long onTimeDeliveries;
    private long delayedDeliveries;
    private double successRate;
    private double averageMinutes;
    private long incidents;
}
