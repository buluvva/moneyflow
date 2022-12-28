CREATE TABLE IF NOT EXISTS users
(
    id BIGSERIAL PRIMARY KEY,
    tg_user_id int UNIQUE,
    user_name varchar(255),
    date_joined varchar(255),
    has_table bool
);

UPDATE users SET has_table = False WHERE tg_user_id = 258016847;
select * from users;

