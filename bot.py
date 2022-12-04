from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from resources.models import User, datetime
from constants import API_TOKEN
from app.process import dbconnect

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dbconnect
@dp.message_handler(Text(equals="ТЕСТ"))
async def test_db(message: types.Message, cur):
    res = cur.execute("SELECT * FROM test").fetchall()
    await message.answer(res)


@dbconnect
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message, cur):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["ТЕСТ"]
    keyboard.add(*buttons)
    user = User(tg_user_id=message.from_user.id,
                date_joined=datetime.now(),
                has_table=False)
    res = cur.execute(f"SELECT * FROM users WHERE tg_user_id = '{user.tg_user_id}'").fetchall()
    if not res:
        cur.execute(f"INSERT INTO users(tg_user_id, user_name, date_joined, has_table) "
                    f"VALUES({user.tg_user_id},'{message.from_user.full_name}', '{user.date_joined}', False)")
        await message.answer(f"Добро пожаловать, {message.from_user.full_name}!", reply_markup=keyboard)
    else:
        full_name = res[0][2]
        if message.from_user.full_name != full_name:
            cur.execute(f"UPDATE users SET user_name = '{message.from_user.full_name}'"
                        f"WHERE tg_user_id = {user.tg_user_id}")
        await message.answer(text=f"Добро пожаловать снова, {message.from_user.full_name}!", reply_markup=keyboard)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
