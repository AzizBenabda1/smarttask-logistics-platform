package tn.esprit.smarttask.service;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import tn.esprit.smarttask.dto.response.ProductTypeResponse;
import tn.esprit.smarttask.entity.ProductType;
import tn.esprit.smarttask.exception.ProductTypeNotFoundException;
import tn.esprit.smarttask.repository.ProductTypeRepository;

import java.util.List;

@Service
@RequiredArgsConstructor
public class ProductTypeService {

    private final ProductTypeRepository productTypeRepository;

    @Transactional(readOnly = true)
    public List<ProductTypeResponse> listActive() {
        return productTypeRepository.findByActiveTrueOrderByNameAsc().stream()
                .map(this::toResponse).toList();
    }

    @Transactional(readOnly = true)
    public ProductType getActiveById(Long id) {
        ProductType type = productTypeRepository.findById(id)
                .orElseThrow(() -> new ProductTypeNotFoundException("Type de produit introuvable: " + id));
        if (!type.isActive()) {
            throw new ProductTypeNotFoundException("Type de produit inactif: " + id);
        }
        return type;
    }

    private ProductTypeResponse toResponse(ProductType type) {
        return ProductTypeResponse.builder()
                .id(type.getId())
                .code(type.getCode())
                .name(type.getName())
                .description(type.getDescription())
                .build();
    }
}
