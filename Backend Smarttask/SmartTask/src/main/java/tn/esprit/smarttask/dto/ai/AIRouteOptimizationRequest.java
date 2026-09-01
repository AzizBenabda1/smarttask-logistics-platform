package tn.esprit.smarttask.dto.ai;

import lombok.Getter;
import lombok.Setter;

import java.util.List;

@Getter
@Setter
public class AIRouteOptimizationRequest {
    private Long driverId;
    private List<AIRouteMissionStop> missions;
}
