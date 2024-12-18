import speech_recognition as sr
import pyttsx3
from transformers import pipeline

# 1. Налаштування синтезатора мовлення (TTS)
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# 2. Налаштування розпізнавання мови (ASR)
recognizer = sr.Recognizer()
def recognize_speech():
    with sr.Microphone() as source:
        print("Слухаю... Говоріть:")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio, language="uk-UA")
            print(f"Ви сказали: {text}")
            return text
        except sr.UnknownValueError:
            print("Не вдалося розпізнати мову.")
            speak("Не вдалося розпізнати мову. Спробуйте ще раз.")
        except sr.RequestError as e:
            print("Помилка сервісу: {0}".format(e))
            speak("Помилка сервісу. Перевірте інтернет-з'єднання.")
        return ""

# 3. Налаштування NLP для розпізнавання намірів
qa_model = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
def get_response(question, context):
    try:
        result = qa_model(question=question, context=context)
        return result["answer"]
    except Exception as e:
        print(f"Помилка NLP: {e}")
        return "На жаль, я не зміг знайти відповідь на ваше питання."

# 4. Основний цикл бота
def main():
    context = "Голосовий бот для довідки. Ви можете запитати про будь-яку інформацію."  # Можна розширити контекст
    speak("Привіт! Я ваш голосовий помічник. Чим можу допомогти?")
    while True:
        user_input = recognize_speech()

        if not user_input:
            continue

        if "завершити" in user_input.lower():
            speak("Дякую, що скористалися ботом. До побачення!")
            break

        response = get_response(user_input, context)
        print(f"Бот: {response}")
        speak(response)

if __name__ == "__main__":
    main()


import openai
import telebot
import pyttsx3
import threading

# Set your OpenAI API key
openai.api_key = ''

# Initialize the bot and the speech engine
bot = telebot.TeleBot('')
engine = pyttsx3.init()


# Generate GPT-3 response
def generate_gpt_response(text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4"
            messages=[{"role": "user", "content": text}],
            max_tokens=150,
            temperature=0.7
        )
        return response['choices'][0]['message']['content'].strip()
    except openai.OpenAIError as e:
        print(f"OpenAI API error: {e}")
        return "Sorry, there was an error with generating the response."
    except Exception as e:
        print(f"General error: {e}")
        return "Sorry, I couldn't generate a response right now."


# Speak function
def speak(text):
    def run_speech():
        engine.say(text)
        engine.runAndWait()

    # Run the speech synthesis in a separate thread
    speech_thread = threading.Thread(target=run_speech)
    speech_thread.start()


# Handle the message
@bot.message_handler(func=lambda message: True)
def respond(message):
    user_input = message.text
    print(f"User said: {user_input}")
    response = generate_gpt_response(user_input)
    print(f"Bot response: {response}")
    speak(response)
    bot.reply_to(message, response)


# Start polling
if __name__ == "__main__":
    bot.polling()





import telebot
import pyttsx3
import requests
import json

# Your Amadeus API key
amadeus_api_key = ''

# Your OpenWeatherMap API key
weather_api_key = ''

# Initialize the bot
bot = telebot.TeleBot('')

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Function to speak the response
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Command handler
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! How can I assist you today?")
    speak("Hello! How can I assist you today?")

# Weather request handler
@bot.message_handler(func=lambda message: message.text.lower() == 'weather')
def get_weather(message):
    city = "London"  # Specify the city to check weather
    weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric'

    weather_response = requests.get(weather_url)
    if weather_response.status_code == 200:
        weather_data = weather_response.json()
        description = weather_data['weather'][0]['description']
        temp = weather_data['main']['temp']
        response = f"The weather in {city}: {description}, temperature: {temp}°C."
        bot.reply_to(message, response)
        speak(response)
    else:
        bot.reply_to(message, "Sorry, I couldn't fetch the weather information.")
        speak("Sorry, I couldn't fetch the weather information.")

# Travel request handler
@bot.message_handler(func=lambda message: 'travel' in message.text.lower())
def search_travel_destinations(message):
    url = 'https://api.amadeus.com/v2/shopping/flight-offers'
    headers = {'Authorization': f'Bearer {amadeus_api_key}', 'Content-Type': 'application/json'}

    params = {
        'origin': 'LON',  # London
        'destination': 'NYC',  # New York
        'departureDate': '2024-12-25',  # Departure date
        'adults': 1  # Number of adults
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        # Check if there are any results
        if data.get("data"):
            offer = data['data'][0]  # Get the first offer
            price = offer['price']['total']
            airline = offer['validatingAirlineCodes'][0]  # First airline
            response = f"Best offer: {price} EUR, airline: {airline}"
            bot.reply_to(message, response)
            speak(response)
        else:
            bot.reply_to(message, "No travel offers found.")
            speak("No travel offers found.")
    else:
        bot.reply_to(message, "Sorry, I couldn't find any travel offers.")
        speak("Sorry, I couldn't find any travel offers.")

# Handler for other messages
@bot.message_handler(func=lambda message: True)
def respond(message):
    bot.reply_to(message, "Sorry, I didn't understand your request.")
    speak("Sorry, I didn't understand your request.")

# Function to start the bot
def start_bot():
    bot.polling()

# Start the bot
if __name__ == '__main__':
    start_bot()






