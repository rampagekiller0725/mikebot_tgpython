from flask import Flask
from flask import request
from flask import Response
import telebot
import requests
import time
import dbmanager
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "7054392482:AAG47au7xGVg4qNjpH-9uTHUHdGNdZLkvd0"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

start_msg = f"""Welcome to Mike Play Bot 🐹 
You are now the director of a crypto exchange.
Which one? You choose. Tap the screen, collect coins, pump up your passive income, 
develop your own income strategy.
We’ll definitely appreciate your efforts once the token is listed (the dates are coming soon).
Don't forget about your friends — bring them to the game and get even more coins together!"""

def parse_message(message):
    print("message-->", message)
    chat_id = message['message']['chat']['id']
    txt = message['message']['text']
    print("chat_id-->", chat_id)
    print("txt-->", txt)
    return chat_id, txt

def tel_send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    r = requests.post(url, json=payload)
    return r

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    username = message.from_user.username
    username_exist = username in dbmanager.users()
    print(username_exist)
    if username_exist == False:
        dbmanager.insert_one({
            "name": username, 
            "level": 1, 
            "profit_perhour": 0, 
            "coins": 0, 
            "fan_tokens_level": 0,
            "btc_pairs_level": 0,
            "eth_pairs_level": 0,
            "top_10_cmc_pairs_level": 0
        })
    
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': message.chat.id,
        'text': f"""Hello, {username}! """ + start_msg,
        'parse_mode': 'markdown',
        'reply_markup': {
            'inline_keyboard': [[
                {
                    'text': 'Play', 
                    'web_app': {
                        'url': 'https://paal-casino-gv0kx1vzd-rampagekiller0725.vercel.app/'
                    }
                }
            ]]
        }
    }
    r = requests.post(url, json=payload)
    return r

if __name__ == "__main__":
    while True:
        try:
            bot.infinity_polling(none_stop=True, timeout=15, long_polling_timeout=10)
        except Exception as e:
            time.sleep(15)