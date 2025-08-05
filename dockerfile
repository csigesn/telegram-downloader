FROM python:3.11-slim

# 安装 ffmpeg 及依赖
RUN apt-get update \
 && apt-get install -y --no-install-recommends ffmpeg \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY bot.py .

# 安装 Python 库
RUN pip install --no-cache-dir python-telegram-bot yt-dlp

# 挂载目录，用于存储临时下载文件
VOLUME ["/downloads"]

# 环境变量
ENV TELEGRAM_BOT_TOKEN=

CMD ["python", "bot.py"]
