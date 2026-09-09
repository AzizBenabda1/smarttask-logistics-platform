package tn.esprit.smarttask.service;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import tn.esprit.smarttask.dto.request.DeliveryConfirmRequest;
import tn.esprit.smarttask.dto.request.OrderRequest;
import tn.esprit.smarttask.dto.request.IncidentRequest;
import tn.esprit.smarttask.dto.request.ReviewRequest;
import tn.esprit.smarttask.dto.response.*;
import tn.esprit.smarttask.entity.*;
import tn.esprit.smarttask.exception.*;
import tn.esprit.smarttask.mapper.OrderMapper;
import tn.esprit.smarttask.mapper.TaskMapper;
import tn.esprit.smarttask.repository.*;

import java.util.ArrayList;
import java.util.List;

@Service
@RequiredArgsConstructor
public class ClientService {

    private final OrderRepository orderRepository;
    private final TaskRepository taskRepository;
    private final TaskHistoryRepository taskHistoryRepository;
    private final IncidentRepository incidentRepository;
    private final ReviewRepository reviewRepository;
    private final NotificationRepository notificationRepository;
    private final OrderMapper orderMapper;
    private final TaskMapper taskMapper;
    private final NotificationHelper notificationHelper;
    private final RealTimeEventService realTimeEventService;
    private final OrderProductHelper orderProductHelper;

    @Transactional
    public OrderResponse createOrder(OrderRequest request, User client) {
        OrderProductHelper.ResolvedProduct resolved = orderProductHelper.resolveProduct(request);
        Order order = Order.builder()
                .client(client)
                .operator(null)
                .productType(resolved.productType())
                .products(resolved.label())
                .quantity(request.getQuantity())
                .amount(request.getAmount())
                .phone(request.getPhone() != null ? request.getPhone() : client.getPhone())
                .deliveryAddress(request.getDeliveryAddress())
                .scheduledDate(request.getScheduledDate())
                .scheduledTime(request.getScheduledTime())
                .instructions(request.getInstructions())
                .priority(request.getPriority())
                .status(OrderStatus.PENDING)
                .build();
        Order saved = orderRepository.save(order);
        notificationHelper.notifyOperators(NotificationType.NEW_TASK, "Nouvelle commande client",
                "Commande #" + saved.getId() + " en attente de validation — " + saved.getProducts(), null);
        return orderMapper.toResponse(saved);
    }

    @Transactional(readOnly = true)
    public void assertTaskAccess(Long taskId, User client) {
        getOwnedTask(taskId, client);
    }

    @Transactional(readOnly = true)
    public ClientDashboardResponse getDashboard(User client) {
        List<Order> orders = orderRepository.findByClientIdOrderByCreatedAtDesc(client.getId());
        long active = orders.stream().filter(o -> o.getStatus() != OrderStatus.DELIVERED
                && o.getStatus() != OrderStatus.RECEIVED && o.getStatus() != OrderStatus.CANCELLED).count();
        long delivered = orders.stream().filter(o -> o.getStatus() == OrderStatus.DELIVERED
                || o.getStatus() == OrderStatus.RECEIVED).count();
        long upcoming = orders.stream().filter(o -> o.getStatus() == OrderStatus.READY || o.getStatus() == OrderStatus.IN_DELIVERY).count();
        return ClientDashboardResponse.builder()
                .activeOrders(active)
                .deliveredOrders(delivered)
                .upcomingDeliveries(upcoming)
                .lastOrder(orders.isEmpty() ? null : orderMapper.toResponse(orders.get(0)))
                .notifications(notificationRepository.findByUserIdOrderByCreatedAtDesc(client.getId())
                        .stream().limit(5).map(taskMapper::toNotificationResponse).toList())
                .build();
    }

    @Transactional(readOnly = true)
    public List<OrderResponse> getOrders(User client) {
        return orderRepository.findByClientIdOrderByCreatedAtDesc(client.getId()).stream()
                .map(orderMapper::toResponse).toList();
    }

    @Transactional(readOnly = true)
    public OrderResponse getOrder(Long id, User client) {
        Order order = getOwnedOrder(id, client);
        return orderMapper.toResponse(order);
    }

    @Transactional(readOnly = true)
    public DeliveryTrackingResponse getDelivery(Long taskId, User client) {
        Task task = getOwnedTask(taskId, client);
        return buildTracking(task);
    }

    @Transactional
    public TaskResponse confirmDelivery(Long taskId, DeliveryConfirmRequest request, User client) {
        Task task = getOwnedTask(taskId, client);
        if (task.getStatus() != TaskStatus.COMPLETED) {
            throw new InvalidStateTransitionException("Delivery must be completed before confirmation");
        }
        if (task.isClientConfirmed()) {
            throw new InvalidStateTransitionException("Delivery already confirmed");
        }
        task.setClientConfirmed(true);
        task.setClientReceivedComment(request.getComment());

        if (task.getOrder() != null) {
            Order order = task.getOrder();
            order.setStatus(OrderStatus.RECEIVED);
            orderRepository.save(order);
        }

        taskHistoryRepository.save(TaskHistory.builder()
                .task(task).action("CLIENT_CONFIRMED").oldStatus(task.getStatus())
                .newStatus(task.getStatus()).performedBy(client)
                .notes(request.getComment() != null ? request.getComment() : "Réception confirmée par le client")
                .build());

        notificationHelper.notifyManagers(NotificationType.NEW_TASK, "Réception confirmée",
                "Client a confirmé la livraison #" + taskId, task);
        Task saved = taskRepository.save(task);
        realTimeEventService.publishTaskUpdate(saved, "Réception confirmée par le client");
        return taskMapper.toResponse(saved);
    }

