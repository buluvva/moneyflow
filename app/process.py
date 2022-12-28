from resources.models import datetime
from app.utils.validators import user_check, category_check, dbconnect
from app.resources.exceptions import WrongValue


@dbconnect
def insert_event(user_id, event_type, category_id, cash_value, cur):
    # check values
    user_check(user_id)
    category_check(category_id)
    if isinstance(cash_value, float) is False:
        raise WrongValue

    cur.execute(f"INSERT INTO events(user_id, event_type, cash_value, category_id, event_timestamp) "
                f"VALUES ('{user_id}','{event_type}', {cash_value}, '{category_id}', '{datetime.now()}')")


@dbconnect
def insert_category_group(cur, cat_group):
    check = cur.execute(f"SELECT * FROM category_groups WHERE group_name = {cat_group}").fetchall()
    if check:
        return "Группа уже существует"
    else:
        cur.execute(f"INSERT INTO category_groups(group_name) VALUES ('{cat_group}')")
        return "Группа добавлена"


@dbconnect
def insert_category(cur, cat, group):
    check = cur.execute(f"SELECT * FROM categories WHERE group_name = {cat} AND category_group = {group}").fetchall()
    if check:
        return "Категория уже существует"
    else:
        cur.execute(f"INSERT INTO categories(category_name, category_group) VALUES ('{cat}', {group})")
        return "Категория добавлена"


@dbconnect
def insert_user(id, name, date_joined, cur):
    res = cur.execute(f"SELECT * FROM users WHERE tg_user_id = '{id}'").fetchall()
    if not res:
        cur.execute(f"INSERT INTO users(tg_user_id, user_name, date_joined, has_table) "
                    f"VALUES({id},'{name}', '{date_joined}', False)")
        return f"Добро пожаловать, {name}!"
    else:
        full_name = res[0][2]
        if name != full_name:
            cur.execute(f"UPDATE users SET user_name = '{name}'"
                        f"WHERE tg_user_id = {id}")
        return f"Добро пожаловать снова, {name}!"


@dbconnect
def show_events(cur):
    res = cur.execute(f"SELECT * FROM events").fetchall()
    return res




