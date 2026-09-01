package tn.esprit.smarttask.service.driver;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import tn.esprit.smarttask.config.DriverAlertProperties;
import tn.esprit.smarttask.entity.*;
import tn.esprit.smarttask.exception.AIServiceUnavailableException;
import tn.esprit.smarttask.repository.NotificationRepository;
import tn.esprit.smarttask.repository.TaskRepository;
import tn.esprit.smarttask.repository.UserRepository;
import tn.esprit.smarttask.service.AIService;
import tn.esprit.smarttask.service.NotificationHelper;

import java.time.LocalDateTime;
import java.time.temporal.ChronoUnit;
import java.util.List;

@Service
@RequiredArgsConstructor
@Slf4j
public class DriverProactiveAlertService {

    private static final List<TaskStatus> ACTIVE = List.of(
            TaskStatus.ASSIGNED, TaskStatus.ACCEPTED, TaskStatus.IN_PROGRESS, TaskStatus.IN_DELIVERY);

    private final TaskRepository taskRepository;
    private final UserRepository userRepository;
    private final NotificationRepository notificationRepository;
    private final NotificationHelper notificationHelper;
    private final AIService aiService;
    private final DriverAlertProperties properties;

    @Transactional
    public int scanAndNotify() {
        if (!properties.isEnabled()) return 0;

        int sent = 0;
        List<User> drivers = userRepository.findByRole(Role.DRIVER).stream().filter(User::isActive).toList();
        for (User driver : drivers) {
            List<Task> missions = taskRepository.findByDriverIdAndStatusIn(driver.getId(), ACTIVE);
            if (missions.isEmpty()) continue;

            sent += checkMissionCountAlert(driver, missions);
            sent += checkDeadlineAlerts(driver, missions);
            sent += checkTrafficAlert(driver, missions);
        }
        if (sent > 0) {
            log.info("Driver proactive alerts sent: {}", sent);
        }
        return sent;
    }

    private int checkMissionCountAlert(User driver, List<Task> missions) {
        if (missions.size() < 3) return 0;
        String title = "IA — Charge de missions";
        if (recentlySentByTitle(driver.getId(), title)) return 0;

        Task urgent = missions.stream()
                .min((a, b) -> a.getDeadline().compareTo(b.getDeadline()))
                .orElse(missions.get(0));
        long minutes = ChronoUnit.MINUTES.between(LocalDateTime.now(), urgent.getDeadline());
        String msg = String.format("Vous avez %d missions actives — la #%d expire dans %d min",
                missions.size(), urgent.getId(), Math.max(0, minutes));
        notificationHelper.notifyUser(driver, NotificationType.AI_RECOMMENDATION, title, msg, urgent, Priority.HIGH);
        return 1;
    }

    private int checkDeadlineAlerts(User driver, List<Task> missions) {
        int sent = 0;
        LocalDateTime now = LocalDateTime.now();
        for (Task task : missions) {
            long minutesLeft = ChronoUnit.MINUTES.between(now, task.getDeadline());
            if (minutesLeft < 0) continue;

            String taskRef = "Mission #" + task.getId();

            if (minutesLeft <= properties.getDelayRiskMinutes()) {
                String title = "IA — Risque de retard";
                if (!recentlySentByMessage(driver.getId(), taskRef)) {
                    String msg = String.format(
                            "%s : risque de retard dans %d min — accélérez ou signalez un incident",
                            taskRef, minutesLeft);
                    Priority p = task.getPriority() == Priority.CRITICAL ? Priority.CRITICAL : Priority.HIGH;
                    notificationHelper.notifyUser(driver, NotificationType.URGENT, title, msg, task, p);
                    sent++;
                }
            } else if (minutesLeft <= properties.getDeadlineWarningMinutes()) {
                String title = "IA — Deadline proche";
                if (!recentlySentByMessage(driver.getId(), taskRef)) {
                    try {
                        var delay = aiService.predictDelay(task.getId());
                        if (delay.getDelayProbability() != null && delay.getDelayProbability() > 0.6) {
                            String msg = String.format(
                                    "%s : risque de retard élevé (%.0f%%) — deadline dans %d min",
                                    taskRef, delay.getDelayProbability() * 100, minutesLeft);
                            notificationHelper.notifyUser(driver, NotificationType.DELAY, title, msg, task, Priority.HIGH);
                            sent++;
                            continue;
                        }
                    } catch (AIServiceUnavailableException ignored) {
                        // message sans score ML
                    }
                    String msg = String.format("%s : deadline dans %d min", taskRef, minutesLeft);
                    notificationHelper.notifyUser(driver, NotificationType.DELAY, title, msg, task, Priority.MEDIUM);
                    sent++;
                }
            }
        }
        return sent;
    }

    private int checkTrafficAlert(User driver, List<Task> missions) {
        int hour = LocalDateTime.now().getHour();
        if (hour < 8 || hour > 19) return 0;

        boolean tunisPeak = missions.stream().anyMatch(t ->
                (t.getZone() != null && t.getZone().toLowerCase().contains("tunis"))
                        || (t.getDeliveryAddress() != null && t.getDeliveryAddress().toLowerCase().contains("tunis")));
        if (!tunisPeak) return 0;

        String title = "IA — Trafic dense";
        if (recentlySentByTitle(driver.getId(), title)) return 0;

        int extra = (hour >= 17 && hour <= 19) || (hour >= 8 && hour <= 10) ? 12 : 8;
        String msg = String.format("Trafic dense zone Tunis — +%d min estimés sur vos livraisons", extra);
        notificationHelper.notifyUser(driver, NotificationType.AI_RECOMMENDATION, title, msg,
                missions.get(0), Priority.MEDIUM);
        return 1;
    }

    private boolean recentlySentByTitle(Long userId, String title) {
        return notificationRepository.existsByUserIdAndTitleAndCreatedAtAfter(
                userId, title, LocalDateTime.now().minusMinutes(properties.getDedupMinutes()));
    }

    private boolean recentlySentByMessage(Long userId, String messageFragment) {
        return notificationRepository.existsByUserIdAndMessageContainingAndCreatedAtAfter(
                userId, messageFragment, LocalDateTime.now().minusMinutes(properties.getDedupMinutes()));
    }
}
