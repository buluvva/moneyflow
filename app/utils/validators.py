from app.resources.exceptions import UserNotFound, CategoryNotFound, WrongValue
import psycopg as ps


conn = ps.connect(dbname="data",
                  user="admin",
                  password="admin",
                  host="0.0.0.0",
                  port="5432")
cur = conn.cursor()


def user_check(user_id):
    user = cur.execute(f"SELECT tg_user_id FROM users WHERE tg_user_id = {user_id}").fetchall()
    if not user:
        raise UserNotFound


def category_check(category_id):
    cat_check = cur.execute(f"SELECT * FROM categories WHERE id = '{category_id}'").fetchall()
    if not cat_check:
        raise CategoryNotFound


def value_check(cash_value):
    if type(cash_value) != float:
        raise WrongValue
