import random
import face_recognition
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, BotCommand, InputMediaPhoto
import json
import numpy as np
import sqlite3

# ADMIN_ID = 00000000
TOKEN = '5455860872:AAGAPtfX5wxVLE9AA8_8SpnnPCbb44mA3wk'

with open('sample.json') as json_file:
    data = json.load(json_file)

known_face_encodings = [np.asarray(i['encode']) for i in data]
known_face_names = [f"{i['dir']} -> {i['name']}" for i in data]



def start_func(update, context):
    global buttons
    buttons = [
        [InlineKeyboardButton(text="Send Photo", callback_data="send_photo"),
         ]
    ]

    update.message.reply_photo(
        photo=open('bot/bot.jpg', 'rb'),
        caption='Salom!!\nKim xaqida malumot olmoqchisiz🙂?\nRasm kiriting..!',
        reply_markup=InlineKeyboardMarkup(buttons)
    )




def message_handler(update, context):
    pass

def inline_messages(update, context):
    query = update.callback_query
    global buttons

    if query.data == 'send_photo':
        query.message.reply_photo(
            photo=f'https://www.google.com/imgres?imgurl=https%3A%2F%2Fblog.bismart.com%2Fhs-fs%2Fhubfs%2Flos-10-mejores-bots-disponibles-en-Internet.jpg%3Fwidth%3D5184%26name%3Dlos-10-mejores-bots-disponibles-en-Internet.jpg&imgrefurl=https%3A%2F%2Fblog.bismart.com%2Fen%2F10-best-bots-internet-now&tbnid=gVyV3Jd8TALO_M&vet=12ahUKEwiBnp6Z24H4AhVPiIsKHYwnBgUQMygTegUIARC_AQ..i&docid=WAEZXTVItK3BuM&w=5184&h=3888&q=bot%20foto&ved=2ahUKEwiBnp6Z24H4AhVPiIsKHYwnBgUQMygTegUIARC_AQ',
            caption='Kirish Mumkun emas😁!\n'
                    'Rasm yuboring👤.',
            reply_markup=InlineKeyboardMarkup(buttons)
        )
6

###################################################################################################################################



def photo_handler(update, context):
    file = update.message.photo[-1].file_id
    obj = context.bot.get_file(file)
    obj.download('image/a.jpg')

    try:
        uknown_img = face_recognition.load_image_file("Image/a.jpg")

        uknown_encoding = face_recognition.face_encodings(uknown_img)[0]
        minimum = 0.5
        result_index = None
        for i in range(len(known_face_encodings)):
            face_distances = face_recognition.face_distance([known_face_encodings[i]], uknown_encoding)[0]
            result = face_recognition.compare_faces([known_face_encodings[i]], uknown_encoding)
            if result[0] and face_distances < minimum:
                minimum = face_distances
                result_index = i

                # connection = sqlite3.connect(db_file)

        if result_index != None:
            df = str(data[result_index]['dir'])
            df1 = str(data[result_index]['name'])
            # print(df)
            student_data = f"Yo'nalish:{df}\nTalaba:{df1}"
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS malumot ("Yonalish", "Ism_familiya")')
            # cursor.execute(f"""INSERT INTO malumot ('Yonalish', 'Ism_familiya') VALUES ( df, df1)""")
            connection.commit()
            connection.close()
        else:
            student_data = "Bu xaqda malumot yo'q"

    except Exception as e:
        print(e)
        student_data ="Xato rasm joyladingiz(Ogohlantiraman faqat faceni qabul qilamiz)🙂!!"


    print(student_data)
    update.message.reply_text(text=student_data)




updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start_func))
dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
dispatcher.add_handler(CallbackQueryHandler(inline_messages))
dispatcher.add_handler(MessageHandler(Filters.photo, photo_handler))

updater.start_polling()
updater.idle()
