
# ADMIN_ID = 00000000
# TOKEN = '7709623940:AAFryYQE1tDVToenEkVktoX9cs12sfHdqcQ'

from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import face_recognition
import json
import numpy as np
import os

TOKEN = '7709623940:AAFryYQE1tDVToenEkVktoX9cs12sfHdqcQ'

with open('sample.json') as json_file:
    data = json.load(json_file)

known_face_encodings = [np.asarray(i['encode']) for i in data]
known_face_names = [f"{i['dir']} -> {i['name']}" for i in data]

async def start_func(update, context):
    buttons = [[InlineKeyboardButton(text="Send Photo", callback_data="send_photo")]]
    await update.message.reply_text(
        text='Salom!!\nKim haqida maʼlumot olmoqchisiz?🙂\nRasm kiriting..!',
        reply_markup=InlineKeyboardMarkup(buttons)
    )

async def inline_messages(update, context):
    query = update.callback_query
    if query.data == 'send_photo':
        await query.message.reply_text(
            text='Rasm yuboring👤.',
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Send Photo", callback_data="send_photo")]])
        )

async def photo_handler(update, context):
    file = await context.bot.get_file(update.message.photo[-1].file_id)
    image_path = 'image/a.jpg'

    # 🔥 Rasmni saqlash uchun katalog mavjudligini tekshirish
    os.makedirs(os.path.dirname(image_path), exist_ok=True)
    
    await file.download_to_drive(image_path)

    try:
        unknown_img = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(unknown_img)
        
        # 🔥 Yuz mavjudligini tekshirish
        if len(encodings) == 0:
            await update.message.reply_text("Xato rasm joyladingiz! Faqat yuz tasvirlarini qabul qilamiz 🙂!")
            return

        unknown_encoding = encodings[0]
        minimum = 0.5
        result_index = None

        for i, encoding in enumerate(known_face_encodings):
            face_distances = face_recognition.face_distance([encoding], unknown_encoding)[0]
            result = face_recognition.compare_faces([encoding], unknown_encoding)
            if result[0] and face_distances < minimum:
                minimum = face_distances
                result_index = i

        if result_index is not None:
            df = data[result_index]['dir']
            df1 = data[result_index]['name']
            student_data = f"Yo'nalish: {df}\nTalaba: {df1}"
        else:
            student_data = "Bu haqda ma'lumot yo'q"

    except Exception as e:
        student_data = f"Xato yuz berdi: {str(e)}"

    await update.message.reply_text(text=student_data)

# 🔥 Yangi versiya bilan mos keladigan `Application`
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler('start', start_func))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, lambda update, context: None))  # 🔥 Filtrni to'g'ri ishlatish
app.add_handler(CallbackQueryHandler(inline_messages))
app.add_handler(MessageHandler(filters.PHOTO, photo_handler))

print("Bot ishlamoqda...")
app.run_polling()
