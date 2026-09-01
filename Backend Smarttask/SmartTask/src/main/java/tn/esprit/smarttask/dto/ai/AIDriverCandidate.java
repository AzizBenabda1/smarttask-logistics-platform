package tn.esprit.smarttask.dto.ai;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@JsonIgnoreProperties(ignoreUnknown = true)
public class AIDriverCandidate {
    private Long id;
    private Double distanceFromClient;
    private Integer currentTasks;
    private Double performanceScore;
    private Double delayRate;
    private Boolean available;
}
