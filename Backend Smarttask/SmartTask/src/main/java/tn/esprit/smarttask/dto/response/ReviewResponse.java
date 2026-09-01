package tn.esprit.smarttask.dto.response;

import lombok.Builder;
import lombok.Getter;

import java.time.LocalDateTime;

@Getter
@Builder
public class ReviewResponse {
    private Long id;
    private Long taskId;
    private int rating;
    private String comment;
    private LocalDateTime createdAt;
}