    @Transactional
    public IncidentResponse createIncident(IncidentRequest request, User client) {
        Task task = request.getTaskId() != null ? getOwnedTask(request.getTaskId(), client) : null;
        Order order = request.getOrderId() != null ? getOwnedOrder(request.getOrderId(), client) : null;
        Incident incident = Incident.builder()
                .reporter(client).task(task).order(order)
                .type(request.getType()).description(request.getDescription())
                .priority(request.getPriority()).status(IncidentStatus.OPEN).build();
        Incident saved = incidentRepository.save(incident);
        notificationHelper.notifyManagers(NotificationType.DELIVERY_ISSUE, "Problème client", request.getDescription(), task);
        return IncidentResponse.builder()
                .id(saved.getId()).type(saved.getType()).description(saved.getDescription())
                .priority(saved.getPriority()).status(saved.getStatus())
                .taskId(task != null ? task.getId() : null)
                .orderId(order != null ? order.getId() : null)
                .reporterName(client.getFirstName() + " " + client.getLastName())
                .createdAt(saved.getCreatedAt()).build();
    }

    @Transactional
    public ReviewResponse createReview(ReviewRequest request, User client) {
        Task task = getOwnedTask(request.getTaskId(), client);
        if (task.getStatus() != TaskStatus.COMPLETED) {
            throw new InvalidStateTransitionException("Can only review completed deliveries");
        }
        if (reviewRepository.existsByTaskId(task.getId())) {
            throw new InvalidStateTransitionException("Delivery already reviewed");
        }
        Review review = Review.builder()
                .client(client).task(task)
                .rating(request.getRating()).comment(request.getComment()).build();
        Review saved = reviewRepository.save(review);
        return ReviewResponse.builder()
                .id(saved.getId()).taskId(task.getId())
                .rating(saved.getRating()).comment(saved.getComment())
                .createdAt(saved.getCreatedAt()).build();
    }

    @Transactional(readOnly = true)
    public List<NotificationResponse> getNotifications(User client) {
        return notificationRepository.findByUserIdOrderByCreatedAtDesc(client.getId())
                .stream().map(taskMapper::toNotificationResponse).toList();
    }

    @Transactional(readOnly = true)
    public List<ReviewResponse> getReviews(User client) {
        return reviewRepository.findByClientIdOrderByCreatedAtDesc(client.getId()).stream()
                .map(r -> ReviewResponse.builder()
                        .id(r.getId()).taskId(r.getTask().getId())
                        .rating(r.getRating()).comment(r.getComment())
                        .createdAt(r.getCreatedAt()).build())
                .toList();
    }

    private Order getOwnedOrder(Long id, User client) {
        Order order = orderRepository.findById(id).orElseThrow(() -> new OrderNotFoundException("Order not found"));
        if (!order.getClient().getId().equals(client.getId())) {
            throw new AccessDeniedResourceException("This order does not belong to you");
        }
        return order;
    }

    private Task getOwnedTask(Long id, User client) {
        Task task = taskRepository.findById(id).orElseThrow(() -> new TaskNotFoundException("Task not found"));
        if (!task.getClient().getId().equals(client.getId())) {
            throw new AccessDeniedResourceException("This delivery does not belong to you");
        }
        return task;
    }

    private DeliveryTrackingResponse buildTracking(Task task) {
        TaskStatus s = task.getStatus();
        List<TimelineStep> timeline = new ArrayList<>();
        timeline.add(step("Commande préparée", s.ordinal() >= TaskStatus.PREPARED.ordinal(), s == TaskStatus.PREPARED));
        timeline.add(step("Chauffeur affecté", task.getDriver() != null, s == TaskStatus.ASSIGNED));
        timeline.add(step("Mission acceptée", s.ordinal() >= TaskStatus.ACCEPTED.ordinal(), s == TaskStatus.ACCEPTED));
        timeline.add(step("En livraison", s.ordinal() >= TaskStatus.IN_DELIVERY.ordinal(), s == TaskStatus.IN_DELIVERY));
        timeline.add(step("Livrée", s.ordinal() >= TaskStatus.COMPLETED.ordinal(), s == TaskStatus.COMPLETED && !task.isClientConfirmed()));
        timeline.add(step("Réception confirmée", task.isClientConfirmed(), task.isClientConfirmed()));

        return DeliveryTrackingResponse.builder()
                .taskId(task.getId())
                .orderId(task.getOrder() != null ? task.getOrder().getId() : null)
                .currentStatus(s)
                .driverName(task.getDriver() != null ? task.getDriver().getFirstName() + " " + task.getDriver().getLastName() : null)
                .deliveryAddress(task.getDeliveryAddress())
                .estimatedArrival(task.getDeadline())
                .deadline(task.getDeadline())
                .clientConfirmed(task.isClientConfirmed())
                .hasProofOfDelivery(task.getProofOfDeliveryImage() != null && !task.getProofOfDeliveryImage().isBlank())
                .latitude(task.getLatitude())
                .longitude(task.getLongitude())
                .timeline(timeline)
                .build();
    }

    private TimelineStep step(String label, boolean completed, boolean current) {
        return TimelineStep.builder().label(label).completed(completed).current(current).build();
    }
}
