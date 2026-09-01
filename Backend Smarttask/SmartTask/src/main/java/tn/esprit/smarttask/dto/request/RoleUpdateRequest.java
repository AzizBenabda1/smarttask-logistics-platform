package tn.esprit.smarttask.dto.request;

import jakarta.validation.constraints.NotNull;
import lombok.Getter;
import lombok.Setter;
import tn.esprit.smarttask.entity.Role;

@Getter
@Setter
public class RoleUpdateRequest {

    @NotNull(message = "Role is required")
    private Role role;
}
