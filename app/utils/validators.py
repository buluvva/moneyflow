from app.resources.exceptions import UserNotFound, CategoryNotFound
import psycopg as ps
from app.process import dbconnect


@dbconnect
def user_check(user_id, cur):
    user = cur.execute(f"SELECT tg_user_id FROM users WHERE tg_user_id = {user_id}").fetchall()
    if not user:
        raise UserNotFound


@dbconnect
def category_check(category_id, cur):
    cat_check = cur.execute(f"SELECT * FROM categories WHERE id = '{category_id}'").fetchall()
    if not cat_check:
        raise CategoryNotFound
