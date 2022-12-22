from resources.models import datetime
import psycopg as ps
from app.utils.validators import user_check, category_check
from app.resources.exceptions import WrongValue
from settings import settings


def dbconnect(func):
    def wrapper(*args):
        conn = ps.connect(dbname="data",
                          user=settings.POSTGRES_LOGIN,
                          password=settings.POSTGRES_PASSWORD,
                          host=settings.POSTGRES_PATH,
                          port="5432")
        cur = conn.cursor()

        try:
            return_value = func(*args, cur)
            conn.commit()
            conn.close()
        except Exception as s:
            conn.rollback()
            conn.close()
            raise s
        return return_value
    return wrapper


@dbconnect
def insert_event(user_id, event_type, category_id, cash_value, cur):
    # check values
    user_check(user_id)
    category_check(category_id)
    if isinstance(cash_value, float) is False:
        raise WrongValue

    cur.execute(f"INSERT INTO events(user_id, event_type, cash_value, category_id, event_timestamp) "
                f"VALUES ('{user_id}','{event_type}', {cash_value}, '{category_id}', '{datetime.now()}')")
