package tn.esprit.smarttask.dto.ai;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Getter;
import lombok.Setter;
import tn.esprit.smarttask.entity.RiskLevel;

import java.util.List;

@Getter
@Setter
@JsonIgnoreProperties(ignoreUnknown = true)
public class AIDeliverySuccessPredictionResponse {
    private Long taskId;
    private String referenceId;
    private Double successProbability;
    private RiskLevel riskLevel;
    private List<String> factors;
    private List<String> suggestedActions;
    private String modelVersion;
    private List<String> explanation;
    private Boolean ruleBased;
}
