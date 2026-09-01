package tn.esprit.smarttask.dto.response;

import lombok.Builder;
import lombok.Getter;
import tn.esprit.smarttask.entity.TaskStatus;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;

@Getter
@Builder
public class DeliveryTrackingResponse {
    private Long taskId;
    private Long orderId;
    private TaskStatus currentStatus;
    private String driverName;
    private String deliveryAddress;
    private LocalDateTime estimatedArrival;
    private LocalDateTime deadline;
    private boolean clientConfirmed;
    private boolean hasProofOfDelivery;
    private BigDecimal latitude;
    private BigDecimal longitude;
    private List<TimelineStep> timeline;
}
