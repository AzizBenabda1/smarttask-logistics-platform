package tn.esprit.smarttask.service;

import lombok.RequiredArgsConstructor;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import tn.esprit.smarttask.dto.request.LoginRequest;
import tn.esprit.smarttask.dto.request.RegisterRequest;
import tn.esprit.smarttask.dto.response.LoginResponse;
import tn.esprit.smarttask.dto.response.UserResponse;
import tn.esprit.smarttask.entity.User;
import tn.esprit.smarttask.exception.AccountDisabledException;
import tn.esprit.smarttask.mapper.UserMapper;
import tn.esprit.smarttask.security.CustomUserDetails;

@Service
@RequiredArgsConstructor
public class AuthService {

    private final AuthenticationManager authenticationManager;
    private final UserService userService;
    private final JwtService jwtService;
    private final UserMapper userMapper;

    @Transactional(readOnly = true)
    public LoginResponse login(LoginRequest request) {
        try {
            Authentication authentication = authenticationManager.authenticate(
                    new UsernamePasswordAuthenticationToken(
                            request.getEmail().toLowerCase().trim(),
                            request.getPassword()
                    )
            );

            CustomUserDetails userDetails = (CustomUserDetails) authentication.getPrincipal();
            User user = userDetails.getUser();

            if (!user.isActive()) {
                throw new AccountDisabledException("Account is disabled");
            }

            String token = jwtService.generateToken(user);
            return LoginResponse.builder()
                    .token(token)
                    .user(userMapper.toResponse(user))
                    .build();
        } catch (BadCredentialsException ex) {
            throw new BadCredentialsException("Invalid email or password");
        }
    }

    @Transactional
    public UserResponse register(RegisterRequest request) {
        return userService.registerUser(request);
    }

    @Transactional(readOnly = true)
    public UserResponse getCurrentUser(User user) {
        return userMapper.toResponse(user);
    }
}
