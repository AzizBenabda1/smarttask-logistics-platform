package tn.esprit.smarttask.dto.ai;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Builder;
import lombok.Getter;

import java.util.List;
import java.util.Map;

@Getter
@Builder
@JsonIgnoreProperties(ignoreUnknown = true)
public class AIChatContext {
    private String role;
    private String userName;
    private Map<String, Object> stats;
    private List<AIChatContextItem> tasks;
    private List<AIChatContextItem> orders;
    private List<AIChatContextItem> drivers;
}
