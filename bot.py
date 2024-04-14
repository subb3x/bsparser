import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InputMediaPhoto
from config import BOT_TOKEN
from aiogram.filters import Command
from main import get_maps, get_picks
from keyboards import maps_kb, menu_kb

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    text = """
Добро пожаловать в bsparser!
Доступные команды:
/active - показать активные в данный момент карты
/upcoming - показать карты, которые появятся в игре следующими
    """
    await message.answer(text, reply_markup=menu_kb())


@dp.message(Command("upcoming"))
async def upcoming(message: types.Message):
    media = []
    text = "Вы можете также посмотреть пики для любой из карт (кнопки не обновляются автоматически, для получения актуальной информации пропишите /upcoming)"
    for i, map in enumerate(get_maps(is_active=False)):
        if i > 9 and i % 9 == 1:
            await message.answer_media_group(media)
            media = []
        media.append(InputMediaPhoto(media=map[2], caption=f'{map[0]} \n{map[3]}'))
    await message.answer_media_group(media)
    await message.answer(text, reply_markup=maps_kb(get_maps(is_active=False)))


@dp.message(Command("active"))
async def active(message: types.Message):
    media = []
    text = "Вы можете также посмотреть пики для любой из карт (кнопки не обновляются автоматически, для получения актуальной информации пропишите /active)"
    for i, map in enumerate(get_maps(is_active=True)):
        if i > 9 and i % 9 == 1:
            await message.answer_media_group(media)
            media = []
        media.append(InputMediaPhoto(media=map[2], caption=f'{map[0]} \n{map[3]}'))
    await message.answer_media_group(media)
    await message.answer(text, reply_markup=maps_kb(get_maps(is_active=True)))


@dp.message(lambda message: message.text in [map[0] for map in get_maps(is_active=False)])
async def picks_upcoming(message: types.Message):
    for map in get_maps(is_active=False):
        if map[0] == message.text:
            if 'solo-showdown' in map[1] or 'trophy-escape' in map[1]:
                await message.answer("К сожалению, пики для одиночных режимов пока не доступны")
            else:
                await message.answer_photo(
                    caption=f"{map[0]} \n\nТоп 10 пиков для данной карты (по кол-ву побед): \n{'\n'.join(get_picks(map[1]))}",
                    photo=map[2])


@dp.message(lambda message: message.text in [map[0] for map in get_maps(is_active=True)])
async def picks_active(message: types.Message):
    for map in get_maps(is_active=True):
        if map[0] == message.text:
            if 'solo-showdown' in map[1] or 'trophy-escape' in map[1]:
                await message.answer("К сожалению, пики для одиночных режимов пока не доступны")
            else:
                await message.answer_photo(
                    caption=f"{map[0]} \n\nТоп 10 пиков для данной карты (по кол-ву побед): \n{'\n'.join(get_picks(map[1]))}",
                    photo=map[2])


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
