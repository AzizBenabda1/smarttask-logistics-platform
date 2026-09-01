package tn.esprit.smarttask.service;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import tn.esprit.smarttask.entity.*;
import tn.esprit.smarttask.repository.NotificationRepository;
import tn.esprit.smarttask.repository.UserRepository;

import java.util.List;

@Service
@RequiredArgsConstructor
public class NotificationHelper {

    private final NotificationRepository notificationRepository;
    private final UserRepository userRepository;

    @Transactional
    public void notifyUser(User user, NotificationType type, String title, String message, Task task, Priority priority) {
        notificationRepository.save(Notification.builder()
                .user(user).type(type).title(title).message(message)
                .priority(priority != null ? priority : Priority.MEDIUM)
                .readFlag(false).relatedTask(task).build());
    }

    @Transactional
    public void notifyManagers(NotificationType type, String title, String message, Task task) {
        userRepository.findByRole(Role.MANAGER).forEach(m ->
                notifyUser(m, type, title, message, task, Priority.HIGH));
    }

    @Transactional
    public void notifyOperators(NotificationType type, String title, String message, Task task) {
        userRepository.findByRole(Role.OPERATOR).forEach(o ->
                notifyUser(o, type, title, message, task, Priority.MEDIUM));
    }
}
