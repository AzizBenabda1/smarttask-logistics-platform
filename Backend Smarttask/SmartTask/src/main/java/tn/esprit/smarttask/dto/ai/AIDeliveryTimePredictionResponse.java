package tn.esprit.smarttask.dto.ai;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Getter;
import lombok.Setter;

import java.util.List;

@Getter
@Setter
@JsonIgnoreProperties(ignoreUnknown = true)
public class AIDeliveryTimePredictionResponse {
    private Long taskId;
    private Integer estimatedDeliveryTime;
    private String unit;
    private String modelVersion;
    private List<String> explanation;
}
