package tn.esprit.smarttask.dto.request;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class ChatSendRequest {

    @NotBlank
    @Size(max = 2000)
    private String message;

    private String sessionId;
}
