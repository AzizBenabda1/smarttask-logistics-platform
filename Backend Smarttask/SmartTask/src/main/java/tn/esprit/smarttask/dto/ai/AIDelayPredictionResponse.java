package tn.esprit.smarttask.dto.ai;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Getter;
import lombok.Setter;
import tn.esprit.smarttask.entity.RiskLevel;

import java.util.List;

@Getter
@Setter
@JsonIgnoreProperties(ignoreUnknown = true)
public class AIDelayPredictionResponse {
    private Long taskId;
    private Double delayProbability;
    private RiskLevel riskLevel;
    private String modelVersion;
    private List<String> explanation;
}
