package tn.esprit.smarttask.dto.ai;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Builder;
import lombok.Getter;

import java.util.Map;

@Getter
@Builder
@JsonIgnoreProperties(ignoreUnknown = true)
public class AIChatContextItem {
    private Long id;
    private String label;
    private String status;
    private Map<String, Object> extra;
}
