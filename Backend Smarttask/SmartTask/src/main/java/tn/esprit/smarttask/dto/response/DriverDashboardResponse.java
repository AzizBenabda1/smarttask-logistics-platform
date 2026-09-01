package tn.esprit.smarttask.dto.response;

import lombok.Builder;
import lombok.Getter;

import java.util.List;

@Getter
@Builder
public class DriverDashboardResponse {
    private long missionsToday;
    private long toAccept;
    private long accepted;
    private long inProgress;
    private long completed;
    private long delayed;
    private List<NotificationResponse> notifications;
}
