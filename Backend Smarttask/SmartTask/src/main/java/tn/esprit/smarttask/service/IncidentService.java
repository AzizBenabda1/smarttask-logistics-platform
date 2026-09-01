package tn.esprit.smarttask.service;

import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import tn.esprit.smarttask.dto.request.IncidentUpdateRequest;
import tn.esprit.smarttask.dto.response.IncidentResponse;
import tn.esprit.smarttask.dto.response.PageResponse;
import tn.esprit.smarttask.entity.*;
import tn.esprit.smarttask.exception.AccessDeniedResourceException;
import tn.esprit.smarttask.repository.IncidentRepository;

@Service
@RequiredArgsConstructor
public class IncidentService {

    private final IncidentRepository incidentRepository;
    private final NotificationHelper notificationHelper;

    @Transactional(readOnly = true)
    public PageResponse<IncidentResponse> getIncidents(IncidentStatus status, Pageable pageable) {
        Page<Incident> page = status != null
                ? incidentRepository.findByStatusOrderByCreatedAtDesc(status, pageable)
                : incidentRepository.findAllByOrderByCreatedAtDesc(pageable);
        return PageResponse.of(page.map(this::toResponse));
    }

    @Transactional
    public IncidentResponse updateStatus(Long id, IncidentUpdateRequest request, User manager) {
        Incident incident = incidentRepository.findById(id)
                .orElseThrow(() -> new AccessDeniedResourceException("Incident not found"));
        incident.setStatus(request.getStatus());
        Incident saved = incidentRepository.save(incident);

        if (incident.getReporter() != null) {
            notificationHelper.notifyUser(incident.getReporter(), NotificationType.DELIVERY_ISSUE,
                    "Incident mis à jour",
                    "Votre signalement #" + id + " est maintenant " + request.getStatus()
                            + (request.getResolutionNote() != null ? " — " + request.getResolutionNote() : ""),
                    incident.getTask(), Priority.MEDIUM);
        }
        return toResponse(saved);
    }

    private IncidentResponse toResponse(Incident i) {
        return IncidentResponse.builder()
                .id(i.getId())
                .type(i.getType())
                .description(i.getDescription())
                .priority(i.getPriority())
                .status(i.getStatus())
                .taskId(i.getTask() != null ? i.getTask().getId() : null)
                .orderId(i.getOrder() != null ? i.getOrder().getId() : null)
                .reporterName(i.getReporter().getFirstName() + " " + i.getReporter().getLastName())
                .createdAt(i.getCreatedAt())
                .build();
    }
}
