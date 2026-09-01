package tn.esprit.smarttask.dto.response;

import lombok.Builder;
import lombok.Getter;

import java.util.List;

@Getter
@Builder
public class ClientDashboardResponse {
    private long activeOrders;
    private long deliveredOrders;
    private long upcomingDeliveries;
    private OrderResponse lastOrder;
    private List<NotificationResponse> notifications;
}
