package tn.esprit.smarttask.service.driver;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import tn.esprit.smarttask.client.SmartTaskAIClient;
import tn.esprit.smarttask.config.AIProperties;
import tn.esprit.smarttask.dto.ai.*;
import tn.esprit.smarttask.dto.response.DriverRouteOptimizationResponse;
import tn.esprit.smarttask.dto.response.DriverRouteStopResponse;
import tn.esprit.smarttask.entity.*;
import tn.esprit.smarttask.exception.AIServiceUnavailableException;
import tn.esprit.smarttask.repository.TaskRepository;

import java.time.LocalDateTime;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

@Service
@RequiredArgsConstructor
@Slf4j
public class DriverRouteOptimizationService {

    private final TaskRepository taskRepository;
    private final SmartTaskAIClient aiClient;
    private final AIProperties aiProperties;

    @Transactional(readOnly = true)
    public DriverRouteOptimizationResponse optimizeRoute(User driver) {
        List<Task> missions = taskRepository.findByDriverIdAndStatusIn(driver.getId(),
                List.of(TaskStatus.ASSIGNED, TaskStatus.ACCEPTED, TaskStatus.IN_PROGRESS, TaskStatus.IN_DELIVERY));

        if (missions.isEmpty()) {
            return DriverRouteOptimizationResponse.builder()
                    .driverId(driver.getId())
                    .stops(List.of())
                    .summary("Aucune mission active à optimiser")
                    .aiPowered(false)
                    .build();
        }

        List<AIRouteMissionStop> stops = missions.stream().map(this::toMissionStop).toList();
        AIRouteOptimizationRequest request = new AIRouteOptimizationRequest();
        request.setDriverId(driver.getId());
        request.setMissions(stops);

        if (aiProperties.isEnabled()) {
            try {
                AIRouteOptimizationResponse ai = aiClient.optimizeRoute(request);
                return toResponse(ai, true);
            } catch (AIServiceUnavailableException ex) {
                log.warn("Route AI unavailable for driver {}, fallback rules", driver.getId());
            }
        }
        return ruleBasedOptimize(driver.getId(), stops);
    }

    private DriverRouteOptimizationResponse ruleBasedOptimize(Long driverId, List<AIRouteMissionStop> missions) {
        List<AIRouteMissionStop> optimized = new ArrayList<>(missions);
        optimized.sort(Comparator.comparingInt(this::scoreMission).reversed());

        int manualTotal = missions.stream().mapToInt(AIRouteMissionStop::getEstimatedMinutes).sum();
        int optimizedTotal = optimized.stream().mapToInt(AIRouteMissionStop::getEstimatedMinutes).sum();
        int saved = Math.max(0, (int) (manualTotal * 0.15));

        List<DriverRouteStopResponse> stops = new ArrayList<>();
        for (int i = 0; i < optimized.size(); i++) {
            AIRouteMissionStop m = optimized.get(i);
            stops.add(toStopResponse(i + 1, m));
        }

        return DriverRouteOptimizationResponse.builder()
                .driverId(driverId)
                .stops(stops)
                .manualTotalMinutes(manualTotal)
                .optimizedTotalMinutes(Math.max(optimizedTotal - saved, 0))
                .estimatedTimeSavedMinutes(saved)
                .aiPowered(false)
                .summary("Ordre optimisé (règles) — gain estimé " + saved + " min")
                .build();
    }

    private int scoreMission(AIRouteMissionStop m) {
        int pw = switch (Priority.valueOf(m.getPriority())) {
            case CRITICAL -> 100;
            case HIGH -> 75;
            case MEDIUM -> 50;
            case LOW -> 25;
        };
        return pw + Math.max(0, 120 - m.getDeadlineMinutes());
    }

    private AIRouteMissionStop toMissionStop(Task task) {
        AIRouteMissionStop stop = new AIRouteMissionStop();
        stop.setTaskId(task.getId());
        stop.setTitle(task.getTitle());
        stop.setZone(task.getZone());
        stop.setDeliveryAddress(task.getDeliveryAddress());
        stop.setPriority(task.getPriority().name());
        stop.setDeadlineMinutes((int) Math.max(5, ChronoUnit.MINUTES.between(LocalDateTime.now(), task.getDeadline())));
        stop.setEstimatedMinutes(task.getEstimatedMinutes() != null ? task.getEstimatedMinutes() : 30);
        return stop;
    }

    private DriverRouteOptimizationResponse toResponse(AIRouteOptimizationResponse ai, boolean aiPowered) {
        List<DriverRouteStopResponse> stops = ai.getStops().stream()
                .map(s -> DriverRouteStopResponse.builder()
                        .order(s.getOrder())
                        .taskId(s.getTaskId())
                        .title(s.getTitle())
                        .zone(s.getZone())
                        .deliveryAddress(s.getDeliveryAddress())
                        .priority(Priority.valueOf(s.getPriority()))
                        .estimatedMinutes(s.getEstimatedMinutes())
                        .urgencyLabel(s.getUrgencyLabel())
                        .build())
                .toList();

        return DriverRouteOptimizationResponse.builder()
                .driverId(ai.getDriverId())
                .stops(stops)
                .manualTotalMinutes(ai.getManualTotalMinutes())
                .optimizedTotalMinutes(ai.getOptimizedTotalMinutes())
                .estimatedTimeSavedMinutes(ai.getEstimatedTimeSavedMinutes())
                .aiPowered(aiPowered)
                .summary(ai.getSummary())
                .build();
    }

    private DriverRouteStopResponse toStopResponse(int order, AIRouteMissionStop m) {
        String urgency = Priority.valueOf(m.getPriority()) == Priority.CRITICAL || m.getDeadlineMinutes() <= 30
                ? "URGENT"
                : (m.getDeadlineMinutes() <= 60 ? "PRIORITAIRE" : "NORMAL");
        return DriverRouteStopResponse.builder()
                .order(order)
                .taskId(m.getTaskId())
                .title(m.getTitle())
                .zone(m.getZone())
                .deliveryAddress(m.getDeliveryAddress())
                .priority(Priority.valueOf(m.getPriority()))
                .estimatedMinutes(m.getEstimatedMinutes())
                .urgencyLabel(urgency)
                .build();
    }
}
