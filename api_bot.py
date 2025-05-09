import telebot
from telebot.types import Message
import requests

API_URL = "http://127.0.0.1:8000/api"
TOKEN = YOUR_TG_BOT_TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_command(message):
    data = {
        "user_id": message.from_user.id,
        "username": message.from_user.username
    }
    response = requests.post(API_URL + "/register", json=data)
    if response.status_code == 200:
        if response.json().get('message'):
            bot.send_message(message.chat.id, "Вы уже были зарегистрированы ранее!")
        else:
            bot.send_message(message.chat.id,
                             f"Вы успешно зарегистрированы! Ваш уникальный номер: {response.json()['id']}")
    else:
        bot.send_message(message.chat.id, f"Произошла ошибка ри регистрации!")
        print(response.json())
        print(response.status_code)
        print(response.text)

@bot.message_handler(commands=['myinfo'])
def user_info(message: Message):
    response = requests.get(f"{API_URL}/user/{message.from_user.id}/")
    if response.status_code == 200:
        data = response.json()
        formatted_message = (
            "<b>🔐 Ваша регистрация:</b>\n\n"
            f"🆔 <b>User ID:</b> {data['user_id']}\n"
            f"👤 <b>Username:</b> @{data['username']}\n"
            f"📅 <b>Дата регистрации:</b> {data['created_at'][:10]} {data['created_at'][11:19]}"
        )
        bot.send_message(message.chat.id, formatted_message, parse_mode="HTML")
    elif response.status_code == 404:
        bot.send_message(message.chat.id, "❗️Вы не зарегистрированы!")
    else:
        bot.send_message(message.chat.id, "⚠️ Непредвиденная ошибка при получении данных!")


if __name__ == "__main__":
    bot.polling(none_stop=True)