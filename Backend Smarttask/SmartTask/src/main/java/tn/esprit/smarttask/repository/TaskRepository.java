package tn.esprit.smarttask.repository;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import tn.esprit.smarttask.entity.Priority;
import tn.esprit.smarttask.entity.Task;
import tn.esprit.smarttask.entity.TaskStatus;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface TaskRepository extends JpaRepository<Task, Long>, JpaSpecificationExecutor<Task> {

    long countByStatus(TaskStatus status);

    @Query("SELECT COUNT(t) FROM Task t WHERE t.status <> :completed AND t.status <> :cancelled AND t.deadline < :now")
    long countDelayedTasks(@Param("now") LocalDateTime now, @Param("completed") TaskStatus completed, @Param("cancelled") TaskStatus cancelled);

    @Query("SELECT COUNT(t) FROM Task t WHERE t.scheduledDate = :date")
    long countByScheduledDate(@Param("date") LocalDate date);

    @Query("SELECT COUNT(t) FROM Task t WHERE t.priority = :priority")
    long countByPriority(@Param("priority") Priority priority);

    @Query("SELECT COALESCE(AVG(t.actualMinutes), 0) FROM Task t WHERE t.status = :status AND t.actualMinutes IS NOT NULL")
    double avgActualMinutesByStatus(@Param("status") TaskStatus status);

    @Query("SELECT t.scheduledDate, COUNT(t) FROM Task t WHERE t.status = :status AND t.scheduledDate IS NOT NULL GROUP BY t.scheduledDate ORDER BY t.scheduledDate DESC")
    List<Object[]> countByScheduledDateGrouped(@Param("status") TaskStatus status, Pageable pageable);

    @Query("SELECT t.scheduledDate, COUNT(t) FROM Task t WHERE t.status = :status AND t.scheduledDate IS NOT NULL GROUP BY t.scheduledDate ORDER BY t.scheduledDate DESC")
    List<Object[]> countDelayedByDay(@Param("status") TaskStatus status, Pageable pageable);

    @Query("SELECT t FROM Task t WHERE t.deadline < :now AND t.status NOT IN :excluded")
    List<Task> findOverdueTasks(@Param("now") LocalDateTime now, @Param("excluded") List<TaskStatus> excluded);

    @Query("SELECT t FROM Task t WHERE t.deadline < :now AND t.status NOT IN :excluded ORDER BY t.deadline ASC")
    List<Task> findDelayedTasks(@Param("now") LocalDateTime now, @Param("excluded") List<TaskStatus> excluded);

    List<Task> findByDriverIsNullAndStatus(TaskStatus status);

    List<Task> findByDriverId(Long driverId);

    List<Task> findByClientIdOrderByCreatedAtDesc(Long clientId);

    long countByDriverIdAndStatus(Long driverId, TaskStatus status);

    List<Task> findByDriverIdAndStatusIn(Long driverId, List<TaskStatus> statuses);

    long countByClient_Id(Long clientId);

    @Query("SELECT COALESCE(AVG(dp.performanceScore), 0) FROM DriverProfile dp")
    double avgDriverPerformance();
}
