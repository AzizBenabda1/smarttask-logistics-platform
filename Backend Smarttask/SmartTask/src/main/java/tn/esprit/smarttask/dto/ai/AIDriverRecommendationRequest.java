package tn.esprit.smarttask.dto.ai;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Getter;
import lombok.Setter;

import java.util.List;

@Getter
@Setter
@JsonIgnoreProperties(ignoreUnknown = true)
public class AIDriverRecommendationRequest {
    private Long taskId;
    private Double distanceKm;
    private String priority;
    private Integer deadlineMinutes;
    private List<AIDriverCandidate> drivers;
}
