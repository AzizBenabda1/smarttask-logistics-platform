package tn.esprit.smarttask.dto.response;

import lombok.Builder;
import lombok.Getter;

import java.util.List;

@Getter
@Builder
public class AIRecommendationResponse {
    private Long taskId;
    private Long recommendedDriverId;
    private String recommendedDriverName;
    private int scorePercent;
    private List<String> reasons;
    private boolean ruleBased;
    private String disclaimer;
}
