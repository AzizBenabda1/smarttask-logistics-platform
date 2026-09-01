package tn.esprit.smarttask.scheduler;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;
import tn.esprit.smarttask.entity.*;
import tn.esprit.smarttask.repository.TaskHistoryRepository;
import tn.esprit.smarttask.repository.TaskRepository;
import tn.esprit.smarttask.service.NotificationHelper;

import java.time.LocalDateTime;
import java.util.List;

@Component
@RequiredArgsConstructor
@Slf4j
public class DelayDetectionScheduler {

    private final TaskRepository taskRepository;
    private final TaskHistoryRepository taskHistoryRepository;
    private final NotificationHelper notificationHelper;

    @Scheduled(fixedRate = 300_000)
    @Transactional
    public void detectAndMarkDelays() {
        LocalDateTime now = LocalDateTime.now();
        List<Task> overdue = taskRepository.findOverdueTasks(now,
                List.of(TaskStatus.COMPLETED, TaskStatus.CANCELLED, TaskStatus.DELAYED));

        if (overdue.isEmpty()) return;

        log.info("Delay detection: {} overdue task(s)", overdue.size());
        for (Task task : overdue) {
            TaskStatus old = task.getStatus();
            task.setStatus(TaskStatus.DELAYED);
            taskRepository.save(task);

            taskHistoryRepository.save(TaskHistory.builder()
                    .task(task).action("AUTO_DELAYED").oldStatus(old)
                    .newStatus(TaskStatus.DELAYED).notes("Deadline dépassée — détection automatique")
                    .build());

            notificationHelper.notifyManagers(NotificationType.DELIVERY_ISSUE, "Retard détecté",
                    "Tâche #" + task.getId() + " en retard — " + task.getTitle(), task);

            if (task.getClient() != null) {
                notificationHelper.notifyUser(task.getClient(), NotificationType.DELIVERY_ISSUE,
                        "Livraison en retard", "Votre livraison \"" + task.getTitle() + "\" est en retard.", task,
                        task.getPriority());
            }
        }
    }
}
