package tn.esprit.smarttask.dto.response;

import lombok.Builder;
import lombok.Getter;
import tn.esprit.smarttask.entity.DriverStatus;

import java.math.BigDecimal;

@Getter
@Builder
public class DriverResponse {
    private Long id;
    private String firstName;
    private String lastName;
    private String email;
    private String phone;
    private DriverStatus status;
    private String zone;
    private int currentLoad;
    private int totalDeliveries;
    private int activeTasks;
    private BigDecimal performanceScore;
}
