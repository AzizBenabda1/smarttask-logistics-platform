package tn.esprit.smarttask.dto.response;

import lombok.Builder;
import lombok.Getter;

import java.time.LocalDateTime;
import java.util.List;

@Getter
@Builder
public class ChatReplyResponse {
    private String reply;
    private String intent;
    private double confidence;
    private List<String> sources;
    private List<ChatActionResponse> actions;
    private List<String> suggestions;
    private boolean proactive;
    private String sessionId;
    private LocalDateTime timestamp;
}
