package tn.esprit.smarttask.dto.ai;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@JsonIgnoreProperties(ignoreUnknown = true)
public class AITaskPrioritizationRequest {
    private Long taskId;
    private Integer deadlineMinutes;
    private String priority;
    private Double delayProbability;
    private Double distanceKm;
    private Integer estimatedDuration;
    private Integer driverCurrentTasks;
}
