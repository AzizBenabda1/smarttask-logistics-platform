package tn.esprit.smarttask.dto.response;

import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class TimelineStep {
    private String label;
    private boolean completed;
    private boolean current;
}
