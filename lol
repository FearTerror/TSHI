import telebot
import easyocr
import cv2
import os


TOKEN = '8023381722:AAH0zVK7HNjmWaxX9KkogavDDxz4Asr7XLE'
bot = telebot.TeleBot(TOKEN)


reader = easyocr.Reader(['en', 'uk'])

def recognize_with_easyocr(image_path):
    image = cv2.imread(image_path)
    image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    results = reader.readtext(image)

    recognized_text = ""
    for (bbox, text, prob) in results:
        recognized_text += f"{text} (Вероятность: {prob:.2f})\n"
    return recognized_text if recognized_text else "Не удалось распознать текст."


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Привет! Отправьте мне изображение номерного знака, и я распознаю его текст.")


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:

        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)


        image_path = "temp_image.jpg"
        with open(image_path, 'wb') as new_file:
            new_file.write(downloaded_file)


        result_text = recognize_with_easyocr(image_path)


        bot.reply_to(message, f"🔍 Распознанный текст:\n{result_text}")


        os.remove(image_path)
    except Exception as e:
        bot.reply_to(message, f"❌ Произошла ошибка: {str(e)}")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "📸 Пожалуйста, отправьте мне изображение номерного знака.")


print("Бот запущен...")
bot.polling()
