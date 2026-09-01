package tn.esprit.smarttask.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
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
import tn.esprit.smarttask.dto.request.TaskIdRequest;
import tn.esprit.smarttask.entity.Role;
import tn.esprit.smarttask.entity.Task;
import tn.esprit.smarttask.entity.User;
import tn.esprit.smarttask.repository.TaskRepository;
import tn.esprit.smarttask.repository.UserRepository;

import java.time.LocalDateTime;

import static org.springframework.security.test.web.servlet.setup.SecurityMockMvcConfigurers.springSecurity;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@ActiveProfiles("test")
@Transactional
class ManagerAIControllerTest {

    private MockMvc mockMvc;

    @Autowired
    private WebApplicationContext context;

    private final ObjectMapper objectMapper = new ObjectMapper();

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private TaskRepository taskRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    private String managerToken;
    private String clientToken;

    @BeforeEach
    void setUp() throws Exception {
        mockMvc = MockMvcBuilders.webAppContextSetup(context)
                .apply(springSecurity())
                .build();

        userRepository.deleteAll();
        seedUser("manager@test.com", Role.MANAGER, "Manager123!");
        seedUser("client@test.com", Role.CLIENT, "Client123!");

        managerToken = login("manager@test.com", "Manager123!");
        clientToken = login("client@test.com", "Client123!");
    }

    @Test
    void predictDelayReturns503WhenAiDisabled() throws Exception {
        User client = userRepository.findByEmail("client@test.com").orElseThrow();
        User manager = userRepository.findByEmail("manager@test.com").orElseThrow();
        Task task = taskRepository.save(Task.builder()
                .title("AI test task")
                .client(client)
                .createdBy(manager)
                .deliveryAddress("1 Rue Test, Tunis")
                .deadline(LocalDateTime.now().plusHours(2))
                .build());

        TaskIdRequest request = new TaskIdRequest();
        request.setTaskId(task.getId());

        mockMvc.perform(post("/api/manager/ai/predict-delay")
                        .header("Authorization", "Bearer " + managerToken)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isServiceUnavailable())
                .andExpect(jsonPath("$.message").exists());
    }

    @Test
    void clientCannotAccessAiPredictDelay() throws Exception {
        TaskIdRequest request = new TaskIdRequest();
        request.setTaskId(1L);

        mockMvc.perform(post("/api/manager/ai/predict-delay")
                        .header("Authorization", "Bearer " + clientToken)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isForbidden());
    }

    private void seedUser(String email, Role role, String password) {
        userRepository.save(User.builder()
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
