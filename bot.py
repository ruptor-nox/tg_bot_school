import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor


logging.basicConfig(level=logging.INFO)


BOT_TOKEN = '7878801559:AAFPDf68fece92kCSh9yuqbBF0j6IAFlkk8'

ADMIN_ID = 123456789


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
button_self = KeyboardButton("Опиши себе")
button_friend = KeyboardButton("Опиши товариша")
keyboard.add(button_self, button_friend)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply(
        "Привіт! Обери одну з кнопок нижче, щоб залишити опис.",
        reply_markup=keyboard
    )


@dp.message_handler(lambda message: message.text == "Опиши себе")
async def ask_for_self_description(message: types.Message):
    await message.reply("Напишіть щось про себе та надішліть мені.")


@dp.message_handler(lambda message: message.text == "Опиши товариша")
async def ask_for_friend_description(message: types.Message):
    await message.reply("Напишіть опис свого товариша та надішліть мені.")


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def handle_description(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username if message.from_user.username else "Невідомий"
    description = message.text

    # Надсилання опису
    try:
        await bot.send_message(
            ADMIN_ID,
            f"Новий опис від @{username} ({user_id}):\n\n{description}"
        )
    except Exception as e:
        logging.error(f"Не вдалося надіслати повідомлення адміністратору: {e}")

    await message.reply("Дякую! Ваш опис було надіслано.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)