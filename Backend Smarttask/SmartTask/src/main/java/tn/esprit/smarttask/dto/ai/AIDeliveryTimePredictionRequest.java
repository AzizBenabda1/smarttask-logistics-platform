package tn.esprit.smarttask.dto.ai;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@JsonIgnoreProperties(ignoreUnknown = true)
public class AIDeliveryTimePredictionRequest {
    private Long taskId;
    private Double distanceKm;
    private Integer estimatedDuration;
    private String priority;
    private Integer hour;
    private Integer dayOfWeek;
    private Integer driverCurrentTasks;
    private Double driverPerformance;
    private String trafficLevel;
    private String zone;
}
