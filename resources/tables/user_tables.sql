CREATE TABLE user_tables
(
    id BIGSERIAL PRIMARY KEY ,
    user_id INT REFERENCES users (tg_user_id),
    table_link varchar(255)
);

drop table user_tables;

select * from user_tables;