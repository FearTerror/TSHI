# import telebot
# from telebot import types
# import sqlite3
# import webbrowser
#
# import requests
# import wikipedia
#
# TOKEN = '7883357675:AAFFUWtWfaApXZJ17j0X_TtsDrbpYb6wfCI'
# bot = telebot.TeleBot(TOKEN)
#
# # Підключення до бази даних
# conn = sqlite3.connect('TSHI.db', check_same_thread=False)
# cursor = conn.cursor()
#
# # Функція для перевірки та створення таблиці, якщо її не існує
# def check_and_create_table():
#     try:
#         cursor.execute("""
#             CREATE TABLE IF NOT EXISTS Product_list (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 Product_name TEXT NOT NULL,
#                 Type_Product TEXT NOT NULL
#             );
#         """)
#         conn.commit()
#     except sqlite3.Error as e:
#         print(f"Помилка при створенні таблиці: {e}")
#
# # Головне меню
# def main_menu():
#     menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     menu.add(types.KeyboardButton("Замовлення продуктів"))
#     menu.add(types.KeyboardButton("Розміщення магазинів на мапі"))
#     menu.add(types.KeyboardButton("Акційні пропозиції"))
#     menu.add(types.KeyboardButton("Підписка на акційні пропозиції"))
#     menu.add(types.KeyboardButton("Додавання продуктів"))
#     menu.add(types.KeyboardButton("Перегляд фруктів"))
#     return menu
#
# @bot.message_handler(func=lambda message: message.text == "Замовлення продуктів")
# def order(message):
#     menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     menu.add('Фрукти', 'Овочі', 'Молочні продукти')
#     bot.send_message(message.chat.id, "Яку категорію продуктів ви хочете замовити?", reply_markup=menu)

