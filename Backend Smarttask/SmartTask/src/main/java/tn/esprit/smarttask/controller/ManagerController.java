package tn.esprit.smarttask.controller;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;
import tn.esprit.smarttask.dto.request.IncidentUpdateRequest;
import tn.esprit.smarttask.dto.response.*;
import tn.esprit.smarttask.entity.IncidentStatus;
import tn.esprit.smarttask.entity.Task;
import tn.esprit.smarttask.entity.User;
import tn.esprit.smarttask.repository.TaskRepository;
import tn.esprit.smarttask.security.SecurityUtils;
import tn.esprit.smarttask.service.IncidentService;
import tn.esprit.smarttask.service.ManagerService;
import tn.esprit.smarttask.service.ai.AIRecommendationService;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/manager")
@RequiredArgsConstructor
@PreAuthorize("hasRole('MANAGER')")
@Tag(name = "Manager", description = "Manager / Logistics supervisor endpoints")
@SecurityRequirement(name = "Bearer Authentication")
public class ManagerController {

    private final ManagerService managerService;
    private final IncidentService incidentService;
    private final AIRecommendationService aiRecommendationService;
    private final TaskRepository taskRepository;

    @GetMapping("/dashboard")
    @Operation(summary = "Manager dashboard KPIs and alerts")
    public ResponseEntity<ManagerDashboardResponse> getDashboard() {
        User manager = SecurityUtils.getCurrentUser();
        return ResponseEntity.ok(managerService.getDashboard(manager));
    }

    @GetMapping("/drivers")
    public ResponseEntity<List<DriverResponse>> getDrivers() {
        return ResponseEntity.ok(managerService.getDrivers());
    }

    @GetMapping("/drivers/{id}")
    public ResponseEntity<DriverResponse> getDriver(@PathVariable Long id) {
        return ResponseEntity.ok(managerService.getDriver(id));
    }

    @GetMapping("/operators")
    public ResponseEntity<List<OperatorResponse>> getOperators() {
        return ResponseEntity.ok(managerService.getOperators());
    }

    @GetMapping("/clients")
    public ResponseEntity<List<ClientResponse>> getClients() {
        return ResponseEntity.ok(managerService.getClients());
    }

    @GetMapping("/delays")
    public ResponseEntity<List<DelayedTaskResponse>> getDelays() {
        return ResponseEntity.ok(managerService.getDelays());
    }

    @GetMapping("/notifications")
    public ResponseEntity<List<NotificationResponse>> getNotifications() {
        return ResponseEntity.ok(managerService.getNotifications(SecurityUtils.getCurrentUser()));
    }

    @PatchMapping("/notifications/{id}/read")
    public ResponseEntity<Map<String, String>> markRead(@PathVariable Long id) {
        managerService.markNotificationRead(id, SecurityUtils.getCurrentUser());
        return ResponseEntity.ok(Map.of("message", "Notification marked as read"));
    }

    @GetMapping("/analytics")
    public ResponseEntity<AnalyticsResponse> getAnalytics() {
        return ResponseEntity.ok(managerService.getAnalytics());
    }

    @GetMapping("/analytics/export")
    public ResponseEntity<String> exportAnalytics() {
        return ResponseEntity.ok()
                .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=smarttask-analytics.csv")
                .contentType(MediaType.parseMediaType("text/csv"))
                .body(managerService.exportAnalyticsCsv());
    }

    @GetMapping("/ai/recommendations")
    public ResponseEntity<List<AIRecommendationResponse>> getAiRecommendations() {
        return ResponseEntity.ok(aiRecommendationService.getRecommendationsForManager());
    }

    @GetMapping("/ai/recommend-driver/{taskId}")
    public ResponseEntity<AIRecommendationResponse> recommendDriver(@PathVariable Long taskId) {
        Task task = taskRepository.findById(taskId)
                .orElseThrow(() -> new tn.esprit.smarttask.exception.TaskNotFoundException("Task not found"));
        return ResponseEntity.ok(aiRecommendationService.recommendDriver(task));
    }

    @GetMapping("/incidents")
    public ResponseEntity<PageResponse<IncidentResponse>> getIncidents(
            @RequestParam(required = false) IncidentStatus status,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "15") int size) {
        Pageable pageable = PageRequest.of(page, size, Sort.by(Sort.Direction.DESC, "createdAt"));
        return ResponseEntity.ok(incidentService.getIncidents(status, pageable));
    }

    @PatchMapping("/incidents/{id}")
    public ResponseEntity<IncidentResponse> updateIncident(@PathVariable Long id,
                                                             @Valid @RequestBody IncidentUpdateRequest request) {
        return ResponseEntity.ok(incidentService.updateStatus(id, request, SecurityUtils.getCurrentUser()));
    }
}
