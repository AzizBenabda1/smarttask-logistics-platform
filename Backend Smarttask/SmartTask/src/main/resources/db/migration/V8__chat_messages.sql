CREATE TABLE chat_messages (
    id          BIGSERIAL PRIMARY KEY,
    user_id     BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role        VARCHAR(20) NOT NULL,
    content     TEXT NOT NULL,
    intent      VARCHAR(50),
    session_id  VARCHAR(64) NOT NULL,
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_chat_role CHECK (role IN ('USER', 'ASSISTANT'))
);

CREATE INDEX idx_chat_messages_user_session ON chat_messages (user_id, session_id, created_at);
