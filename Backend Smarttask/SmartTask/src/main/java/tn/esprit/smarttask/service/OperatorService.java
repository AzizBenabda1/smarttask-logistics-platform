package tn.esprit.smarttask.service;

import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.domain.Specification;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import tn.esprit.smarttask.dto.request.IncidentRequest;
import tn.esprit.smarttask.dto.request.OrderRequest;
import tn.esprit.smarttask.dto.response.*;
import tn.esprit.smarttask.entity.*;
import tn.esprit.smarttask.exception.*;
import tn.esprit.smarttask.event.OrderCreatedEvent;
import tn.esprit.smarttask.mapper.OrderMapper;
import tn.esprit.smarttask.mapper.TaskMapper;
import tn.esprit.smarttask.repository.*;

import jakarta.persistence.criteria.Predicate;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import org.springframework.context.ApplicationEventPublisher;

@Service
@RequiredArgsConstructor
public class OperatorService {

    private final OrderRepository orderRepository;
    private final TaskRepository taskRepository;
    private final TaskHistoryRepository taskHistoryRepository;
    private final IncidentRepository incidentRepository;
    private final NotificationRepository notificationRepository;
    private final UserRepository userRepository;
    private final OrderMapper orderMapper;
    private final TaskMapper taskMapper;
    private final NotificationHelper notificationHelper;
    private final ApplicationEventPublisher eventPublisher;
    private final ProductTypeService productTypeService;

    @Transactional(readOnly = true)
    public OperatorDashboardResponse getDashboard(User operator) {
        LocalDate today = LocalDate.now();
        return OperatorDashboardResponse.builder()
                .ordersToday(orderRepository.findByScheduledDate(today).size())
                .pendingOrders(orderRepository.countByStatus(OrderStatus.PENDING))
                .verifiedOrders(orderRepository.countByStatus(OrderStatus.VERIFIED))
                .readyOrders(orderRepository.countByStatus(OrderStatus.READY))
                .tasksToPrepare(taskRepository.countByStatus(TaskStatus.PENDING))
                .tasksInProgress(taskRepository.countByStatus(TaskStatus.IN_PROGRESS)
                        + taskRepository.countByStatus(TaskStatus.IN_DELIVERY))
                .tasksCompleted(taskRepository.countByStatus(TaskStatus.COMPLETED))
                .openIncidents(incidentRepository.countByStatus(IncidentStatus.OPEN)
                        + incidentRepository.countByStatus(IncidentStatus.IN_PROGRESS))
                .deliveriesInProgress(taskRepository.countByStatus(TaskStatus.IN_DELIVERY))
                .alerts(notificationRepository.findByUserIdOrderByCreatedAtDesc(operator.getId())
                        .stream().limit(5).map(taskMapper::toNotificationResponse).toList())
                .build();
    }

    @Transactional(readOnly = true)
    public PageResponse<OrderResponse> getOrdersPage(OrderStatus status, Priority priority, Long clientId, Pageable pageable) {
        Specification<Order> spec = buildOrderSpec(status, priority, clientId);
        Page<Order> page = orderRepository.findAll(spec, pageable);
        return PageResponse.of(page.map(orderMapper::toResponse));
    }

    @Transactional(readOnly = true)
    public List<OrderResponse> getOrders(OrderStatus status, Priority priority, Long clientId) {
        return orderRepository.findAll(buildOrderSpec(status, priority, clientId)).stream()
                .map(orderMapper::toResponse).toList();
    }

    private Specification<Order> buildOrderSpec(OrderStatus status, Priority priority, Long clientId) {
        return (root, query, cb) -> {
            List<Predicate> preds = new ArrayList<>();
            if (status != null) preds.add(cb.equal(root.get("status"), status));
            if (priority != null) preds.add(cb.equal(root.get("priority"), priority));
            if (clientId != null) preds.add(cb.equal(root.get("client").get("id"), clientId));
            return cb.and(preds.toArray(new Predicate[0]));
        };
    }

    @Transactional(readOnly = true)
    public OrderResponse getOrder(Long id) {
        return orderMapper.toResponse(findOrder(id));
    }

