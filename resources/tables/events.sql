CREATE TABLE events
(
    id BIGSERIAL PRIMARY KEY,
    user_id INT REFERENCES users (id),
    event_type VARCHAR(255),
    cash_value float4,
    category_id INT REFERENCES categories (id),
    event_timestamp VARCHAR(255)
);

select * from events;

