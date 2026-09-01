package tn.esprit.smarttask.dto.response;

import lombok.Builder;
import lombok.Getter;

import java.util.List;

@Getter
@Builder
public class ChatInitResponse {
    private String sessionId;
    private String welcomeMessage;
    private List<String> suggestions;
    private List<ChatHistoryItemResponse> history;
}
