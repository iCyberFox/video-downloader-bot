import os
import uuid
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import yt_dlp

BOT_TOKEN = 7668246463:AAGM4qxBbaSaznoXUSPKvkjQ5imUdUMckwg  # Заміни на свій токен

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Надішли мені посилання на відео з YouTube, Instagram або Facebook!")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if not url.startswith("http"):
        await update.message.reply_text("❌ Це не схоже на посилання.")
        return

    video_filename = f"{uuid.uuid4()}.mp4"

    ydl_opts = {
        'format': 'mp4',
        'outtmpl': video_filename,
        'quiet': True,
        'noplaylist': True,
        'merge_output_format': 'mp4',
    }

    await update.message.reply_text("⏳ Завантажую відео...")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        if os.path.getsize(video_filename) > 49 * 1024 * 1024:
            await update.message.reply_text("❌ Відео занадто велике для відправки (більше 50МБ).")
        else:
            with open(video_filename, 'rb') as video:
                await update.message.reply_video(video)

    except Exception as e:
        await update.message.reply_text(f"❌ Помилка при завантаженні: {e}")

    finally:
        if os.path.exists(video_filename):
            os.remove(video_filename)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    print("✅ Бот запущено. Натисни Ctrl+C для зупинки.")
    app.run_polling()

if __name__ == '__main__':
    main()
