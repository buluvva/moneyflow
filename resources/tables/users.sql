CREATE TABLE IF NOT EXISTS users(id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                                      tg_user_id int,
                                      user_name varchar(255),
                                      date_joined varchar(255),
                                      has_table bool);



