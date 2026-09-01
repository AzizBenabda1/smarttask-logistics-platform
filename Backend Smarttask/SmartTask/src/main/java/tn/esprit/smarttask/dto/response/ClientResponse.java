package tn.esprit.smarttask.dto.response;

import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class ClientResponse {
    private Long id;
    private String firstName;
    private String lastName;
    private String email;
    private String phone;
    private long deliveryCount;
}
