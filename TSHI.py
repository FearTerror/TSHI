import telebot
from telebot import types
import webbrowser

TOKEN = '7883357675:AAFFUWtWfaApXZJ17j0X_TtsDrbpYb6wfCI'
bot = telebot.TeleBot(TOKEN)


def main_menu():
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)#row_width=3
    Zamov = types.KeyboardButton("Замовлення продуктів")
    Rozmich = types.KeyboardButton("Розміщення магазинів на мапі")
    SaleProp = types.KeyboardButton("Акційні пропозиції")
    Subscribes = types.KeyboardButton("Підписка на акційні пропозиції")
    #Knopka5 = types.KeyboardButton("For task")
    #menu.add(Zamov)
    #menu.row(Rozmich, SaleProp, Subscribes)
    menu.add(Zamov, Rozmich, SaleProp, Subscribes)
    #menu.add(Zamov, Rozmich)
    #menu.row(SaleProp, Subscribes, Knopka5)

    return menu

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Ласкаво просимо до сервісу замовлення продуктових товарів!\n/help - Для отримання списку команд\nОберіть послугу:", reply_markup=main_menu())


@bot.message_handler(func=lambda message: message.text == "Замовлення продуктів")
def order(message):
    bot.send_message(message.chat.id, "Яку категорію продуктів, ви хочете замовити?")


@bot.message_handler(func=lambda message: message.text == "Розміщення магазинів на мапі")
def map(message):
    try:
        with open("map.jpg", "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption="Ось розміщення наших магазинів")
    except FileNotFoundError:
        bot.send_message(message.chat.id, "Файл map.jpg не знайдено. Перевірте шлях до зображення.")

@bot.message_handler(func=lambda message: message.text == "Акційні пропозиції")
def sale(message):
    bot.send_message(message.chat.id, "Ось список акційних пропозицій на цьому тижні:.")


@bot.message_handler(func=lambda message: message.text == "Підписка на акційні пропозиції")
def sale_subs(message):
    bot.send_message(message.chat.id, "Підписка оформлена. Дякую за використання нашого магазину!")



@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, "Ось список команд:\n/start - Почати роботу з ботом\n/website - Сайт магазину\n /inform - Тестові функції")


@bot.message_handler(commands=['website'])
def open_website(message):
    bot.send_message(message.chat.id, "Відкриваю вебсайт...")
    webbrowser.open('https://www.metro.ua/')  # Замініть на URL вашого сайту

@bot.message_handler(commands=['inform'])
def inform(message):
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("Отримати фото котика", callback_data="send_cat")
    keyboard.add(button)
    bot.send_message(
        message.chat.id,
        "Тестова функція надсилання фотографії в чаті.",
        reply_markup=keyboard
    )

@bot.callback_query_handler(func=lambda call: call.data == "send_cat")
def send_cat(call):
    try:
        with open("cat.jpg", "rb") as photo:
            bot.send_photo(call.message.chat.id, photo, caption="Ось ваш кіт!")
    except FileNotFoundError:
        bot.send_message(call.message.chat.id, "Файл cat.jpg не знайдено. Перевірте шлях до файлу.")


bot.polling(none_stop=True)
