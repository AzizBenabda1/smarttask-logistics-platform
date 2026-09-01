package tn.esprit.smarttask.dto.response;

import lombok.Builder;
import lombok.Getter;
import tn.esprit.smarttask.entity.IncidentStatus;
import tn.esprit.smarttask.entity.IncidentType;
import tn.esprit.smarttask.entity.Priority;

import java.time.LocalDateTime;

@Getter
@Builder
public class IncidentResponse {
    private Long id;
    private IncidentType type;
    private String description;
    private Priority priority;
    private IncidentStatus status;
    private Long taskId;
    private Long orderId;
    private String reporterName;
    private LocalDateTime createdAt;
}
