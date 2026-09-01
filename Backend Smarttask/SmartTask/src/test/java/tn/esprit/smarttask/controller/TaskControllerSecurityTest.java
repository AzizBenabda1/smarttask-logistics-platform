package tn.esprit.smarttask.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.context.WebApplicationContext;
import tn.esprit.smarttask.dto.request.LoginRequest;
import tn.esprit.smarttask.dto.request.TaskRequest;
import tn.esprit.smarttask.entity.Priority;
import tn.esprit.smarttask.entity.Role;
import tn.esprit.smarttask.entity.User;
import tn.esprit.smarttask.repository.UserRepository;

import java.time.LocalDateTime;

import static org.springframework.security.test.web.servlet.setup.SecurityMockMvcConfigurers.springSecurity;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@ActiveProfiles("test")
@Transactional
class TaskControllerSecurityTest {

    private MockMvc mockMvc;

    @Autowired
    private WebApplicationContext context;

    private final ObjectMapper objectMapper = new ObjectMapper().registerModule(new JavaTimeModule());

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    private String managerToken;
    private String clientToken;
    private Long clientId;
    private Long driverId;

    @BeforeEach
    void setUp() throws Exception {
        mockMvc = MockMvcBuilders.webAppContextSetup(context)
                .apply(springSecurity())
                .build();

        userRepository.deleteAll();
        seedUser("manager@test.com", Role.MANAGER, "Manager123!");
        clientId = seedUser("client@test.com", Role.CLIENT, "Client123!").getId();
        driverId = seedUser("driver@test.com", Role.DRIVER, "Driver123!").getId();

        managerToken = login("manager@test.com", "Manager123!");
        clientToken = login("client@test.com", "Client123!");
    }

    @Test
    void managerCanCreateTask() throws Exception {
        TaskRequest request = new TaskRequest();
        request.setTitle("Test delivery");
        request.setClientId(clientId);
        request.setDeliveryAddress("1 Test Street");
        request.setDeadline(LocalDateTime.now().plusDays(1));
        request.setPriority(Priority.MEDIUM);

        mockMvc.perform(post("/api/tasks")
                        .header("Authorization", "Bearer " + managerToken)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.title").value("Test delivery"));
    }

    @Test
    void clientCannotAccessTasks() throws Exception {
        mockMvc.perform(get("/api/tasks")
                        .header("Authorization", "Bearer " + clientToken))
                .andExpect(status().isForbidden());
    }

    @Test
    void managerCanAssignDriver() throws Exception {
        TaskRequest request = new TaskRequest();
        request.setTitle("Assign test");
        request.setClientId(clientId);
        request.setDeliveryAddress("2 Test Street");
        request.setDeadline(LocalDateTime.now().plusDays(1));
        request.setPriority(Priority.HIGH);

        String createResponse = mockMvc.perform(post("/api/tasks")
                        .header("Authorization", "Bearer " + managerToken)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isCreated())
                .andReturn().getResponse().getContentAsString();

        Long taskId = objectMapper.readTree(createResponse).get("id").asLong();

        mockMvc.perform(post("/api/tasks/" + taskId + "/assign/" + driverId)
                        .header("Authorization", "Bearer " + managerToken))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.driverId").value(driverId));
    }

    private User seedUser(String email, Role role, String password) {
        return userRepository.save(User.builder()
                .firstName("Test")
                .lastName(role.name())
                .email(email)
                .password(passwordEncoder.encode(password))
                .role(role)
                .active(true)
                .build());
    }

    private String login(String email, String password) throws Exception {
        LoginRequest request = new LoginRequest();
        request.setEmail(email);
        request.setPassword(password);

        String response = mockMvc.perform(post("/api/auth/login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isOk())
                .andReturn()
                .getResponse()
                .getContentAsString();

        return objectMapper.readTree(response).get("token").asText();
    }
}
