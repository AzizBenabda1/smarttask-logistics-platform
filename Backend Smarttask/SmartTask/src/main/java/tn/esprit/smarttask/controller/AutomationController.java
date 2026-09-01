package tn.esprit.smarttask.controller;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;
import tn.esprit.smarttask.config.ExpressAutomationProperties;
import tn.esprit.smarttask.dto.response.AutomationLogResponse;
import tn.esprit.smarttask.dto.response.AutomationStatusResponse;
import tn.esprit.smarttask.dto.response.ExpressChainResultResponse;
import tn.esprit.smarttask.entity.AutomationLog;
import tn.esprit.smarttask.repository.AutomationLogRepository;
import tn.esprit.smarttask.service.automation.ExpressDeliveryAutomationService;

import java.util.List;

@RestController
@RequestMapping("/api/automation")
@RequiredArgsConstructor
@Tag(name = "IA Automation", description = "Chaînes d'automation SmartTask")
@SecurityRequirement(name = "Bearer Authentication")
public class AutomationController {

    private final ExpressDeliveryAutomationService expressChain;
    private final ExpressAutomationProperties expressProperties;
    private final AutomationLogRepository automationLogRepository;

    @GetMapping("/status")
    @PreAuthorize("hasAnyRole('MANAGER', 'OPERATOR')")
    @Operation(summary = "Statut chaîne Livraison Express Autonome")
    public ResponseEntity<AutomationStatusResponse> status() {
        return ResponseEntity.ok(AutomationStatusResponse.builder()
                .expressEnabled(expressProperties.isEnabled())
                .minDriverScore(expressProperties.getMinDriverScore())
                .autoTriggerPriorities(expressProperties.getAutoTriggerPriorities())
                .chainName("Livraison Express Autonome")
                .stepCount(7)
                .build());
    }

    @PostMapping("/express/{orderId}")
    @PreAuthorize("hasAnyRole('MANAGER', 'OPERATOR')")
    @Operation(summary = "Exécuter la chaîne express (7 instructions IA)")
    public ResponseEntity<ExpressChainResultResponse> runExpress(@PathVariable Long orderId) {
        return ResponseEntity.ok(expressChain.execute(orderId));
    }

    @GetMapping("/logs")
    @PreAuthorize("hasRole('MANAGER')")
    @Operation(summary = "Journal automation")
    public ResponseEntity<List<AutomationLogResponse>> logs() {
        return ResponseEntity.ok(automationLogRepository
                .findTop50ByChainTypeOrderByCreatedAtDesc(ExpressDeliveryAutomationService.CHAIN_TYPE)
                .stream().map(this::toResponse).toList());
    }

    @GetMapping("/logs/run/{runId}")
    @PreAuthorize("hasAnyRole('MANAGER', 'OPERATOR')")
    public ResponseEntity<List<AutomationLogResponse>> logsByRun(@PathVariable String runId) {
        return ResponseEntity.ok(automationLogRepository.findByRunIdOrderByStepNumberAsc(runId)
                .stream().map(this::toResponse).toList());
    }

    private AutomationLogResponse toResponse(AutomationLog log) {
        return AutomationLogResponse.builder()
                .id(log.getId()).runId(log.getRunId()).chainType(log.getChainType())
                .orderId(log.getOrderId()).taskId(log.getTaskId())
                .stepNumber(log.getStepNumber()).stepName(log.getStepName())
                .status(log.getStatus().name()).message(log.getMessage())
                .createdAt(log.getCreatedAt()).build();
    }
}
