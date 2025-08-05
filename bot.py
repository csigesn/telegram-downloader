import os
import logging
from telegram import Update, Bot
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from yt_dlp import YoutubeDL

# 日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 环境变量
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
STORAGE = "/downloads"
os.makedirs(STORAGE, exist_ok=True)

# 下载并发送音频
def download_and_send(update: Update, context: CallbackContext):
    url = update.message.text.strip()
    chat_id = update.message.chat_id
    msg = update.message.reply_text("开始下载，请稍候…")

    opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{STORAGE}/%(id)s.%(ext)s",
        "quiet": True,
    }

    try:
        with YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        context.bot.send_audio(chat_id, open(filename, "rb"))
        msg.edit_text("下载完成 ✔️")
    except Exception as e:
        logger.error("下载失败", exc_info=e)
        msg.edit_text("下载失败，请检查链接或稍后重试 ❌")

# 主入口
if __name__ == "__main__":
    if not TOKEN:
        logger.error("请设置环境变量 TELEGRAM_BOT_TOKEN")
        exit(1)

    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, download_and_send))

    updater.start_polling()
    logger.info("Bot 已启动，开始轮询…")
    updater.idle()
