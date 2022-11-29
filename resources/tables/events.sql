CREATE TABLE events
(
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    user_id INT REFERENCES users (id),
    type VARCHAR(255),
    category_id INT REFERENCES categories (id),
    timestamp VARCHAR(255)
);