package tn.esprit.smarttask.dto.ai;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Getter;
import lombok.Setter;
import tn.esprit.smarttask.entity.Priority;

@Getter
@Setter
@JsonIgnoreProperties(ignoreUnknown = true)
public class AITaskPrioritizationResponse {
    private Long taskId;
    private Integer priorityScore;
    private Priority recommendedPriority;
    private String reason;
    private String scoringMethod;
}
