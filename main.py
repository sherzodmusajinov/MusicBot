import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
import yt_dlp
import os

TELEGRAM_API_TOKEN = "7020718621:AAFiz9IiFwo_JGgHP6Fsm5XG8mt7jO_ucfg"

bot = Bot(token=TELEGRAM_API_TOKEN)
dp = Dispatcher()

yt_dlp_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': '%(title)s.%(ext)s',
    'quiet': True,
}

@dp.message(Command(commands=["start", "help"]))
async def send_welcome(message: Message):
    await message.reply(
        "Salom! Men musiqa yuklab beruvchi botman. Kerakli qo'shiq nomini yozing, men uni YouTube'dan topib beraman."
    )

@dp.message()
async def download_music(message: Message):
    query = message.text
    await message.reply("Qo'shiqni qidiryapman, iltimos kuting...")

    try:
        with yt_dlp.YoutubeDL(yt_dlp_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=True)['entries'][0]
            filename = ydl.prepare_filename(info).replace('.webm', '.mp3')

        if not os.path.exists(filename):
            raise FileNotFoundError("Fayl yuklab olinmadi yoki noto'g'ri formatda.")

        audio_file = FSInputFile(filename)
        await message.reply_document(audio_file)

        os.remove(filename)
    except Exception as e:
        await message.reply("Xatolik yuz berdi. Iltimos, boshqa qo'shiqni sinab ko'ring.")
        print(f"Xatolik: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
