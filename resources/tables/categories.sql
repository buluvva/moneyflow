CREATE TABLE categories
(
    id BIGSERIAL PRIMARY KEY,
    category_name VARCHAR(255),
    category_group INT REFERENCES category_groups (id)
);