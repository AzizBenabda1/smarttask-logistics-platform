package tn.esprit.smarttask.service;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;
import tn.esprit.smarttask.dto.request.OrderRequest;
import tn.esprit.smarttask.entity.ProductType;
import tn.esprit.smarttask.exception.InvalidStateTransitionException;

@Component
@RequiredArgsConstructor
public class OrderProductHelper {

    private final ProductTypeService productTypeService;

    public ResolvedProduct resolveProduct(OrderRequest request) {
        if (request.getProductTypeId() != null) {
            ProductType type = productTypeService.getActiveById(request.getProductTypeId());
            String label = type.getName();
            if (request.getProducts() != null && !request.getProducts().isBlank()) {
                label = label + " — " + request.getProducts().trim();
            }
            return new ResolvedProduct(type, label);
        }
        if (request.getCustomProductType() == null || request.getCustomProductType().isBlank()) {
            throw new InvalidStateTransitionException("Choisissez un type de produit ou saisissez un type « Autre »");
        }
        String label = request.getCustomProductType().trim();
        if (request.getProducts() != null && !request.getProducts().isBlank()) {
            label = label + " — " + request.getProducts().trim();
        }
        return new ResolvedProduct(null, label);
    }

    public record ResolvedProduct(ProductType productType, String label) {}
}
