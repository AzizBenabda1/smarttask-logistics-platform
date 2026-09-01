package tn.esprit.smarttask.dto.response;

import lombok.Builder;
import lombok.Getter;
import tn.esprit.smarttask.entity.TaskStatus;

import java.math.BigDecimal;

@Getter
@Builder
public class TaskLiveUpdate {
    private Long taskId;
    private TaskStatus status;
    private BigDecimal latitude;
    private BigDecimal longitude;
    private boolean clientConfirmed;
    private boolean hasProofOfDelivery;
    private String message;
    private long timestamp;
}
