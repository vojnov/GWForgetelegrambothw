from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
import requests
import yt_dlp

async def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("Image", callback_data='download_image'),
         InlineKeyboardButton("Video", callback_data='download_video')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Do you want to download an image or a video?', reply_markup=reply_markup)

async def button(update: Update, context):
    query = update.callback_query
    await query.answer()
    if query.data == 'download_image':
        await query.message.reply_text('Send me a link to an image.')
        context.user_data['mode'] = 'image'
    elif query.data == 'download_video':
        await query.message.reply_text('Send me a link to a video.')
        context.user_data['mode'] = 'video'

async def handle_message(update: Update, context):
    url = update.message.text
    mode = context.user_data.get('mode', '')

    if url.startswith('http://') or url.startswith('https://'):
        if mode == 'image':
            response = requests.get(url)
            if response.status_code == 200:
                temp_path = 'temp_image.jpg'
                with open(temp_path, 'wb') as f:
                    f.write(response.content)
                with open(temp_path, 'rb') as f:
                    await update.message.reply_photo(photo=f)
            else:
                await update.message.reply_text('Failed to download image.')
        elif mode == 'video':
            await download_and_send_video(update, url)
    else:
        await update.message.reply_text('Please send a valid URL.')

async def download_and_send_video(update: Update, url: str):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'postprocessors': [{'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'}],
        'outtmpl': 'downloaded_video.mp4',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    with open('downloaded_video.mp4', 'rb') as f:
        await update.message.reply_document(document=f)

def main():
    application = Application.builder().token('6928659936:AAGVQiWHgTi5p8R6vuQTAVBiAlmn1TFW5YA').build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())

