package tn.esprit.smarttask.controller;

import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;
import tn.esprit.smarttask.dto.request.DeliveryConfirmRequest;
import tn.esprit.smarttask.dto.request.IncidentRequest;
import tn.esprit.smarttask.dto.request.ReviewRequest;
import tn.esprit.smarttask.dto.response.*;
import tn.esprit.smarttask.security.SecurityUtils;
import tn.esprit.smarttask.service.ClientService;
import tn.esprit.smarttask.service.RealTimeEventService;

import java.util.List;

@RestController
@RequestMapping("/api/client")
@RequiredArgsConstructor
@PreAuthorize("hasRole('CLIENT')")
@Tag(name = "Client", description = "Client final endpoints")
@SecurityRequirement(name = "Bearer Authentication")
public class ClientController {

    private final ClientService clientService;
    private final RealTimeEventService realTimeEventService;

    @GetMapping("/dashboard")
    public ResponseEntity<ClientDashboardResponse> dashboard() {
        return ResponseEntity.ok(clientService.getDashboard(SecurityUtils.getCurrentUser()));
    }

    @GetMapping("/orders")
    public ResponseEntity<List<OrderResponse>> getOrders() {
        return ResponseEntity.ok(clientService.getOrders(SecurityUtils.getCurrentUser()));
    }

    @GetMapping("/orders/{id}")
    public ResponseEntity<OrderResponse> getOrder(@PathVariable Long id) {
        return ResponseEntity.ok(clientService.getOrder(id, SecurityUtils.getCurrentUser()));
    }

    @GetMapping("/deliveries/{id}")
    public ResponseEntity<DeliveryTrackingResponse> getDelivery(@PathVariable Long id) {
        return ResponseEntity.ok(clientService.getDelivery(id, SecurityUtils.getCurrentUser()));
    }

    @GetMapping(value = "/deliveries/{id}/stream", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public SseEmitter streamDelivery(@PathVariable Long id) {
        clientService.assertTaskAccess(id, SecurityUtils.getCurrentUser());
        return realTimeEventService.subscribeTask(id);
    }

    @PostMapping("/deliveries/{id}/confirm")
    public ResponseEntity<TaskResponse> confirmDelivery(@PathVariable Long id,
            @RequestBody(required = false) DeliveryConfirmRequest request) {
        if (request == null) request = new DeliveryConfirmRequest();
        return ResponseEntity.ok(clientService.confirmDelivery(id, request, SecurityUtils.getCurrentUser()));
    }

    @PostMapping("/incidents")
    public ResponseEntity<IncidentResponse> createIncident(@Valid @RequestBody IncidentRequest request) {
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(clientService.createIncident(request, SecurityUtils.getCurrentUser()));
    }

    @PostMapping("/reviews")
    public ResponseEntity<ReviewResponse> createReview(@Valid @RequestBody ReviewRequest request) {
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(clientService.createReview(request, SecurityUtils.getCurrentUser()));
    }

    @GetMapping("/reviews")
    public ResponseEntity<List<ReviewResponse>> getReviews() {
        return ResponseEntity.ok(clientService.getReviews(SecurityUtils.getCurrentUser()));
    }

    @GetMapping("/notifications")
    public ResponseEntity<List<NotificationResponse>> getNotifications() {
        return ResponseEntity.ok(clientService.getNotifications(SecurityUtils.getCurrentUser()));
    }
}
