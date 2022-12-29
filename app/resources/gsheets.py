import pygsheets as pg
import pandas as pd
from app.utils.validators import dbconnect, user_check
from datetime import datetime


scope = ["https://spreadsheets.google.com/feeds",
         'https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive.file',
         'https://www.googleapis.com/auth/drive']
c = pg.authorize(client_secret='client_secret.json',
                 service_account_file='service_file_bot.json',
                 service_account_env_var=None,
                 credentials_directory=None,
                 scopes=scope,
                 custom_credentials=None,
                 local=False)


def grabber(url):
    return sheet_grabber(url).get_as_df(index_colum=1)


def sheet_grabber(url):
    sheet = c.open_by_url(url)
    return sheet.sheet1


@dbconnect
def check_table(user_id, cur):
    user_check(user_id)
    has_table = cur.execute(f"SELECT has_table FROM users WHERE tg_user_id = {user_id}").fetchall()
    if has_table:
        link = cur.execute(f"SELECT table_link FROM user_tables WHERE user_id = {user_id}").fetchall()
        print(link)
        return grabber(link[0][0])
    else:
        table_url = create_table(user_id)
        cur.execute(f"INSERT INTO user_tables(user_id, table_link) VALUES ('{user_id}', '{table_url}')")
        cur.execute(f"UPDATE users SET has_table = True WHERE tg_user_id = {user_id}")
        return grabber(table_url)


def create_table(user_id):
    sheet = c.create(title=f'{user_id}')
    df = pd.read_csv('./app/resources/schema.csv')
    sheet.sheet1.set_dataframe(df, (1, 1), encoding='utf-8', fit=True)
    return sheet.url


@dbconnect
def add_spend(user_id, category, value, cur):
    link = cur.execute(f"SELECT table_link FROM user_tables WHERE user_id = {user_id}").fetchone()
    df = grabber(link[0])
    day = datetime.now().day
    df.loc[category, day] += value
    df.loc[category, 'Расх. за мес.'] += value
    df.loc['Баланс','Расх. за мес.'] -= value
    sheet_grabber(link[0]).set_dataframe(df, 'B1', encoding='utf-8')
    return grabber(link[0])


@dbconnect
def add_income(user_id, value, cur):
    link = cur.execute(f"SELECT table_link FROM user_tables WHERE user_id = {user_id}").fetchone()
    df = grabber(link[0])
    df.loc['Баланс', 'Расх. за мес.'] += value
    sheet_grabber(link[0]).set_dataframe(df, 'B1', encoding='utf-8')
    return grabber(link[0])


@dbconnect
def grab_balance(user_id, cur):
    link = cur.execute(f"SELECT table_link FROM user_tables WHERE user_id = {user_id}").fetchone()
    df = grabber(link[0])
    return df.loc['Баланс', 'Расх. за мес.']


@dbconnect
def grab_buttons(cur):
    res = []
    cats = cur.execute(f"SELECT * FROM categories").fetchall()
    for cat in cats:
        res.append(cat[1])
    return res

