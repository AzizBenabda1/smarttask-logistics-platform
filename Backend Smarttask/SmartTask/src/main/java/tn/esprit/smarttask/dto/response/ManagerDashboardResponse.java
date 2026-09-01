package tn.esprit.smarttask.dto.response;

import lombok.Builder;
import lombok.Getter;
import tn.esprit.smarttask.entity.Priority;
import tn.esprit.smarttask.entity.RiskLevel;
import tn.esprit.smarttask.entity.TaskStatus;

import java.time.LocalDateTime;
import java.util.List;

@Getter
@Builder
public class ManagerDashboardResponse {
    private long totalTasks;
    private long pendingTasks;
    private long inProgressTasks;
    private long completedTasks;
    private long delayedTasks;
    private long deliveriesToday;
    private long availableDrivers;
    private long busyDrivers;
    private long totalDrivers;
    private long totalOperators;
    private long totalClients;
    private List<AIRecommendationResponse> aiRecommendations;
    private List<NotificationResponse> alerts;
    private List<ChartPoint> tasksByStatus;
    private double onTimeRate;
    private double delayRate;
}
