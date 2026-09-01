CREATE TABLE automation_logs (
    id          BIGSERIAL PRIMARY KEY,
    run_id      VARCHAR(64) NOT NULL,
    chain_type  VARCHAR(50) NOT NULL,
    order_id    BIGINT REFERENCES orders(id) ON DELETE SET NULL,
    task_id     BIGINT REFERENCES tasks(id) ON DELETE SET NULL,
    step_number INT NOT NULL,
    step_name   VARCHAR(100) NOT NULL,
    status      VARCHAR(20) NOT NULL,
    message     TEXT NOT NULL,
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_automation_status CHECK (status IN ('SUCCESS', 'SKIPPED', 'FAILED'))
);

CREATE INDEX idx_automation_logs_run ON automation_logs (run_id, step_number);
CREATE INDEX idx_automation_logs_order ON automation_logs (order_id, created_at DESC);
