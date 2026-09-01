package tn.esprit.smarttask.dto.response;

import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class ProductTypeResponse {
    private Long id;
    private String code;
    private String name;
    private String description;
}
