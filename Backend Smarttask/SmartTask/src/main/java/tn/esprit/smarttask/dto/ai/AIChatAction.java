package tn.esprit.smarttask.dto.ai;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Getter;

import java.util.Map;

@Getter
@JsonIgnoreProperties(ignoreUnknown = true)
public class AIChatAction {
    private String label;
    private String actionType;
    private Map<String, Object> payload;
}
