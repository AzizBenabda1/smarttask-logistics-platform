-- Tasks & logistics module
CREATE TABLE driver_profiles (
    id              BIGSERIAL PRIMARY KEY,
    user_id         BIGINT NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    status          VARCHAR(20) NOT NULL DEFAULT 'AVAILABLE',
    zone            VARCHAR(100),
    current_load    INT NOT NULL DEFAULT 0,
    total_deliveries INT NOT NULL DEFAULT 0,
    performance_score DECIMAL(5,2) NOT NULL DEFAULT 80.00,
    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_driver_status CHECK (status IN ('AVAILABLE', 'BUSY', 'UNAVAILABLE', 'OFFLINE'))
);

CREATE TABLE tasks (
    id                  BIGSERIAL PRIMARY KEY,
    title               VARCHAR(200) NOT NULL,
    description         TEXT,
    client_id           BIGINT NOT NULL REFERENCES users(id),
    driver_id           BIGINT REFERENCES users(id),
    created_by_id       BIGINT NOT NULL REFERENCES users(id),
    delivery_address    VARCHAR(500) NOT NULL,
    zone                VARCHAR(100),
    scheduled_date      DATE,
    scheduled_time      TIME,
    deadline            TIMESTAMP NOT NULL,
    priority            VARCHAR(20) NOT NULL DEFAULT 'MEDIUM',
    status              VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    delivery_type       VARCHAR(50),
    weight_quantity     VARCHAR(100),
    instructions        TEXT,
    estimated_minutes   INT,
    actual_minutes      INT,
    latitude            DECIMAL(10,7),
    longitude           DECIMAL(10,7),
    created_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_task_priority CHECK (priority IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')),
    CONSTRAINT chk_task_status CHECK (status IN ('PENDING', 'ASSIGNED', 'IN_PROGRESS', 'IN_DELIVERY', 'COMPLETED', 'CANCELLED', 'DELAYED'))
);

CREATE TABLE task_history (
    id              BIGSERIAL PRIMARY KEY,
    task_id         BIGINT NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    action          VARCHAR(100) NOT NULL,
    old_status      VARCHAR(20),
    new_status      VARCHAR(20),
    performed_by_id BIGINT REFERENCES users(id),
    notes           TEXT,
    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE notifications (
    id              BIGSERIAL PRIMARY KEY,
    user_id         BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type            VARCHAR(50) NOT NULL,
    title           VARCHAR(200) NOT NULL,
    message         TEXT NOT NULL,
    priority        VARCHAR(20) NOT NULL DEFAULT 'MEDIUM',
    read_flag       BOOLEAN NOT NULL DEFAULT FALSE,
    related_task_id BIGINT REFERENCES tasks(id) ON DELETE SET NULL,
    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_notification_priority CHECK (priority IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL'))
);

CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_priority ON tasks(priority);
CREATE INDEX idx_tasks_driver ON tasks(driver_id);
CREATE INDEX idx_tasks_client ON tasks(client_id);
CREATE INDEX idx_tasks_deadline ON tasks(deadline);
CREATE INDEX idx_task_history_task ON task_history(task_id);
CREATE INDEX idx_notifications_user ON notifications(user_id);
