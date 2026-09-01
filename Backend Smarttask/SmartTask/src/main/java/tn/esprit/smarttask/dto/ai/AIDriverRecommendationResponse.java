package tn.esprit.smarttask.dto.ai;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Getter;
import lombok.Setter;

import java.util.List;

@Getter
@Setter
@JsonIgnoreProperties(ignoreUnknown = true)
public class AIDriverRecommendationResponse {
    private Long taskId;
    private Long recommendedDriverId;
    private Integer score;
    private List<String> reasons;
    private String scoringMethod;
    private String modelVersion;
}
