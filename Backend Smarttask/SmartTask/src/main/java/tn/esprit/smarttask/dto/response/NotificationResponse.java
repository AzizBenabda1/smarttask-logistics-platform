package tn.esprit.smarttask.dto.response;

import lombok.Builder;
import lombok.Getter;
import tn.esprit.smarttask.entity.Priority;

import java.time.LocalDateTime;

@Getter
@Builder
public class NotificationResponse {
    private Long id;
    private String type;
    private String title;
    private String message;
    private Priority priority;
    private boolean read;
    private Long relatedTaskId;
    private LocalDateTime createdAt;
}
