package tn.esprit.smarttask.dto.response;

import lombok.Builder;
import lombok.Getter;

import java.util.List;

@Getter
@Builder
public class AnalyticsResponse {
    private long totalDeliveries;
    private long completedDeliveries;
    private long onTimeDeliveries;
    private long delayedDeliveries;
    private double averageDeliveryMinutes;
    private long incidents;
    private double averagePerformance;
    private List<ChartPoint> deliveriesByDay;
    private List<ChartPoint> deliveriesByStatus;
    private List<ChartPoint> delaysByDay;
    private List<ChartPoint> tasksByPriority;
}
