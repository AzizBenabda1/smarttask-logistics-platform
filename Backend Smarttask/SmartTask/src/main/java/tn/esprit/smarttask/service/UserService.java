package tn.esprit.smarttask.service;

import lombok.RequiredArgsConstructor;
import org.springframework.data.jpa.domain.Specification;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.util.StringUtils;
import tn.esprit.smarttask.dto.request.PasswordChangeRequest;
import tn.esprit.smarttask.dto.request.RegisterRequest;
import tn.esprit.smarttask.dto.request.UpdateProfileRequest;
import tn.esprit.smarttask.dto.request.UserRequest;
import tn.esprit.smarttask.dto.response.UserResponse;
import tn.esprit.smarttask.entity.Role;
import tn.esprit.smarttask.entity.User;
import tn.esprit.smarttask.exception.EmailAlreadyExistsException;
import tn.esprit.smarttask.exception.InvalidPasswordException;
import tn.esprit.smarttask.exception.UserNotFoundException;
import tn.esprit.smarttask.mapper.UserMapper;
import tn.esprit.smarttask.repository.UserRepository;

import jakarta.persistence.criteria.Predicate;
import java.util.ArrayList;
import java.util.List;

@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;
    private final UserMapper userMapper;
    private final PasswordEncoder passwordEncoder;

    @Transactional(readOnly = true)
    public List<UserResponse> getAllUsers(String search, Role role) {
        Specification<User> spec = buildSearchSpecification(search, role);
        return userRepository.findAll(spec).stream()
                .map(userMapper::toResponse)
                .toList();
    }

    @Transactional(readOnly = true)
    public UserResponse getUserById(Long id) {
        return userMapper.toResponse(findUserById(id));
    }

    @Transactional(readOnly = true)
    public User findUserById(Long id) {
        return userRepository.findById(id)
                .orElseThrow(() -> new UserNotFoundException("User not found with id: " + id));
    }

    @Transactional(readOnly = true)
    public User findUserByEmail(String email) {
        return userRepository.findByEmail(email.toLowerCase().trim())
                .orElseThrow(() -> new UserNotFoundException("User not found with email: " + email));
    }

    @Transactional
    public UserResponse createUser(UserRequest request) {
        if (!StringUtils.hasText(request.getPassword())) {
            throw new InvalidPasswordException("Password is required when creating a user");
        }
        validateEmailUniqueness(request.getEmail(), null);
        String encodedPassword = passwordEncoder.encode(request.getPassword());
        User user = userMapper.fromUserRequest(request, encodedPassword);
        return userMapper.toResponse(userRepository.save(user));
    }

    @Transactional
    public UserResponse registerUser(RegisterRequest request) {
        validateEmailUniqueness(request.getEmail(), null);
        String encodedPassword = passwordEncoder.encode(request.getPassword());
        User user = userMapper.fromRegisterRequest(request, encodedPassword);
        return userMapper.toResponse(userRepository.save(user));
    }

    @Transactional
    public UserResponse updateUser(Long id, UserRequest request) {
        User user = findUserById(id);
        validateEmailUniqueness(request.getEmail(), id);
        String encodedPassword = StringUtils.hasText(request.getPassword())
                ? passwordEncoder.encode(request.getPassword())
                : null;
        userMapper.updateFromUserRequest(user, request, encodedPassword);
        return userMapper.toResponse(userRepository.save(user));
    }

    @Transactional
    public UserResponse updateProfile(User user, UpdateProfileRequest request) {
        userMapper.updateFromProfileRequest(user, request);
        return userMapper.toResponse(userRepository.save(user));
    }

    @Transactional
    public void changePassword(User user, PasswordChangeRequest request) {
        if (!passwordEncoder.matches(request.getCurrentPassword(), user.getPassword())) {
            throw new InvalidPasswordException("Current password is incorrect");
        }
        if (!request.getNewPassword().equals(request.getConfirmPassword())) {
            throw new InvalidPasswordException("New password and confirmation do not match");
        }
        user.setPassword(passwordEncoder.encode(request.getNewPassword()));
        userRepository.save(user);
    }

    @Transactional
    public UserResponse updateStatus(Long id, boolean active) {
        User user = findUserById(id);
        user.setActive(active);
        return userMapper.toResponse(userRepository.save(user));
    }

    @Transactional
    public UserResponse updateRole(Long id, Role role) {
        User user = findUserById(id);
        user.setRole(role);
        return userMapper.toResponse(userRepository.save(user));
    }

    @Transactional
    public void deleteUser(Long id) {
        if (!userRepository.existsById(id)) {
            throw new UserNotFoundException("User not found with id: " + id);
        }
        userRepository.deleteById(id);
    }

    private void validateEmailUniqueness(String email, Long excludeId) {
        String normalizedEmail = email.toLowerCase().trim();
        userRepository.findByEmail(normalizedEmail).ifPresent(existing -> {
            if (excludeId == null || !existing.getId().equals(excludeId)) {
                throw new EmailAlreadyExistsException("Email already exists: " + normalizedEmail);
            }
        });
    }

    private Specification<User> buildSearchSpecification(String search, Role role) {
        return (root, query, cb) -> {
            List<Predicate> predicates = new ArrayList<>();
            if (StringUtils.hasText(search)) {
                String pattern = "%" + search.toLowerCase() + "%";
                predicates.add(cb.or(
                        cb.like(cb.lower(root.get("firstName")), pattern),
                        cb.like(cb.lower(root.get("lastName")), pattern),
                        cb.like(cb.lower(root.get("email")), pattern),
                        cb.like(cb.lower(root.get("phone")), pattern)
                ));
            }
            if (role != null) {
                predicates.add(cb.equal(root.get("role"), role));
            }
            return cb.and(predicates.toArray(new Predicate[0]));
        };
    }
}
