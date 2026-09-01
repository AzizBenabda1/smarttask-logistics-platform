package tn.esprit.smarttask.dto.response;

import lombok.Builder;
import lombok.Getter;

import java.util.List;

@Getter
@Builder
public class OperatorDashboardResponse {
    private long ordersToday;
    private long pendingOrders;
    private long verifiedOrders;
    private long readyOrders;
    private long tasksToPrepare;
    private long tasksInProgress;
    private long tasksCompleted;
    private long openIncidents;
    private long deliveriesInProgress;
    private List<NotificationResponse> alerts;
}
