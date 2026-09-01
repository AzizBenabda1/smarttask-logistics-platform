package tn.esprit.smarttask.dto.response;

import lombok.Builder;
import lombok.Getter;
import tn.esprit.smarttask.dto.ai.AIDelayPredictionResponse;
import tn.esprit.smarttask.dto.ai.AIDeliveryTimePredictionResponse;
import tn.esprit.smarttask.dto.ai.AITaskPrioritizationResponse;
import tn.esprit.smarttask.entity.RiskLevel;

import java.util.List;

@Getter
@Builder
public class TaskAIAnalysisResponse {
    private Long taskId;
    private Double delayProbability;
    private RiskLevel riskLevel;
    private Integer estimatedDeliveryTimeMinutes;
    private String deliveryTimeUnit;
    private Integer priorityScore;
    private String recommendedPriority;
    private List<String> explanation;
    private String delayModelVersion;
    private String deliveryTimeModelVersion;
    private boolean aiServiceAvailable;
}
