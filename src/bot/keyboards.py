from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, \
    KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

button_help = KeyboardButton("/Help")
button_generate_text = KeyboardButton("/Generate_text")
button_show_stats = KeyboardButton("/Stat")

greet_kb = ReplyKeyboardMarkup(resize_keyboard=True)
greet_kb.add(button_help)
greet_kb.add(button_generate_text)
greet_kb.add(button_show_stats)