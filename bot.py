import logging
import os
import requests
from config import TG_TOKEN
from text_recognision import audio_to_text, shorten_text, audio_converter
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update, context):
    user = update.effective_user
    await update.message.reply_text(
        f"Здравствуйте, {user.first_name}.\n"
        f"Пересылайте аудио сообщения в бота, он распознает речь и сократит ее.",
    )


async def shorten_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    new_file = await context.bot.get_file(update.message.voice.file_id)
    # print(new_file)
    file_id = new_file.file_id
    file_path = new_file.file_path
    r = requests.get(file_path)
    with open(file_id, 'wb') as fp:
        fp.write(r.content)
    new_name = audio_converter(file_id)
    text = audio_to_text(new_name)
    print(text)
    os.remove(new_name)
    short_text = shorten_text(text)
    print(short_text)

    await update.message.reply_text(short_text)


def main():
    application = Application.builder().token(TG_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.VOICE & ~filters.COMMAND, shorten_voice))
    application.run_polling()


if __name__ == "__main__":
    main()
