# bot.py
import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
)
from yt_dlp import YoutubeDL

# 日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 环境变量
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    logger.error("请设置环境变量 TELEGRAM_BOT_TOKEN")
    exit(1)

STORAGE = "/downloads"
os.makedirs(STORAGE, exist_ok=True)

# 下载并发送音频
async def download_and_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    chat_id = update.effective_chat.id
    msg = await update.message.reply_text("开始下载，请稍候…")

    opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{STORAGE}/%(id)s.%(ext)s",
        "quiet": True,
    }

    try:
        with YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        await context.bot.send_audio(chat_id, audio=open(filename, "rb"))
        await msg.edit_text("下载完成 ✔️")
    except Exception as e:
        logger.error("下载失败", exc_info=e)
        await msg.edit_text("下载失败，请检查链接或稍后重试 ❌")

# 主入口
async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), download_and_send))
    logger.info("Bot 已启动，开始轮询…")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
