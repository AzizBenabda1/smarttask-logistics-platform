package tn.esprit.smarttask.controller;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;
import tn.esprit.smarttask.dto.request.*;
import tn.esprit.smarttask.dto.response.*;
import tn.esprit.smarttask.entity.*;
import tn.esprit.smarttask.security.SecurityUtils;
import tn.esprit.smarttask.service.ManagerService;
import tn.esprit.smarttask.service.TaskService;
import tn.esprit.smarttask.service.ai.AIRecommendationService;

import java.time.LocalDate;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/tasks")
@RequiredArgsConstructor
@PreAuthorize("hasRole('MANAGER')")
@Tag(name = "Tasks", description = "Task management for managers")
@SecurityRequirement(name = "Bearer Authentication")
public class TaskController {

    private final TaskService taskService;

    @GetMapping
    public ResponseEntity<PageResponse<TaskResponse>> getAll(
            @RequestParam(required = false) TaskStatus status,
            @RequestParam(required = false) Priority priority,
            @RequestParam(required = false) Long driverId,
            @RequestParam(required = false) Long clientId,
            @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate date,
            @RequestParam(required = false) Boolean delayed,
            @RequestParam(required = false) String search,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        Pageable pageable = org.springframework.data.domain.PageRequest.of(page, size,
                org.springframework.data.domain.Sort.by(org.springframework.data.domain.Sort.Direction.DESC, "createdAt"));
        return ResponseEntity.ok(taskService.getPage(status, priority, driverId, clientId, date, delayed, search, pageable));
    }

    @GetMapping("/{id}")
    public ResponseEntity<TaskResponse> getById(@PathVariable Long id) {
        return ResponseEntity.ok(taskService.getById(id));
    }

    @GetMapping("/{id}/history")
    public ResponseEntity<List<TaskHistoryResponse>> getHistory(@PathVariable Long id) {
        return ResponseEntity.ok(taskService.getHistory(id));
    }

    @PostMapping
    public ResponseEntity<TaskResponse> create(@Valid @RequestBody TaskRequest request) {
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(taskService.create(request, SecurityUtils.getCurrentUser()));
    }

    @PutMapping("/{id}")
    public ResponseEntity<TaskResponse> update(@PathVariable Long id, @Valid @RequestBody TaskRequest request) {
        return ResponseEntity.ok(taskService.update(id, request, SecurityUtils.getCurrentUser()));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        taskService.delete(id);
        return ResponseEntity.noContent().build();
    }

    @PatchMapping("/{id}/status")
    public ResponseEntity<TaskResponse> updateStatus(@PathVariable Long id, @Valid @RequestBody TaskStatusUpdateRequest request) {
        return ResponseEntity.ok(taskService.updateStatus(id, request, SecurityUtils.getCurrentUser()));
    }

    @PatchMapping("/{id}/priority")
    public ResponseEntity<TaskResponse> updatePriority(@PathVariable Long id, @Valid @RequestBody PriorityUpdateRequest request) {
        return ResponseEntity.ok(taskService.updatePriority(id, request, SecurityUtils.getCurrentUser()));
    }

    @PostMapping("/{id}/assign/{driverId}")
    @Operation(summary = "Assign task to driver")
    public ResponseEntity<TaskResponse> assign(@PathVariable Long id, @PathVariable Long driverId) {
        return ResponseEntity.ok(taskService.assignDriver(id, driverId, SecurityUtils.getCurrentUser()));
    }

    @PostMapping("/{id}/assign-recommended")
    @Operation(summary = "Assign task using AI recommendation")
    public ResponseEntity<TaskResponse> assignRecommended(@PathVariable Long id) {
        return ResponseEntity.ok(taskService.assignRecommendedDriver(id, SecurityUtils.getCurrentUser()));
    }
}
