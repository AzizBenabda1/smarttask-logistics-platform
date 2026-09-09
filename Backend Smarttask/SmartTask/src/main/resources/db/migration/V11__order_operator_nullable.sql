-- Client-created orders have no operator until verification
ALTER TABLE orders ALTER COLUMN operator_id DROP NOT NULL;
