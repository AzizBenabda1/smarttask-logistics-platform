package tn.esprit.smarttask.dto.response;

import lombok.Builder;
import lombok.Getter;

import java.time.LocalDateTime;

@Getter
@Builder
public class ChatHistoryItemResponse {
    private Long id;
    private String role;
    private String content;
    private String intent;
    private LocalDateTime createdAt;
}
