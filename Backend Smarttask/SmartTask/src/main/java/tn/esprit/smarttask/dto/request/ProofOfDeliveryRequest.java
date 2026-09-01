package tn.esprit.smarttask.dto.request;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class ProofOfDeliveryRequest {
    @NotBlank
    @Size(max = 500_000)
    private String imageBase64;
    private String note;
}
