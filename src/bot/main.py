import TOKEN
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import Message, message
from aiogram.dispatcher.filters import Text, Command
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
import sqlite3
import keyboards
import logging

class UserState(StatesGroup):
    variation = State()
    count = State()
    count_ngram = State()

TOKEN_API = TOKEN.TOKEN

storage = MemoryStorage()
bot = Bot(token=TOKEN_API, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

# создаем базу данных
sqlite_connection = sqlite3.connect('sqlite_python.db')
cursor = sqlite_connection.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users(user_id INTEGER, block INTEGER);""")
sqlite_connection.commit()


@dp.message_handler(commands=['start'])
async def start(message: Message):
    cursor.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
    result = cursor.fetchone()

    if result is None:
        cursor.execute(f'''SELECT * FROM users WHERE (user_id="{message.from_user.id}")''')
        entry = cursor.fetchone()
        if entry is None:
            cursor.execute(f'''INSERT INTO users VALUES ('{message.from_user.id}', '0')''')
            sqlite_connection.commit()
            await message.reply("Hello!", reply_markup=keyboards.greet_kb)
    else:
        await message.reply("your block Value is " + str(result[0]), reply_markup=keyboards.greet_kb)



@dp.message_handler(commands=["Generate_text"])
async def text_generator(message: Message):
    await message.reply("enter the number of the variation with which you want to generate the text(for information about variations type \"\help\"):", reply_markup=keyboards.greet_kb)
    await UserState.variation.set()

@dp.message_handler(state=UserState.variation)
async def get_variation(message: Message, state: FSMContext):
    await state.update_data(variation=message.text)
    await message.answer("Good! Now enter length of ngram:")
    await UserState.count.set()

'''@dp.message_handler(state=UserState.count_ngram)
async def get_variation(message: Message, state: FSMContext):
    await state.update_data(count_ngram=message.text)
    await message.answer("Good! Now enter count of words:")
    await UserState.count.set()
'''
@dp.message_handler(state=UserState.count)
async def get_count(message: Message, state: FSMContext):
    await state.update_data(count=message.text)
    await message.answer("Good! Wait a moment.")
    data = await state.get_data()
    await message.answer(f"Variation: {data['variation']}\n"
                         f"Count: {data['count']}\n"
                         f"generating...")
    await state.finish()


@dp.message_handler(commands=["Help"])
async def help(message: Message):
    await message.answer("...")


@dp.message_handler(commands=["Stat"])
async def stat(message: Message, command: Command):
    cursor.execute('''select * from users''')
    results = cursor.fetchall()
    await message.answer(f'Людей которые когда либо заходили в бота: {len(results)}')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
