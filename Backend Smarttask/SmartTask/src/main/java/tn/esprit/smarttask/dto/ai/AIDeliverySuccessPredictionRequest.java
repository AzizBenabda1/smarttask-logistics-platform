package tn.esprit.smarttask.dto.ai;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@JsonIgnoreProperties(ignoreUnknown = true)
public class AIDeliverySuccessPredictionRequest {
    private Long taskId;
    private String referenceId;
    private Long clientId;
    private String deliveryAddress;
    private Double distanceKm;
    private Integer estimatedDuration;
    private Integer deadlineMinutes;
    private String priority;
    private Integer hour;
    private Integer dayOfWeek;
    private Double addressCompletenessScore;
    private Double clientIncidentRate;
    private Double clientFailedDeliveryRate;
    private Double productFragileScore;
    private Integer driverCurrentTasks;
    private Double driverDelayRate;
    private String trafficLevel;
}
