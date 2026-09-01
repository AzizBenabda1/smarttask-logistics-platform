package tn.esprit.smarttask.dto.request;

import jakarta.validation.constraints.*;
import lombok.Getter;
import lombok.Setter;
import tn.esprit.smarttask.entity.Priority;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalTime;

@Getter
@Setter
public class OrderRequest {

    @NotNull
    private Long clientId;

    /** Type choisi dans la liste (null si « Autre ») */
    private Long productTypeId;

    /** Nom du type si « Autre » — obligatoire quand productTypeId est null */
    @Size(max = 150)
    private String customProductType;

    /** Détails complémentaires (optionnel) */
    @Size(max = 500)
    private String products;

    @Min(1)
    private int quantity = 1;

    @NotNull
    @DecimalMin("0.0")
    private BigDecimal amount;

    @Pattern(regexp = "^\\+?[0-9\\s-]{8,20}$", message = "Invalid phone number")
    private String phone;

    @NotBlank
    @Size(max = 500)
    private String deliveryAddress;

    private LocalDate scheduledDate;
    private LocalTime scheduledTime;
    private String instructions;

    @NotNull
    private Priority priority;
}
