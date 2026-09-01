package tn.esprit.smarttask.controller;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import tn.esprit.smarttask.dto.response.ProductTypeResponse;
import tn.esprit.smarttask.service.ProductTypeService;

import java.util.List;

@RestController
@RequestMapping("/api/product-types")
@RequiredArgsConstructor
@Tag(name = "Product Types", description = "Types de produits livrables SmartTask")
@SecurityRequirement(name = "Bearer Authentication")
public class ProductTypeController {

    private final ProductTypeService productTypeService;

    @GetMapping
    @Operation(summary = "Liste des types de produits actifs")
    public ResponseEntity<List<ProductTypeResponse>> list() {
        return ResponseEntity.ok(productTypeService.listActive());
    }
}