    @Transactional(readOnly = true)
    public List<OrderResponse> getPendingOrders() {
        return orderRepository.findByStatusOrderByCreatedAtDesc(OrderStatus.PENDING).stream()
                .map(orderMapper::toResponse).toList();
    }

    @Transactional
    public OrderResponse createOrder(OrderRequest request, User operator) {
        User client = userRepository.findById(request.getClientId())
                .orElseThrow(() -> new UserNotFoundException("Client not found"));
        if (client.getRole() != Role.CLIENT) {
            throw new InvalidAssignmentException("Selected user is not a client");
        }
        ResolvedProduct resolved = resolveProduct(request);
        Order order = Order.builder()
                .client(client).operator(operator)
                .productType(resolved.productType())
                .products(resolved.label())
                .quantity(request.getQuantity())
                .amount(request.getAmount()).phone(request.getPhone())
                .deliveryAddress(request.getDeliveryAddress())
                .scheduledDate(request.getScheduledDate()).scheduledTime(request.getScheduledTime())
                .instructions(request.getInstructions()).priority(request.getPriority())
                .status(OrderStatus.PENDING).build();
        Order saved = orderRepository.save(order);
        notificationHelper.notifyManagers(NotificationType.NEW_TASK, "Nouvelle commande",
                "Commande #" + saved.getId() + " — " + saved.getProducts(), null);
        eventPublisher.publishEvent(new OrderCreatedEvent(this, saved.getId(), saved.getPriority().name()));
        return orderMapper.toResponse(saved);
    }

    @Transactional
    public OrderResponse updateOrder(Long id, OrderRequest request, User operator) {
        Order order = findOrder(id);
        User client = userRepository.findById(request.getClientId())
                .orElseThrow(() -> new UserNotFoundException("Client not found"));
        ResolvedProduct resolved = resolveProduct(request);
        order.setClient(client);
        order.setProductType(resolved.productType());
        order.setProducts(resolved.label());
        order.setQuantity(request.getQuantity());
        order.setAmount(request.getAmount());
        order.setPhone(request.getPhone());
        order.setDeliveryAddress(request.getDeliveryAddress());
        order.setScheduledDate(request.getScheduledDate());
        order.setScheduledTime(request.getScheduledTime());
        order.setInstructions(request.getInstructions());
        order.setPriority(request.getPriority());
        return orderMapper.toResponse(orderRepository.save(order));
    }

    private ResolvedProduct resolveProduct(OrderRequest request) {
        if (request.getProductTypeId() != null) {
            ProductType type = productTypeService.getActiveById(request.getProductTypeId());
            String label = type.getName();
            if (request.getProducts() != null && !request.getProducts().isBlank()) {
                label = label + " — " + request.getProducts().trim();
            }
            return new ResolvedProduct(type, label);
        }
        if (request.getCustomProductType() == null || request.getCustomProductType().isBlank()) {
            throw new InvalidStateTransitionException("Choisissez un type de produit ou saisissez un type « Autre »");
        }
        String label = request.getCustomProductType().trim();
        if (request.getProducts() != null && !request.getProducts().isBlank()) {
            label = label + " — " + request.getProducts().trim();
        }
        return new ResolvedProduct(null, label);
    }

    private record ResolvedProduct(ProductType productType, String label) {}

    @Transactional
    public OrderResponse verifyOrder(Long id, User operator) {
        Order order = findOrder(id);
        if (order.getStatus() != OrderStatus.PENDING) {
            throw new InvalidStateTransitionException("Only pending orders can be verified");
        }
        order.setStatus(OrderStatus.VERIFIED);
        Order saved = orderRepository.save(order);
        notificationHelper.notifyUser(order.getClient(), NotificationType.NEW_TASK,
                "Commande validée", "Votre commande #" + id + " a été vérifiée", null, Priority.MEDIUM);
        return orderMapper.toResponse(saved);
    }

