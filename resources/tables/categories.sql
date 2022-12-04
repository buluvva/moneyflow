CREATE TABLE categories
(
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    category_name VARCHAR(255)
    category_group INT references category_frops (id)
)