package tn.esprit.smarttask.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import tn.esprit.smarttask.entity.Review;

import java.util.List;
import java.util.Optional;

@Repository
public interface ReviewRepository extends JpaRepository<Review, Long> {
    List<Review> findByClientIdOrderByCreatedAtDesc(Long clientId);
    Optional<Review> findByTaskId(Long taskId);
    boolean existsByTaskId(Long taskId);
}
