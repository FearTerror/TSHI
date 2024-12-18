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


import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl
import matplotlib.pyplot as plt


def plot_temperature_membership():

    temperature = np.linspace(-10, 50, 100)

    cold = fuzz.trimf(temperature, [-10, -10, 15])
    moderate = fuzz.trimf(temperature, [10, 25, 40])
    hot = fuzz.trimf(temperature, [30, 50, 50])

    plt.figure(figsize=(8, 4))
    plt.plot(temperature, cold, label="Холодно")
    plt.plot(temperature, moderate, label="Помірно")
    plt.plot(temperature, hot, label="Спекотно")
    plt.title("Функції належності для температури")
    plt.xlabel("Температура (°C)")
    plt.ylabel("Ступінь належності")
    plt.legend()
    plt.grid()
    plt.show()

    return temperature, cold, moderate, hot


def fuzzify_temperature(user_temp, temperature, cold, moderate, hot):

    cold_level = fuzz.interp_membership(temperature, cold, user_temp)
    moderate_level = fuzz.interp_membership(temperature, moderate, user_temp)
    hot_level = fuzz.interp_membership(temperature, hot, user_temp)

    print(f"\nТемпература {user_temp}°C:")
    print(f"  Холодно: {cold_level:.2f}")
    print(f"  Помірно: {moderate_level:.2f}")
    print(f"  Спекотно: {hot_level:.2f}")


def fan_speed_control(temp, hum):

    temperature = ctrl.Antecedent(np.linspace(0, 50, 100), 'temperature')
    humidity = ctrl.Antecedent(np.linspace(0, 100, 100), 'humidity')
    fan_speed = ctrl.Consequent(np.linspace(0, 100, 100), 'fan_speed')


    temperature['low'] = fuzz.trimf(temperature.universe, [0, 0, 25])
    temperature['medium'] = fuzz.trimf(temperature.universe, [15, 25, 35])
    temperature['high'] = fuzz.trimf(temperature.universe, [30, 50, 50])

    humidity['dry'] = fuzz.trimf(humidity.universe, [0, 0, 50])
    humidity['normal'] = fuzz.trimf(humidity.universe, [25, 50, 75])
    humidity['wet'] = fuzz.trimf(humidity.universe, [50, 100, 100])

    fan_speed['low'] = fuzz.trimf(fan_speed.universe, [0, 0, 50])
    fan_speed['medium'] = fuzz.trimf(fan_speed.universe, [25, 50, 75])
    fan_speed['high'] = fuzz.trimf(fan_speed.universe, [50, 100, 100])


    rule1 = ctrl.Rule(temperature['high'] & humidity['wet'], fan_speed['high'])
    rule2 = ctrl.Rule(temperature['medium'] & humidity['normal'], fan_speed['medium'])
    rule3 = ctrl.Rule(temperature['low'] | humidity['dry'], fan_speed['low'])


    fan_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
    fan = ctrl.ControlSystemSimulation(fan_ctrl)


    fan.input['temperature'] = temp
    fan.input['humidity'] = hum
    fan.compute()

    print(f"Швидкість вентилятора (за температури {temp}°C і вологості {hum}%): {fan.output['fan_speed']:.2f}")


def investment_risk_control(risk, profit):

    market_risk = ctrl.Antecedent(np.linspace(0, 100, 100), 'market_risk')
    expected_profit = ctrl.Antecedent(np.linspace(0, 100, 100), 'expected_profit')
    investment_level = ctrl.Consequent(np.linspace(0, 100, 100), 'investment_level')


    market_risk['low'] = fuzz.trimf(market_risk.universe, [0, 0, 50])
    market_risk['medium'] = fuzz.trimf(market_risk.universe, [25, 50, 75])
    market_risk['high'] = fuzz.trimf(market_risk.universe, [50, 100, 100])

    expected_profit['low'] = fuzz.trimf(expected_profit.universe, [0, 0, 50])
    expected_profit['medium'] = fuzz.trimf(expected_profit.universe, [25, 50, 75])
    expected_profit['high'] = fuzz.trimf(expected_profit.universe, [50, 100, 100])

    investment_level['not_recommended'] = fuzz.trimf(investment_level.universe, [0, 0, 50])
    investment_level['possible'] = fuzz.trimf(investment_level.universe, [25, 50, 75])
    investment_level['recommended'] = fuzz.trimf(investment_level.universe, [50, 100, 100])


    rule1 = ctrl.Rule(market_risk['low'] & expected_profit['high'], investment_level['recommended'])
    rule2 = ctrl.Rule(market_risk['medium'] & expected_profit['medium'], investment_level['possible'])
    rule3 = ctrl.Rule(market_risk['high'] | expected_profit['low'], investment_level['not_recommended'])

    investment_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
    investment = ctrl.ControlSystemSimulation(investment_ctrl)

    investment.input['market_risk'] = risk
    investment.input['expected_profit'] = profit
    investment.compute()

    print(f"Рівень інвестицій (ризик: {risk}%, прибуток: {profit}%): {investment.output['investment_level']:.2f}")


# Основна програма
if __name__ == "__main__":

    temperature, cold, moderate, hot = plot_temperature_membership()
    user_temp = float(input("Введіть температуру (°C): "))
    fuzzify_temperature(user_temp, temperature, cold, moderate, hot)

    temp = float(input("\nВведіть температуру для вентилятора (°C): "))
    hum = float(input("Введіть вологість (%): "))
    fan_speed_control(temp, hum)

    risk = float(input("\nВведіть рівень ризику ринку (%): "))
    profit = float(input("Введіть очікуваний прибуток (%): "))
    investment_risk_control(risk, profit)






