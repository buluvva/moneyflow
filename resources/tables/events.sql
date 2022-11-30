CREATE TABLE events
(
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    user_id INT REFERENCES users (id),
    event_type VARCHAR(255),
    cash_value float4,
    category_id INT REFERENCES categories (id),
    timestamp VARCHAR(255)
);

