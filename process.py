from aiogram import Bot, Dispatcher, executor

bot = Bot(token='5843791019:AAEYiP_dHfBXTq_bxT_frvPdo1x0OrpXTyg')
dp = Dispatcher(bot)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

