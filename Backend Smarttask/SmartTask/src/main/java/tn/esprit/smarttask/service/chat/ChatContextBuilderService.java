package tn.esprit.smarttask.service.chat;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import tn.esprit.smarttask.dto.ai.AIChatContext;
import tn.esprit.smarttask.dto.ai.AIChatContextItem;
import tn.esprit.smarttask.entity.*;
import tn.esprit.smarttask.repository.*;

import java.time.LocalDateTime;
import java.util.*;

@Service
@RequiredArgsConstructor
public class ChatContextBuilderService {

    private final TaskRepository taskRepository;
    private final OrderRepository orderRepository;
    private final DriverProfileRepository driverProfileRepository;
    private final UserRepository userRepository;

    @Transactional(readOnly = true)
    public AIChatContext buildContext(User user) {
        return AIChatContext.builder()
                .role(user.getRole().name())
                .userName(user.getFirstName() + " " + user.getLastName())
                .stats(buildStatsForUser(user))
                .tasks(buildTasks(user, user.getRole()))
                .orders(buildOrders(user, user.getRole()))
                .drivers(buildDrivers(user.getRole()))
                .build();
    }

    private Map<String, Object> buildStatsForUser(User user) {
        Map<String, Object> stats = new LinkedHashMap<>();
        LocalDateTime now = LocalDateTime.now();
        Role role = user.getRole();

        if (role == Role.MANAGER || role == Role.ADMIN) {
            stats.put("totalTasks", taskRepository.count());
            stats.put("pendingTasks", taskRepository.countByStatus(TaskStatus.PENDING));
            stats.put("delayedTasks", taskRepository.countDelayedTasks(now, TaskStatus.COMPLETED, TaskStatus.CANCELLED));
            stats.put("completedTasks", taskRepository.countByStatus(TaskStatus.COMPLETED));
            stats.put("availableDrivers", driverProfileRepository.countByStatus(DriverStatus.AVAILABLE));
            stats.put("totalDrivers", userRepository.countByRole(Role.DRIVER));
        } else if (role == Role.OPERATOR) {
            stats.put("pendingOrders", orderRepository.countByStatus(OrderStatus.PENDING));
            stats.put("verifiedOrders", orderRepository.countByStatus(OrderStatus.VERIFIED));
        } else if (role == Role.DRIVER) {
            long active = taskRepository.findByDriverIdAndStatusIn(user.getId(),
                    List.of(TaskStatus.ASSIGNED, TaskStatus.IN_PROGRESS, TaskStatus.IN_DELIVERY)).size();
            stats.put("activeMissions", active);
        } else if (role == Role.CLIENT) {
            stats.put("totalOrders", orderRepository.findByClientIdOrderByCreatedAtDesc(user.getId()).size());
        }
        return stats;
    }

    private List<AIChatContextItem> buildTasks(User user, Role role) {
        List<Task> tasks = switch (role) {
            case MANAGER, ADMIN -> {
                List<Task> delayed = taskRepository.findDelayedTasks(LocalDateTime.now(),
                        List.of(TaskStatus.COMPLETED, TaskStatus.CANCELLED));
                if (!delayed.isEmpty()) yield delayed.stream().limit(10).toList();
                yield taskRepository.findAll().stream().limit(10).toList();
            }
            case DRIVER -> taskRepository.findByDriverId(user.getId()).stream().limit(10).toList();
            case CLIENT -> taskRepository.findByClientIdOrderByCreatedAtDesc(user.getId()).stream().limit(10).toList();
            case OPERATOR -> taskRepository.findAll().stream()
                    .filter(t -> t.getStatus() == TaskStatus.PENDING || t.getStatus() == TaskStatus.ASSIGNED)
                    .limit(10).toList();
        };

        return tasks.stream().map(this::toTaskItem).toList();
    }

    private AIChatContextItem toTaskItem(Task t) {
        Map<String, Object> extra = new HashMap<>();
        extra.put("address", t.getDeliveryAddress());
        extra.put("delayed", t.getDeadline() != null && t.getDeadline().isBefore(LocalDateTime.now())
                && t.getStatus() != TaskStatus.COMPLETED && t.getStatus() != TaskStatus.CANCELLED);
        if (t.getEstimatedMinutes() != null) extra.put("estimatedMinutes", t.getEstimatedMinutes());
        String clientName = t.getClient() != null ? t.getClient().getFirstName() + " " + t.getClient().getLastName() : "";
        return AIChatContextItem.builder()
                .id(t.getId())
                .label(t.getTitle() + (clientName.isBlank() ? "" : " — " + clientName))
                .status(t.getStatus().name())
                .extra(extra)
                .build();
    }

    private List<AIChatContextItem> buildOrders(User user, Role role) {
        List<Order> orders = switch (role) {
            case CLIENT -> orderRepository.findByClientIdOrderByCreatedAtDesc(user.getId()).stream().limit(10).toList();
            case OPERATOR -> orderRepository.findByStatusOrderByCreatedAtDesc(OrderStatus.PENDING).stream().limit(10).toList();
            default -> List.of();
        };

        return orders.stream().map(o -> {
            Map<String, Object> extra = new HashMap<>();
            if (o.getTaskId() != null) extra.put("taskId", o.getTaskId());
            return AIChatContextItem.builder()
                    .id(o.getId())
                    .label(o.getProducts())
                    .status(o.getStatus().name())
                    .extra(extra)
                    .build();
        }).toList();
    }

    private List<AIChatContextItem> buildDrivers(Role role) {
        if (role != Role.MANAGER && role != Role.ADMIN) {
            return List.of();
        }
        return driverProfileRepository.findAll().stream().limit(15).map(dp -> {
            User u = dp.getUser();
            Map<String, Object> extra = new HashMap<>();
            extra.put("zone", dp.getZone() != null ? dp.getZone() : "N/A");
            extra.put("load", dp.getCurrentLoad());
            extra.put("performance", dp.getPerformanceScore());
            return AIChatContextItem.builder()
                    .id(u.getId())
                    .label(u.getFirstName() + " " + u.getLastName())
                    .status(dp.getStatus().name())
                    .extra(extra)
                    .build();
        }).toList();
    }
}
