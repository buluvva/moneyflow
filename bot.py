from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from resources.models import User, datetime
from constants import API_TOKEN
from app.process import insert_user, show_events
from aiogram.dispatcher import FSMContext
from resources.models import Bills
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from app.resources.buttons import groups_list, categories_dict

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


# async def test_db(message: types.Message):
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     buttons = ["Меню"]
#     keyboard.add(*buttons)
#     events = show_events()
#     res = list([i for i in events])
#     await message.answer(res)



# @dp.message_handler(commands="start")
@dp.message_handler(commands="start")
async def cmd_start(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Выбор категории расхода", "Узнать баланс"]
    keyboard.add(*buttons)
    user = User(tg_user_id=message.from_user.id,
                date_joined=datetime.now(),
                has_table=False)
    res = insert_user(user.tg_user_id, message.from_user.full_name, user.date_joined)
    await state.set_state(Bills.waiting_for_move.state)
    await message.answer(f"{res}\n Выберите действие", reply_markup=keyboard)


# @dp.message_handler(Text(equals="Выбор категории"))
async def group_start(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in groups_list:
        keyboard.add(name)
    await state.set_state(Bills.waiting_for_group.state)
    await message.answer("Выберите группу:", reply_markup=keyboard)


async def group_chosen(message: types.Message, state: FSMContext):
    if message.text.lower() not in groups_list:
        await message.answer("Пожалуйста, выберите группу, используя клавиатуру ниже.")
        return
    await state.update_data(chosen_group=message.text.lower())

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for size in categories_dict:
        keyboard.add(size)
    await state.set_state(Bills.waiting_for_category.state)
    await message.answer("Теперь выберите категорию:", reply_markup=keyboard)


async def category_chosen(message: types.Message, state: FSMContext):
    if message.text.lower() not in categories_dict:
        await message.answer("Пожалуйста, выберите размер порции, используя клавиатуру ниже.")
        return
    user_data = await state.get_data()
    await message.answer(f"Вы выбрали категорию {message.text.lower()} из группы {user_data['chosen_group']}", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(group_start, state=Bills.waiting_for_move)
    dp.register_message_handler(group_chosen, state=Bills.waiting_for_group)
    dp.register_message_handler(category_chosen, state=Bills.waiting_for_category)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
