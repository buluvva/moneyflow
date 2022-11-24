from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
import psycopg as ps
bot = Bot(token='5843791019:AAEYiP_dHfBXTq_bxT_frvPdo1x0OrpXTyg')
dp = Dispatcher(bot)


@dp.message_handler(Text(equals="ТЕСТ"))
async def test_db(message: types.Message):
    conn = ps.connect(dbname="data",
                      user="admin",
                      password="admin",
                      host="192.168.10.100",
                      port="5432")
    cur = conn.cursor()
    conn.commit()
    res = cur.execute("SELECT * FROM test").fetchall()
    conn.commit()
    conn.close()
    await message.answer(res)


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup()
    button_1 = types.KeyboardButton(text="ТЕСТ")
    keyboard.add(button_1)
    await message.answer("Выберите действие", reply_markup=keyboard)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
