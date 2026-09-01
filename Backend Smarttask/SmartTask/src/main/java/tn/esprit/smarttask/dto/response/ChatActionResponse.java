package tn.esprit.smarttask.dto.response;

import lombok.Builder;
import lombok.Getter;

import java.util.Map;

@Getter
@Builder
public class ChatActionResponse {
    private String label;
    private String actionType;
    private Map<String, Object> payload;
}
