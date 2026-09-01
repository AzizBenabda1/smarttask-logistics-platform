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
import tn.esprit.smarttask.entity.Role;
import tn.esprit.smarttask.entity.User;
import tn.esprit.smarttask.repository.UserRepository;

import static org.springframework.security.test.web.servlet.setup.SecurityMockMvcConfigurers.springSecurity;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@ActiveProfiles("test")
@Transactional
class ManagerSecurityTest {

    private MockMvc mockMvc;

    @Autowired
    private WebApplicationContext context;

    private final ObjectMapper objectMapper = new ObjectMapper();

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    private String managerToken;
    private String clientToken;
    private String driverToken;

    @BeforeEach
    void setUp() throws Exception {
        mockMvc = MockMvcBuilders.webAppContextSetup(context)
                .apply(springSecurity())
                .build();

        userRepository.deleteAll();
        seedUser("manager@test.com", Role.MANAGER, "Manager123!");
        seedUser("client@test.com", Role.CLIENT, "Client123!");
        seedUser("driver@test.com", Role.DRIVER, "Driver123!");

        managerToken = login("manager@test.com", "Manager123!");
        clientToken = login("client@test.com", "Client123!");
        driverToken = login("driver@test.com", "Driver123!");
    }

    @Test
    void managerCanAccessDashboard() throws Exception {
        mockMvc.perform(get("/api/manager/dashboard")
                        .header("Authorization", "Bearer " + managerToken))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.totalDrivers").value(1));
    }

    @Test
    void clientCannotAccessManagerDashboard() throws Exception {
        mockMvc.perform(get("/api/manager/dashboard")
                        .header("Authorization", "Bearer " + clientToken))
                .andExpect(status().isForbidden());
    }

    @Test
    void driverCannotAccessManagerDashboard() throws Exception {
        mockMvc.perform(get("/api/manager/dashboard")
                        .header("Authorization", "Bearer " + driverToken))
                .andExpect(status().isForbidden());
    }

    @Test
    void unauthenticatedCannotAccessManagerDashboard() throws Exception {
        mockMvc.perform(get("/api/manager/dashboard"))
                .andExpect(status().isUnauthorized());
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
