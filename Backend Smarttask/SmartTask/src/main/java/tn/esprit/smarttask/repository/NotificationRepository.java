package tn.esprit.smarttask.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import tn.esprit.smarttask.entity.Notification;

import java.util.List;

@Repository
public interface NotificationRepository extends JpaRepository<Notification, Long> {
    List<Notification> findByUserIdOrderByCreatedAtDesc(Long userId);
    long countByUserIdAndReadFlagFalse(Long userId);
    boolean existsByUserIdAndTitleAndCreatedAtAfter(Long userId, String title, java.time.LocalDateTime after);
    boolean existsByUserIdAndMessageContainingAndCreatedAtAfter(Long userId, String fragment, java.time.LocalDateTime after);
}
