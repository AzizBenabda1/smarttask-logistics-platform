package tn.esprit.smarttask.dto.response;

import lombok.Builder;
import lombok.Getter;
import tn.esprit.smarttask.entity.Priority;

@Getter
@Builder
public class DriverRouteStopResponse {
    private int order;
    private Long taskId;
    private String title;
    private String zone;
    private String deliveryAddress;
    private Priority priority;
    private int estimatedMinutes;
    private String urgencyLabel;
}