    @Transactional
    public TaskResponse prepareTask(Long orderId, User operator) {
        Order order = findOrder(orderId);
        if (order.getStatus() != OrderStatus.VERIFIED && order.getStatus() != OrderStatus.PREPARING) {
            throw new InvalidStateTransitionException("Order must be verified before preparation");
        }
        if (order.getTaskId() != null) {
            throw new InvalidStateTransitionException("Task already created for this order");
        }
        User manager = userRepository.findByRole(Role.MANAGER).stream().findFirst()
                .orElse(operator);

        LocalDateTime deadline = order.getScheduledDate() != null
                ? order.getScheduledDate().atTime(order.getScheduledTime() != null ? order.getScheduledTime() : java.time.LocalTime.of(18, 0))
                : LocalDateTime.now().plusDays(1);

        Task task = Task.builder()
                .title("Livraison commande #" + order.getId())
                .description(order.getProducts())
                .client(order.getClient())
                .createdBy(manager)
                .order(order)
                .deliveryAddress(order.getDeliveryAddress())
                .scheduledDate(order.getScheduledDate())
                .scheduledTime(order.getScheduledTime())
                .deadline(deadline)
                .priority(order.getPriority())
                .status(TaskStatus.PREPARED)
                .instructions(order.getInstructions())
                .weightQuantity(order.getQuantity() + " unité(s)")
                .build();
        Task saved = taskRepository.save(task);
        order.setTaskId(saved.getId());
        order.setStatus(OrderStatus.READY);
        orderRepository.save(order);

        taskHistoryRepository.save(TaskHistory.builder()
                .task(saved).action("PREPARED").newStatus(TaskStatus.PREPARED)
                .performedBy(operator).notes("Task prepared from order #" + orderId).build());

        notificationHelper.notifyManagers(NotificationType.NEW_TASK, "Tâche prête",
                "Tâche #" + saved.getId() + " prête pour affectation", saved);
        return taskMapper.toResponse(saved);
    }

    @Transactional(readOnly = true)
    public List<TaskResponse> getTasks() {
        return taskRepository.findAll().stream()
                .filter(t -> t.getStatus() == TaskStatus.PENDING || t.getStatus() == TaskStatus.PREPARED
                        || t.getStatus() == TaskStatus.ASSIGNED || t.getStatus() == TaskStatus.IN_PROGRESS
                        || t.getStatus() == TaskStatus.IN_DELIVERY)
                .map(taskMapper::toResponse).toList();
    }

    @Transactional
    public IncidentResponse createIncident(IncidentRequest request, User operator) {
        Task task = request.getTaskId() != null ? taskRepository.findById(request.getTaskId())
                .orElseThrow(() -> new TaskNotFoundException("Task not found")) : null;
        Order order = request.getOrderId() != null ? findOrder(request.getOrderId()) : null;

        Incident incident = Incident.builder()
                .reporter(operator).task(task).order(order)
                .type(request.getType()).description(request.getDescription())
                .priority(request.getPriority()).status(IncidentStatus.OPEN).build();
        Incident saved = incidentRepository.save(incident);
        notificationHelper.notifyManagers(NotificationType.DELIVERY_ISSUE, "Incident signalé",
                request.getDescription(), task);
        return toIncidentResponse(saved);
    }

    @Transactional(readOnly = true)
    public List<ClientResponse> getClients() {
        return userRepository.findByRole(Role.CLIENT).stream()
                .map(u -> taskMapper.toClientResponse(u, taskRepository.countByClient_Id(u.getId()))).toList();
    }

    @Transactional(readOnly = true)
    public List<IncidentResponse> getIncidents(User operator) {
        return incidentRepository.findByReporterIdOrderByCreatedAtDesc(operator.getId()).stream()
                .map(this::toIncidentResponse).toList();
    }

    private Order findOrder(Long id) {
        return orderRepository.findById(id).orElseThrow(() -> new OrderNotFoundException("Order not found: " + id));
    }

    private IncidentResponse toIncidentResponse(Incident i) {
        return IncidentResponse.builder()
                .id(i.getId()).type(i.getType()).description(i.getDescription())
                .priority(i.getPriority()).status(i.getStatus())
                .taskId(i.getTask() != null ? i.getTask().getId() : null)
                .orderId(i.getOrder() != null ? i.getOrder().getId() : null)
                .reporterName(i.getReporter().getFirstName() + " " + i.getReporter().getLastName())
                .createdAt(i.getCreatedAt()).build();
    }
}
