package tn.esprit.smarttask.controller;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;
import tn.esprit.smarttask.dto.ai.*;
import tn.esprit.smarttask.dto.request.TaskIdRequest;
import tn.esprit.smarttask.dto.response.TaskAIAnalysisResponse;
import tn.esprit.smarttask.service.AIService;

import java.util.Map;

@RestController
@RequestMapping("/api/manager/ai")
@RequiredArgsConstructor
@PreAuthorize("hasRole('MANAGER')")
@Tag(name = "Manager AI", description = "SmartTask AI proxy endpoints (Python microservice)")
@SecurityRequirement(name = "Bearer Authentication")
public class ManagerAIController {

    private final AIService aiService;

    @GetMapping("/health")
    @Operation(summary = "Proxy AI microservice health")
    public ResponseEntity<Map<String, Object>> health() {
        return ResponseEntity.ok(aiService.health());
    }

    @GetMapping("/model-status")
    public ResponseEntity<Map<String, Object>> modelStatus() {
        return ResponseEntity.ok(aiService.modelStatus());
    }

    @PostMapping("/predict-delay")
    public ResponseEntity<AIDelayPredictionResponse> predictDelay(@Valid @RequestBody TaskIdRequest request) {
        return ResponseEntity.ok(aiService.predictDelay(request.getTaskId()));
    }

    @PostMapping("/predict-delivery-time")
    public ResponseEntity<AIDeliveryTimePredictionResponse> predictDeliveryTime(
            @Valid @RequestBody TaskIdRequest request) {
        return ResponseEntity.ok(aiService.predictDeliveryTime(request.getTaskId()));
    }

    @PostMapping("/prioritize-task")
    public ResponseEntity<AITaskPrioritizationResponse> prioritizeTask(@Valid @RequestBody TaskIdRequest request) {
        return ResponseEntity.ok(aiService.prioritizeTask(request.getTaskId()));
    }

    @PostMapping("/recommend-driver")
    public ResponseEntity<AIDriverRecommendationResponse> recommendDriver(
            @Valid @RequestBody TaskIdRequest request) {
        return ResponseEntity.ok(aiService.recommendDriver(request.getTaskId()));
    }

    @PostMapping("/detect-anomaly")
    public ResponseEntity<AIAnomalyDetectionResponse> detectAnomaly(@Valid @RequestBody TaskIdRequest request) {
        return ResponseEntity.ok(aiService.detectAnomaly(request.getTaskId()));
    }

    @PostMapping("/analyze")
    @Operation(summary = "Full AI analysis: delay risk + delivery time + priority")
    public ResponseEntity<TaskAIAnalysisResponse> analyzeTask(@Valid @RequestBody TaskIdRequest request) {
        return ResponseEntity.ok(aiService.analyzeTask(request.getTaskId()));
    }

    @PostMapping("/predict-delivery-success")
    @Operation(summary = "Predict first-attempt delivery success probability")
    public ResponseEntity<AIDeliverySuccessPredictionResponse> predictDeliverySuccess(
            @Valid @RequestBody TaskIdRequest request) {
        return ResponseEntity.ok(aiService.predictDeliverySuccess(request.getTaskId()));
    }
}
