package tn.esprit.smarttask.config;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Profile;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;
import tn.esprit.smarttask.entity.*;
import tn.esprit.smarttask.repository.*;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;

@Component
@Profile("!test")
@RequiredArgsConstructor
@Slf4j
public class DataInitializer implements CommandLineRunner {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final DriverProfileRepository driverProfileRepository;
    private final TaskRepository taskRepository;
    private final TaskHistoryRepository taskHistoryRepository;
    private final OrderRepository orderRepository;

    @Override
    public void run(String... args) {
        seedUser("admin@smarttask.com", "Admin", "SmartTask", "+21600000000", Role.ADMIN, "Admin123!");
        User manager = seedUser("manager@smarttask.com", "Karim", "Manager", "+21611111111", Role.MANAGER, "Manager123!");
        User driver1 = seedUser("driver1@smarttask.com", "Mohamed", "Chauffeur", "+21622222222", Role.DRIVER, "Driver123!");
        User driver2 = seedUser("driver2@smarttask.com", "Ali", "Chauffeur", "+21622222223", Role.DRIVER, "Driver123!");
        User operator = seedUser("operator1@smarttask.com", "Sami", "Operateur", "+21633333333", Role.OPERATOR, "Operator123!");
        User client1 = seedUser("client1@smarttask.com", "Ahmed", "Client", "+21644444444", Role.CLIENT, "Client123!");
        User client2 = seedUser("client2@smarttask.com", "Sara", "Client", "+21644444445", Role.CLIENT, "Client123!");

        seedDriverProfile(driver1, DriverStatus.AVAILABLE, "Tunis", 1);
        seedDriverProfile(driver2, DriverStatus.BUSY, "Ariana", 1);

        if (orderRepository.count() == 0) {
            seedCompleteScenario(manager, operator, client1, client2, driver1, driver2);
        } else if (taskRepository.count() == 0) {
            seedSampleTasks(manager, client1, client2, driver1, driver2);
        }
    }

    private void seedCompleteScenario(User manager, User operator, User client1, User client2,
                                      User driver1, User driver2) {
        LocalDate today = LocalDate.now();

        // 1. Commande en attente de vérification (opérateur)
        orderRepository.save(Order.builder()
                .client(client1).operator(operator)
                .products("Pièces détachées auto").quantity(2).amount(BigDecimal.valueOf(150))
                .phone("+21644444444").deliveryAddress("12 Rue de la Liberté, Tunis")
                .scheduledDate(today).scheduledTime(LocalTime.of(14, 0))
                .instructions("Sonner 2 fois").priority(Priority.HIGH)
                .status(OrderStatus.PENDING).build());

        // 2. Commande vérifiée — prête à préparer
        orderRepository.save(Order.builder()
                .client(client2).operator(operator)
                .products("Documents administratifs").quantity(1).amount(BigDecimal.valueOf(25))
                .phone("+21644444445").deliveryAddress("45 Avenue Habib Bourguiba, Ariana")
                .scheduledDate(today).scheduledTime(LocalTime.of(16, 30))
                .priority(Priority.MEDIUM).status(OrderStatus.VERIFIED).build());

        // 3. Commande prête + tâche PREPARED (manager assigne)
        Order order3 = orderRepository.save(Order.builder()
                .client(client1).operator(operator)
                .products("Équipement informatique").quantity(1).amount(BigDecimal.valueOf(890))
                .phone("+21644444444").deliveryAddress("8 Rue Ibn Khaldoun, Ben Arous")
                .scheduledDate(today).scheduledTime(LocalTime.of(17, 0))
                .priority(Priority.CRITICAL).status(OrderStatus.READY).build());

        Task taskPrepared = taskRepository.save(Task.builder()
                .title("Livraison commande #" + order3.getId())
                .description("Équipement informatique").client(client1).createdBy(manager).order(order3)
                .deliveryAddress(order3.getDeliveryAddress()).zone("Ben Arous")
                .scheduledDate(today).deadline(LocalDateTime.now().plusHours(4))
                .priority(Priority.CRITICAL).status(TaskStatus.PREPARED)
                .instructions("Fragile").build());
        order3.setTaskId(taskPrepared.getId());
        orderRepository.save(order3);

        // 4. Mission ASSIGNED pour driver1 (accepter)
        Task taskAssigned = taskRepository.save(Task.builder()
                .title("Livraison express Tunis").client(client2).driver(driver1).createdBy(manager)
                .deliveryAddress("3 Rue de Marseille, Tunis").zone("Tunis")
                .scheduledDate(today).scheduledTime(LocalTime.of(15, 0))
                .deadline(LocalDateTime.now().plusHours(2))
                .priority(Priority.HIGH).status(TaskStatus.ASSIGNED).build());

        // 5. Mission IN_DELIVERY pour client1 (liée à une commande)
        Order orderDelivery = orderRepository.save(Order.builder()
                .client(client1).operator(operator)
                .products("Médicaments").quantity(1).amount(BigDecimal.valueOf(45))
                .phone("+21644444444").deliveryAddress("20 Avenue de Carthage, Tunis")
                .scheduledDate(today).scheduledTime(LocalTime.of(13, 0))
                .priority(Priority.CRITICAL).status(OrderStatus.IN_DELIVERY).build());

        Task taskDelivery = taskRepository.save(Task.builder()
                .title("Livraison médicaments").client(client1).driver(driver1).createdBy(manager)
                .order(orderDelivery).deliveryAddress(orderDelivery.getDeliveryAddress()).zone("Tunis")
                .scheduledDate(today).deadline(LocalDateTime.now().plusHours(1))
                .priority(Priority.CRITICAL).status(TaskStatus.IN_DELIVERY).build());
        orderDelivery.setTaskId(taskDelivery.getId());
        orderRepository.save(orderDelivery);

        // 6. Mission COMPLETED pour client1 — commande DELIVERED à confirmer
        Order orderCompleted = orderRepository.save(Order.builder()
                .client(client1).operator(operator)
                .products("Colis standard").quantity(1).amount(BigDecimal.valueOf(75))
                .phone("+21644444444").deliveryAddress("5 Rue de la République, Tunis")
                .scheduledDate(today.minusDays(1)).scheduledTime(LocalTime.of(10, 0))
                .priority(Priority.MEDIUM).status(OrderStatus.DELIVERED).build());

        Task taskCompleted = taskRepository.save(Task.builder()
                .title("Livraison colis standard").client(client1).driver(driver2).createdBy(manager)
                .order(orderCompleted).deliveryAddress(orderCompleted.getDeliveryAddress()).zone("Tunis")
                .scheduledDate(today.minusDays(1)).deadline(LocalDateTime.now().minusHours(2))
                .priority(Priority.MEDIUM).status(TaskStatus.COMPLETED)
                .deliveredAt(LocalDateTime.now().minusHours(3)).actualMinutes(45).build());
        orderCompleted.setTaskId(taskCompleted.getId());
        orderRepository.save(orderCompleted);

        // 7. Mission retardée driver2
        taskRepository.save(Task.builder()
                .title("Livraison pièces auto").client(client1).driver(driver2).createdBy(manager)
                .deliveryAddress("12 Rue de la Liberté, Tunis").zone("Tunis")
                .scheduledDate(today).deadline(LocalDateTime.now().minusHours(1))
                .priority(Priority.HIGH).status(TaskStatus.DELAYED).build());

        taskHistoryRepository.save(TaskHistory.builder().task(taskPrepared).action("PREPARED")
                .newStatus(TaskStatus.PREPARED).performedBy(operator).build());
        taskHistoryRepository.save(TaskHistory.builder().task(taskAssigned).action("ASSIGNED")
                .newStatus(TaskStatus.ASSIGNED).performedBy(manager).build());
        taskHistoryRepository.save(TaskHistory.builder().task(taskDelivery).action("IN_DELIVERY")
                .newStatus(TaskStatus.IN_DELIVERY).performedBy(driver1).build());
        taskHistoryRepository.save(TaskHistory.builder().task(taskCompleted).action("COMPLETED")
                .newStatus(TaskStatus.COMPLETED).performedBy(driver2).build());

        log.info("Complete test scenario seeded (orders + tasks for all roles)");
        log.info("=== COMPTES DE TEST ===");
        log.info("Operator: operator1@smarttask.com / Operator123!");
        log.info("Driver 1: driver1@smarttask.com / Driver123!");
        log.info("Driver 2: driver2@smarttask.com / Driver123!");
        log.info("Client 1: client1@smarttask.com / Client123!");
        log.info("Client 2: client2@smarttask.com / Client123!");
        log.info("Manager: manager@smarttask.com / Manager123!");
    }

