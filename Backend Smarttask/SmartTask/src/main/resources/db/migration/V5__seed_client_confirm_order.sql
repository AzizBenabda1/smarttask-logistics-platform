-- Commande DELIVERED + tâche COMPLETED pour tester la confirmation client (client1)
-- Exécuté seulement si aucune commande DELIVERED n'existe encore pour client1@smarttask.com

DO $$
DECLARE
    v_client_id BIGINT;
    v_operator_id BIGINT;
    v_manager_id BIGINT;
    v_driver_id BIGINT;
    v_order_id BIGINT;
    v_task_id BIGINT;
BEGIN
    SELECT id INTO v_client_id FROM users WHERE email = 'client1@smarttask.com' LIMIT 1;
    SELECT id INTO v_operator_id FROM users WHERE email = 'operator1@smarttask.com' LIMIT 1;
    SELECT id INTO v_manager_id FROM users WHERE email = 'manager@smarttask.com' LIMIT 1;
    SELECT id INTO v_driver_id FROM users WHERE email = 'driver2@smarttask.com' LIMIT 1;

    IF v_client_id IS NULL OR v_operator_id IS NULL OR v_manager_id IS NULL OR v_driver_id IS NULL THEN
        RETURN;
    END IF;

    IF EXISTS (
        SELECT 1 FROM orders o
        JOIN users u ON o.client_id = u.id
        WHERE u.email = 'client1@smarttask.com' AND o.status = 'DELIVERED'
    ) THEN
        RETURN;
    END IF;

    INSERT INTO orders (client_id, operator_id, products, quantity, amount, phone, delivery_address,
                        scheduled_date, scheduled_time, priority, status, created_at, updated_at)
    VALUES (v_client_id, v_operator_id, 'Colis standard', 1, 75, '+21644444444',
            '5 Rue de la République, Tunis', CURRENT_DATE - 1, '10:00:00', 'MEDIUM', 'DELIVERED',
            NOW() - INTERVAL '1 day', NOW())
    RETURNING id INTO v_order_id;

    INSERT INTO tasks (title, description, client_id, driver_id, created_by_id, order_id, delivery_address, zone,
                       scheduled_date, deadline, priority, status, client_confirmed, delivered_at, actual_minutes,
                       created_at, updated_at)
    VALUES ('Livraison colis standard', 'Colis standard', v_client_id, v_driver_id, v_manager_id, v_order_id,
            '5 Rue de la République, Tunis', 'Tunis', CURRENT_DATE - 1, NOW() - INTERVAL '2 hours',
            'MEDIUM', 'COMPLETED', false, NOW() - INTERVAL '3 hours', 45, NOW() - INTERVAL '1 day', NOW())
    RETURNING id INTO v_task_id;

    UPDATE orders SET task_id = v_task_id WHERE id = v_order_id;
END $$;
