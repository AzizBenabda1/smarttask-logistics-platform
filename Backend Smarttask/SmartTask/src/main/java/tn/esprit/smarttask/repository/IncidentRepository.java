package tn.esprit.smarttask.repository;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import tn.esprit.smarttask.entity.Incident;
import tn.esprit.smarttask.entity.IncidentStatus;

import java.util.List;

@Repository
public interface IncidentRepository extends JpaRepository<Incident, Long> {
    List<Incident> findByReporterIdOrderByCreatedAtDesc(Long reporterId);
    long countByReporterId(Long reporterId);
    long countByStatus(IncidentStatus status);
    Page<Incident> findByStatusOrderByCreatedAtDesc(IncidentStatus status, Pageable pageable);
    Page<Incident> findAllByOrderByCreatedAtDesc(Pageable pageable);
}
