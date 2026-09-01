-- Orders, incidents, reviews + extended task workflow

ALTER TABLE tasks DROP CONSTRAINT IF EXISTS chk_task_status;
ALTER TABLE tasks ADD CONSTRAINT chk_task_status CHECK (status IN (
    'PENDING', 'PREPARED', 'ASSIGNED', 'ACCEPTED', 'IN_PROGRESS', 'IN_DELIVERY',
    'COMPLETED', 'CANCELLED', 'DELAYED'
));

CREATE TABLE orders (
    id                  BIGSERIAL PRIMARY KEY,
    client_id           BIGINT NOT NULL REFERENCES users(id),
    operator_id         BIGINT NOT NULL REFERENCES users(id),
    products            TEXT NOT NULL,
    quantity            INT NOT NULL DEFAULT 1,
    amount              DECIMAL(12,2) NOT NULL DEFAULT 0,
    phone               VARCHAR(20),
    delivery_address    VARCHAR(500) NOT NULL,
    scheduled_date      DATE,
    scheduled_time      TIME,
    instructions        TEXT,
    priority            VARCHAR(20) NOT NULL DEFAULT 'MEDIUM',
    status              VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    task_id             BIGINT,
    created_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_order_priority CHECK (priority IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')),
    CONSTRAINT chk_order_status CHECK (status IN ('PENDING', 'VERIFIED', 'PREPARING', 'READY', 'IN_DELIVERY', 'DELIVERED', 'CANCELLED'))
);

ALTER TABLE tasks ADD COLUMN IF NOT EXISTS order_id BIGINT REFERENCES orders(id) ON DELETE SET NULL;
ALTER TABLE tasks ADD COLUMN IF NOT EXISTS client_confirmed BOOLEAN NOT NULL DEFAULT FALSE;
ALTER TABLE tasks ADD COLUMN IF NOT EXISTS client_received_comment TEXT;
ALTER TABLE tasks ADD COLUMN IF NOT EXISTS delivered_at TIMESTAMP;

ALTER TABLE orders ADD CONSTRAINT fk_orders_task FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE SET NULL;

CREATE TABLE incidents (
    id              BIGSERIAL PRIMARY KEY,
    reporter_id     BIGINT NOT NULL REFERENCES users(id),
    task_id         BIGINT REFERENCES tasks(id) ON DELETE SET NULL,
    order_id        BIGINT REFERENCES orders(id) ON DELETE SET NULL,
    type            VARCHAR(50) NOT NULL,
    description     TEXT NOT NULL,
    priority        VARCHAR(20) NOT NULL DEFAULT 'MEDIUM',
    status          VARCHAR(20) NOT NULL DEFAULT 'OPEN',
    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_incident_priority CHECK (priority IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')),
    CONSTRAINT chk_incident_status CHECK (status IN ('OPEN', 'IN_PROGRESS', 'RESOLVED', 'CLOSED'))
);

CREATE TABLE reviews (
    id              BIGSERIAL PRIMARY KEY,
    client_id       BIGINT NOT NULL REFERENCES users(id),
    task_id         BIGINT NOT NULL UNIQUE REFERENCES tasks(id) ON DELETE CASCADE,
    rating          INT NOT NULL,
    comment         TEXT,
    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_review_rating CHECK (rating BETWEEN 1 AND 5)
);

CREATE INDEX idx_orders_client ON orders(client_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_operator ON orders(operator_id);
CREATE INDEX idx_incidents_reporter ON incidents(reporter_id);
CREATE INDEX idx_reviews_client ON reviews(client_id);
