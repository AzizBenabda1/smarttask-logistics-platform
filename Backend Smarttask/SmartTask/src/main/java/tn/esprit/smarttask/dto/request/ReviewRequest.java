package tn.esprit.smarttask.dto.request;

import jakarta.validation.constraints.*;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class ReviewRequest {

    @NotNull
    private Long taskId;

    @Min(1)
    @Max(5)
    private int rating;

    private String comment;
}
