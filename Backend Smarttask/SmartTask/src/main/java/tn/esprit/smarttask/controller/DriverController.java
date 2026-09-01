package tn.esprit.smarttask.controller;

import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;
import tn.esprit.smarttask.dto.request.IncidentRequest;
import tn.esprit.smarttask.dto.request.LocationUpdateRequest;
import tn.esprit.smarttask.dto.request.ProofOfDeliveryRequest;
import tn.esprit.smarttask.dto.response.*;
import tn.esprit.smarttask.security.SecurityUtils;
import tn.esprit.smarttask.service.DriverService;
import tn.esprit.smarttask.service.driver.DriverProactiveAlertService;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/driver")
@RequiredArgsConstructor
@PreAuthorize("hasRole('DRIVER')")
@Tag(name = "Driver", description = "Driver / delivery endpoints")
@SecurityRequirement(name = "Bearer Authentication")
public class DriverController {

    private final DriverService driverService;
    private final DriverProactiveAlertService proactiveAlertService;

    @GetMapping("/dashboard")
    public ResponseEntity<DriverDashboardResponse> dashboard() {
        return ResponseEntity.ok(driverService.getDashboard(SecurityUtils.getCurrentUser()));
    }

    @GetMapping("/tasks")
    public ResponseEntity<List<TaskResponse>> getTasks() {
        return ResponseEntity.ok(driverService.getMyTasks(SecurityUtils.getCurrentUser()));
    }

    @GetMapping("/tasks/{id}")
    public ResponseEntity<TaskResponse> getTask(@PathVariable Long id) {
        return ResponseEntity.ok(driverService.getTask(id, SecurityUtils.getCurrentUser()));
    }

    @PatchMapping("/tasks/{id}/accept")
    public ResponseEntity<TaskResponse> accept(@PathVariable Long id) {
        return ResponseEntity.ok(driverService.acceptTask(id, SecurityUtils.getCurrentUser()));
    }

    @PatchMapping("/tasks/{id}/start")
    public ResponseEntity<TaskResponse> start(@PathVariable Long id) {
        return ResponseEntity.ok(driverService.startTask(id, SecurityUtils.getCurrentUser()));
    }

    @PatchMapping("/tasks/{id}/delivery")
    public ResponseEntity<TaskResponse> inDelivery(@PathVariable Long id) {
        return ResponseEntity.ok(driverService.markInDelivery(id, SecurityUtils.getCurrentUser()));
    }

    @PatchMapping("/tasks/{id}/complete")
    public ResponseEntity<TaskResponse> complete(@PathVariable Long id) {
        return ResponseEntity.ok(driverService.completeDelivery(id, SecurityUtils.getCurrentUser()));
    }

    @PatchMapping("/tasks/{id}/location")
    public ResponseEntity<TaskResponse> updateLocation(@PathVariable Long id,
                                                         @Valid @RequestBody LocationUpdateRequest request) {
        return ResponseEntity.ok(driverService.updateLocation(id, request.getLatitude(), request.getLongitude(),
                SecurityUtils.getCurrentUser()));
    }

    @PostMapping("/tasks/{id}/proof")
    public ResponseEntity<TaskResponse> uploadProof(@PathVariable Long id,
                                                    @Valid @RequestBody ProofOfDeliveryRequest request) {
        return ResponseEntity.ok(driverService.uploadProofOfDelivery(id, request, SecurityUtils.getCurrentUser()));
    }

    @GetMapping("/route")
    public ResponseEntity<List<TaskResponse>> route() {
        return ResponseEntity.ok(driverService.getRouteTasks(SecurityUtils.getCurrentUser()));
    }

    @GetMapping("/route/optimized")
    public ResponseEntity<DriverRouteOptimizationResponse> optimizedRoute() {
        return ResponseEntity.ok(driverService.getOptimizedRoute(SecurityUtils.getCurrentUser()));
    }

    @PostMapping("/alerts/check")
    public ResponseEntity<Map<String, Integer>> triggerAlerts() {
        return ResponseEntity.ok(Map.of("alertsSent", proactiveAlertService.scanAndNotify()));
    }

    @PostMapping("/incidents")
    public ResponseEntity<IncidentResponse> createIncident(@Valid @RequestBody IncidentRequest request) {
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(driverService.createIncident(request, SecurityUtils.getCurrentUser()));
    }

    @GetMapping("/history")
    public ResponseEntity<List<TaskResponse>> history() {
        return ResponseEntity.ok(driverService.getHistory(SecurityUtils.getCurrentUser()));
    }

    @GetMapping("/performance")
    public ResponseEntity<DriverPerformanceResponse> performance() {
        return ResponseEntity.ok(driverService.getPerformance(SecurityUtils.getCurrentUser()));
    }
}
