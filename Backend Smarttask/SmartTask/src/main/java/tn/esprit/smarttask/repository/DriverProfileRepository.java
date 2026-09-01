package tn.esprit.smarttask.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import tn.esprit.smarttask.entity.DriverProfile;
import tn.esprit.smarttask.entity.DriverStatus;

import java.util.List;
import java.util.Optional;

@Repository
public interface DriverProfileRepository extends JpaRepository<DriverProfile, Long> {
    Optional<DriverProfile> findByUserId(Long userId);
    List<DriverProfile> findByStatus(DriverStatus status);
    long countByStatus(DriverStatus status);
}
