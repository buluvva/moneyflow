from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from resources.models import User, datetime
import psycopg as ps
bot = Bot(token='5843791019:AAEYiP_dHfBXTq_bxT_frvPdo1x0OrpXTyg')
dp = Dispatcher(bot)


@dp.message_handler(Text(equals="ТЕСТ"))
async def test_db(message: types.Message):
    conn = ps.connect(dbname="data",
                      user="admin",
                      password="admin",
                      host="0.0.0.0",
                      port="5432")
    cur = conn.cursor()
    res = cur.execute("SELECT * FROM test").fetchall()
    conn.commit()
    conn.close()
    await message.answer(res)


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["ТЕСТ"]
    keyboard.add(*buttons)
    user = User(tg_user_id=message.from_user.id,
                date_joined=datetime.now(),
                has_table=False)
    conn = ps.connect(dbname="data",
                      user="admin",
                      password="admin",
                      host="0.0.0.0",
                      port="5432")
    cur = conn.cursor()
    res = cur.execute(f"SELECT * FROM users WHERE tg_user_id = '{user.tg_user_id}'").fetchall()
    full_name = res[0][2]
    if not res:
        cur.execute(f"INSERT INTO users(tg_user_id, user_name, date_joined, has_table) "
                    f"VALUES({user.tg_user_id},'{message.from_user.full_name}', '{user.date_joined}', False)")
        conn.commit()
        res = cur.execute(f"SELECT * FROM users WHERE tg_user_id = '{user.tg_user_id}'").fetchall()
        conn.close()
        await message.answer(f"Добро пожаловать, {message.from_user.full_name}!", reply_markup=keyboard)
    elif message.from_user.full_name != full_name:
        cur.execute(f"UPDATE users SET user_name = '{message.from_user.full_name}'"
                    f"WHERE tg_user_id = {user.tg_user_id}")
        conn.commit()
        conn.close()
        await message.answer(text=f"Добро пожаловать снова, {message.from_user.full_name}!", reply_markup=keyboard)
    else:
        conn.close()
        await message.answer(text=f"Добро пожаловать снова, {message.from_user.full_name}!", reply_markup=keyboard)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
