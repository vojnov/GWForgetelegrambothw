FROM python:3.10

RUN pip install -U yt-dlp

RUN apt-get update && apt-get install -y ffmpeg

COPY requirements.txt /telegrambot/
WORKDIR /telegrambot/
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "bot.py"]


