package tn.esprit.smarttask.controller;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;
import tn.esprit.smarttask.dto.request.IncidentRequest;
import tn.esprit.smarttask.dto.request.OrderRequest;
import tn.esprit.smarttask.dto.response.*;
import tn.esprit.smarttask.entity.OrderStatus;
import tn.esprit.smarttask.entity.Priority;
import tn.esprit.smarttask.security.SecurityUtils;
import tn.esprit.smarttask.service.AIService;
import tn.esprit.smarttask.service.OperatorService;

import java.util.List;

@RestController
@RequestMapping("/api/operator")
@RequiredArgsConstructor
@PreAuthorize("hasRole('OPERATOR')")
@Tag(name = "Operator", description = "Operator workspace endpoints")
@SecurityRequirement(name = "Bearer Authentication")
public class OperatorController {

    private final OperatorService operatorService;
    private final AIService aiService;

    @GetMapping("/dashboard")
    @Operation(summary = "Operator dashboard KPIs")
    public ResponseEntity<OperatorDashboardResponse> dashboard() {
        return ResponseEntity.ok(operatorService.getDashboard(SecurityUtils.getCurrentUser()));
    }

    @GetMapping("/orders")
    public ResponseEntity<PageResponse<OrderResponse>> getOrders(
            @RequestParam(required = false) OrderStatus status,
            @RequestParam(required = false) Priority priority,
            @RequestParam(required = false) Long clientId,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        Pageable pageable = PageRequest.of(page, size, Sort.by(Sort.Direction.DESC, "createdAt"));
        return ResponseEntity.ok(operatorService.getOrdersPage(status, priority, clientId, pageable));
    }

    @GetMapping("/orders/pending")
    public ResponseEntity<List<OrderResponse>> pendingOrders() {
        return ResponseEntity.ok(operatorService.getPendingOrders());
    }

    @GetMapping("/orders/{id}")
    public ResponseEntity<OrderResponse> getOrder(@PathVariable Long id) {
        return ResponseEntity.ok(operatorService.getOrder(id));
    }

    @PostMapping("/orders")
    public ResponseEntity<OrderResponse> createOrder(@Valid @RequestBody OrderRequest request) {
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(operatorService.createOrder(request, SecurityUtils.getCurrentUser()));
    }

    @PutMapping("/orders/{id}")
    public ResponseEntity<OrderResponse> updateOrder(@PathVariable Long id, @Valid @RequestBody OrderRequest request) {
        return ResponseEntity.ok(operatorService.updateOrder(id, request, SecurityUtils.getCurrentUser()));
    }

    @PostMapping("/orders/{id}/verify")
    public ResponseEntity<OrderResponse> verifyOrder(@PathVariable Long id) {
        return ResponseEntity.ok(operatorService.verifyOrder(id, SecurityUtils.getCurrentUser()));
    }

    @GetMapping("/tasks")
    public ResponseEntity<List<TaskResponse>> getTasks() {
        return ResponseEntity.ok(operatorService.getTasks());
    }

    @PostMapping("/tasks/{orderId}/prepare")
    public ResponseEntity<TaskResponse> prepareTask(@PathVariable Long orderId) {
        return ResponseEntity.ok(operatorService.prepareTask(orderId, SecurityUtils.getCurrentUser()));
    }

    @GetMapping("/clients")
    public ResponseEntity<List<ClientResponse>> getClients() {
        return ResponseEntity.ok(operatorService.getClients());
    }

    @GetMapping("/incidents")
    public ResponseEntity<List<IncidentResponse>> getIncidents() {
        return ResponseEntity.ok(operatorService.getIncidents(SecurityUtils.getCurrentUser()));
    }

    @PostMapping("/incidents")
    public ResponseEntity<IncidentResponse> createIncident(@Valid @RequestBody IncidentRequest request) {
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(operatorService.createIncident(request, SecurityUtils.getCurrentUser()));
    }

    @PostMapping("/ai/delivery-success/preview")
    @Operation(summary = "Preview delivery success score before creating order")
    public ResponseEntity<tn.esprit.smarttask.dto.ai.AIDeliverySuccessPredictionResponse> previewDeliverySuccess(
            @Valid @RequestBody OrderRequest request) {
        return ResponseEntity.ok(aiService.previewDeliverySuccess(request));
    }
}