    private User seedUser(String email, String firstName, String lastName, String phone, Role role, String rawPassword) {
        return userRepository.findByEmail(email).orElseGet(() -> {
            User user = User.builder()
                    .firstName(firstName).lastName(lastName).email(email)
                    .password(passwordEncoder.encode(rawPassword)).phone(phone).role(role).active(true).build();
            userRepository.save(user);
            log.info("Default user created: {} / {} ({})", email, rawPassword, role);
            return user;
        });
    }

    private void seedDriverProfile(User driver, DriverStatus status, String zone, int load) {
        driverProfileRepository.findByUserId(driver.getId()).orElseGet(() ->
                driverProfileRepository.save(DriverProfile.builder()
                        .user(driver).status(status).zone(zone).currentLoad(load)
                        .totalDeliveries(15).performanceScore(BigDecimal.valueOf(85)).build()));
    }

    private void seedSampleTasks(User manager, User client1, User client2, User driver1, User driver2) {
        Task t1 = taskRepository.save(Task.builder()
                .title("Livraison pièces auto").description("Livraison urgente")
                .client(client1).driver(driver2).createdBy(manager)
                .deliveryAddress("12 Rue de la Liberté, Tunis").zone("Tunis")
                .scheduledDate(LocalDate.now()).scheduledTime(LocalTime.of(14, 0))
                .deadline(LocalDateTime.now().minusHours(1)).priority(Priority.HIGH)
                .status(TaskStatus.DELAYED).deliveryType("Express").weightQuantity("25 kg").build());

        taskRepository.save(Task.builder()
                .title("Livraison documents").client(client2).createdBy(manager)
                .deliveryAddress("45 Avenue Habib Bourguiba, Ariana").zone("Ariana")
                .scheduledDate(LocalDate.now()).deadline(LocalDateTime.now().plusHours(3))
                .priority(Priority.MEDIUM).status(TaskStatus.PENDING).build());

        taskHistoryRepository.save(TaskHistory.builder().task(t1).action("CREATED")
                .newStatus(TaskStatus.PENDING).performedBy(manager).build());
        log.info("Sample tasks seeded");
    }
}
