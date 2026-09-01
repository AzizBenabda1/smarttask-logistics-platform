package tn.esprit.smarttask.dto.ai;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Getter;
import lombok.Setter;

import java.util.List;

@Getter
@Setter
@JsonIgnoreProperties(ignoreUnknown = true)
public class AIDelayPredictionRequest {
    private Long taskId;
    private Double distanceKm;
    private Integer estimatedDuration;
    private Integer deadlineMinutes;
    private String priority;
    private Integer hour;
    private Integer dayOfWeek;
    private Integer driverCurrentTasks;
    private Double driverDelayRate;
    private String trafficLevel;
}
