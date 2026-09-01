package tn.esprit.smarttask.dto.ai;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Getter;
import lombok.Setter;

import java.util.List;

@Getter
@Setter
@JsonIgnoreProperties(ignoreUnknown = true)
public class AIAnomalyDetectionResponse {
    private Boolean anomaly;
    private Double score;
    private String reason;
    private List<String> explanation;
}
