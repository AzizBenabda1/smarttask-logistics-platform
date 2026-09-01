package tn.esprit.smarttask.dto.ai;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.util.List;

@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonIgnoreProperties(ignoreUnknown = true)
public class AIChatResponse {
    private String reply;
    private String intent;
    private double confidence;
    private List<String> sources;
    private List<AIChatAction> actions;
    private List<String> suggestions;
    private boolean proactive;
}
