package tn.esprit.smarttask.mapper;

import org.springframework.stereotype.Component;
import tn.esprit.smarttask.dto.request.RegisterRequest;
import tn.esprit.smarttask.dto.request.UpdateProfileRequest;
import tn.esprit.smarttask.dto.request.UserRequest;
import tn.esprit.smarttask.dto.response.UserResponse;
import tn.esprit.smarttask.entity.Role;
import tn.esprit.smarttask.entity.User;

@Component
public class UserMapper {

    public UserResponse toResponse(User user) {
        return UserResponse.builder()
                .id(user.getId())
                .firstName(user.getFirstName())
                .lastName(user.getLastName())
                .email(user.getEmail())
                .phone(user.getPhone())
                .role(user.getRole())
                .active(user.isActive())
                .build();
    }

    public User fromRegisterRequest(RegisterRequest request, String encodedPassword) {
        return User.builder()
                .firstName(request.getFirstName())
                .lastName(request.getLastName())
                .email(request.getEmail().toLowerCase().trim())
                .password(encodedPassword)
                .phone(request.getPhone())
                .role(Role.CLIENT)
                .active(true)
                .build();
    }

    public User fromUserRequest(UserRequest request, String encodedPassword) {
        return User.builder()
                .firstName(request.getFirstName())
                .lastName(request.getLastName())
                .email(request.getEmail().toLowerCase().trim())
                .password(encodedPassword)
                .phone(request.getPhone())
                .role(request.getRole())
                .active(request.getActive() != null ? request.getActive() : true)
                .build();
    }

    public void updateFromUserRequest(User user, UserRequest request, String encodedPassword) {
        user.setFirstName(request.getFirstName());
        user.setLastName(request.getLastName());
        user.setEmail(request.getEmail().toLowerCase().trim());
        user.setPhone(request.getPhone());
        user.setRole(request.getRole());
        if (request.getActive() != null) {
            user.setActive(request.getActive());
        }
        if (encodedPassword != null) {
            user.setPassword(encodedPassword);
        }
    }

    public void updateFromProfileRequest(User user, UpdateProfileRequest request) {
        user.setFirstName(request.getFirstName());
        user.setLastName(request.getLastName());
        user.setPhone(request.getPhone());
    }
}
