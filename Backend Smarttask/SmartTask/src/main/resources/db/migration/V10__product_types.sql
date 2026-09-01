CREATE TABLE product_types (
    id          BIGSERIAL PRIMARY KEY,
    code        VARCHAR(50) NOT NULL UNIQUE,
    name        VARCHAR(150) NOT NULL,
    description TEXT,
    active      BOOLEAN NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO product_types (code, name, description) VALUES
('DOCUMENTS', 'Documents & courrier', 'Enveloppes, dossiers, courrier administratif'),
('COLIS_STANDARD', 'Colis standard', 'Cartons et colis courants'),
('COLIS_FRAGILE', 'Colis fragile', 'Produits fragiles'),
('MEDICAMENTS', 'Médicaments', 'Produits pharmaceutiques'),
('EQUIPEMENT', 'Équipement lourd', 'Matériel informatique ou industriel'),
('ALIMENTAIRE', 'Produits alimentaires', 'Denrées alimentaires et produits frais');

ALTER TABLE orders ADD COLUMN IF NOT EXISTS product_type_id BIGINT REFERENCES product_types(id);
CREATE INDEX IF NOT EXISTS idx_orders_product_type ON orders(product_type_id);

UPDATE orders
SET product_type_id = (SELECT id FROM product_types WHERE code = 'COLIS_STANDARD')
WHERE product_type_id IS NULL AND products IS NOT NULL;