# @bot.message_handler(func=lambda message: message.text in ['Фрукти', 'Овочі', 'Молочні продукти'])
# def show_products(message):
#     product_type = message.text
#     try:
#         cursor.execute("SELECT id, Product_name FROM Product_list WHERE Type_Product = ?", (product_type,))
#         products = cursor.fetchall()
#         if products:
#             response = f"Список {product_type.lower()}:\n" + "\n".join([f"{row[0]}. {row[1]}" for row in products])
#         else:
#             response = f"У базі даних немає {product_type.lower()}."
#         bot.send_message(message.chat.id, response, reply_markup=main_menu())
#     except sqlite3.Error as e:
#         bot.send_message(message.chat.id, f"Сталася помилка при отриманні даних: {e}")
#
#
# @bot.message_handler(func=lambda message: message.text == "Розміщення магазинів на мапі")
# def map(message):
#     try:
#         with open("map.jpg", "rb") as photo:
#             bot.send_photo(message.chat.id, photo, caption="Ось розміщення наших магазинів")
#     except FileNotFoundError:
#         bot.send_message(message.chat.id, "Файл map.jpg не знайдено. Перевірте шлях до зображення.")
#
# @bot.message_handler(func=lambda message: message.text == "Акційні пропозиції")
# def sale(message):
#     bot.send_message(message.chat.id, "Ось список акційних пропозицій на цьому тижні:.")
#
#
# @bot.message_handler(func=lambda message: message.text == "Підписка на акційні пропозиції")
# def sale_subs(message):
#     bot.send_message(message.chat.id, "Введіть вашу електронну пошту для підписки:")
#     bot.register_next_step_handler(message, process_email)
#
# def process_email(message):
#     email = message.text
#     # Логіка перевірки або збереження електронної пошти
#     bot.send_message(message.chat.id, f"На вашу електронну пошту {email} надіслано тестове повідомлення.")
#     bot.send_message(message.chat.id, "Підписка оформлена. Дякую за використання нашого магазину!", reply_markup=main_menu())
#
# @bot.message_handler(commands=['website'])
# def open_website(message):
#     bot.send_message(message.chat.id, "Відкриваю вебсайт...")
#     webbrowser.open('https://www.metro.ua/')  # Замініть на URL вашого сайту
#
# @bot.message_handler(commands=['inform'])
# def inform(message):
#     keyboard = types.InlineKeyboardMarkup()
#     button = types.InlineKeyboardButton("Отримати фото котика", callback_data="send_cat")
#     keyboard.add(button)
#     bot.send_message(
#         message.chat.id,
#         "Тестова функція надсилання фотографії в чаті.",
#         reply_markup=keyboard
#     )
#
# @bot.callback_query_handler(func=lambda call: call.data == "send_cat")
# def send_cat(call):
#     try:
#         with open("cat.jpg", "rb") as photo:
#             bot.send_photo(call.message.chat.id, photo, caption="Ось ваш кіт!")
#     except FileNotFoundError:
#         bot.send_message(call.message.chat.id, "Файл cat.jpg не знайдено. Перевірте шлях до файлу.")
#
# @bot.message_handler(commands=['start'])
# def start(message):
#     bot.send_message(
#         message.chat.id,
#         "Ласкаво просимо до сервісу замовлення продуктових товарів!\n/help - Для отримання списку команд\nОберіть послугу:",
#         reply_markup=main_menu()
#     )
#
# @bot.message_handler(func=lambda message: message.text == 'Додавання продуктів')
# def register_prod(message):
#     menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     menu.add(types.KeyboardButton("Повернутися в головне меню"))
#     bot.send_message(message.chat.id, "Введіть назву продукту:", reply_markup=menu)
#     bot.register_next_step_handler(message, get_product_name)
#
# def get_product_name(message):
#     product_name = message.text
#
#     menu = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
#     menu.add('Овочі', 'Молочні продукти', 'Фрукти')
#     bot.send_message(message.chat.id, "Виберіть тип продукту:", reply_markup=menu)
#     bot.register_next_step_handler(message, get_product_type, product_name)
#
# def get_product_type(message, product_name):
#     product_type = message.text
#     if product_type not in ['Овочі', 'Молочні продукти', 'Фрукти']:
#         bot.send_message(message.chat.id, "Невірний тип продукту. Спробуйте ще раз.", reply_markup=main_menu())
#         return
#     try:
#         # Додавання продукту до бази даних
#         cursor.execute("INSERT INTO Product_list (Product_name, Type_Product) VALUES (?, ?)", (product_name, product_type))
#         conn.commit()
#         bot.send_message(message.chat.id, f"Продукт '{product_name}' додано до бази даних як '{product_type}'.", reply_markup=main_menu())
#     except sqlite3.Error as e:
#         bot.send_message(message.chat.id, f"Сталася помилка при додаванні до бази даних: {e}")
#
# @bot.message_handler(func=lambda message: message.text == 'Перегляд фруктів')
# def view_fruits(message):
#     try:
#         cursor.execute("SELECT id, Product_name FROM Product_list WHERE Type_Product = ?", ('Фрукти',))
#         fruits = cursor.fetchall()
#         if fruits:
#             response = "Список фруктів:\n" + "\n".join([f"{row[0]}. {row[1]}" for row in fruits])
#         else:
#             response = "Фрукти не знайдені в базі даних."
#         bot.send_message(message.chat.id, response, reply_markup=main_menu())
#     except sqlite3.Error as e:
#         bot.send_message(message.chat.id, f"Сталася помилка при отриманні даних: {e}")
#
# @bot.message_handler(func=lambda message: message.text == "Повернутися в головне меню")
# def return_to_main_menu(message):
#     bot.send_message(message.chat.id, "Повернення до головного меню.", reply_markup=main_menu())
#
# @bot.message_handler(commands=['help'])
# def help_command(message):
#     bot.send_message(
#         message.chat.id,
#         "Ось список команд:\n/start - Почати роботу з ботом\n/website - Сайт магазину\n/inform - Тестові функції"
#     )
#
#
#
# # Перевірка бази даних і запуск бота
# if __name__ == "__main__":
#     check_and_create_table()
#     print("База даних перевірена. Бот готовий до запуску.")
#     bot.polling(none_stop=True)


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





