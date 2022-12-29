from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from resources.models import User, datetime
from constants import API_TOKEN
from app.process import insert_user, show_events
from aiogram.dispatcher import FSMContext
from resources.models import Bills
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from app.resources.gsheets import grab_buttons, grab_balance, add_spend

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
buttons = grab_buttons()


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Выбор категории расхода", "Узнать баланс", "Пополнить баланс"]
    keyboard.add(*buttons)
    user = User(tg_user_id=message.from_user.id,
                date_joined=datetime.now(),
                has_table=False)
    res = insert_user(user.tg_user_id, message.from_user.full_name, user.date_joined)
    await message.answer(f"{res}\n Выберите действие", reply_markup=keyboard)
    await state.set_state(Bills.waiting_for_move.state)


@dp.message_handler(state=Bills.waiting_for_move)
async def group_start(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if message.text == 'Выбор категории расхода':
        for name in buttons:
            keyboard.add(name)
        await state.set_state(Bills.waiting_for_category.state)
        await message.answer("Выберите категорию:", reply_markup=keyboard)
    elif message.text == 'Узнать баланс':
        await message.answer(grab_balance(message.from_user.id))
        await state.finish()


@dp.message_handler(state=Bills.waiting_for_category)
async def category_chosen(message: types.Message, state: FSMContext):
    await state.update_data(category=message.text)
    if message.text not in buttons:
        await message.answer("Пожалуйста, выберите категорию, используя кнопки ниже.")
        return
    await message.answer(f"Введите сумму расходов", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Bills.waiting_for_value.state)


@dp.message_handler(state=Bills.waiting_for_value)
async def value_chosen(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    try:
        float(message.text)
    except ValueError:
        await message.answer("Пожалуйста, введите корреткное число")
        return
    add_spend(message.from_user.id, user_data['category'], float(message.text))
    await message.answer(f"Вы добавили трату в категорию {user_data['category']} ")
    await state.finish()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(group_start, state=Bills.waiting_for_move)
    dp.register_message_handler(category_chosen, state=Bills.waiting_for_category)
    dp.register_message_handler(value_chosen, state=Bills.waiting_for_value)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
