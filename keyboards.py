from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types


def maps_kb(maps: list) -> types.ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for i in range(len(maps)):
        builder.add(KeyboardButton(text=maps[i][0]))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def menu_kb() -> types.ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text='/active'))
    builder.add(KeyboardButton(text='/upcoming'))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)
