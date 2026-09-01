package tn.esprit.smarttask.dto.ai;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
@JsonIgnoreProperties(ignoreUnknown = true)
public class AIChatRequest {
    private String message;
    private AIChatContext context;
    private String sessionId;
}
