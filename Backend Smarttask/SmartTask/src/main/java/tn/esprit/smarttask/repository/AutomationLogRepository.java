package tn.esprit.smarttask.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import tn.esprit.smarttask.entity.AutomationLog;

import java.util.List;

@Repository
public interface AutomationLogRepository extends JpaRepository<AutomationLog, Long> {

    List<AutomationLog> findTop50ByChainTypeOrderByCreatedAtDesc(String chainType);

    List<AutomationLog> findByRunIdOrderByStepNumberAsc(String runId);

    List<AutomationLog> findByOrderIdOrderByCreatedAtDesc(Long orderId);
}
