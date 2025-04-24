import telebot
import time
from dotenv import load_dotenv
import os

load_dotenv()

bot = telebot.TeleBot(os.getenv('API_TOKEN'))


@bot.message_handler(commands=['start'])
def greeting(message):
    bot.send_message(message.chat.id, f'Assalamaleikum {message.chat.username}, lets work together!')



@bot.message_handler(commands=['post'])
def authentification(message):
    bot.send_message(message.chat.id, 'What is the password?')
    bot.register_next_step_handler(message, password)

def password(message):
    if message.text.strip() == os.getenv('PASSKEY'):
        bot.send_message(message.chat.id, 'Enter todays reminder:')
        bot.register_next_step_handler(message, section)
    else:
        bot.send_message(message.chat.id, "Wrong!")
        authentification(message)

def section(message):
    bot.send_message(os.getenv('CHANNEL_ID'), message.text)
    sent = bot.send_message(os.getenv('CHANNEL_ID'), message.text)
    global messageid
    messageid = sent.message_id

@bot.message_handler(commands=['edit'])
def path(message):
    bot.send_message(message.chat.id, 'Enter edited text:')
    bot.register_next_step_handler(message, edit)

def edit(message):
    bot.edit_message_text(chat_id= os.getenv('CHANNEL_ID'), message_id=messageid, text = message.text)


try:
    bot.polling(non_stop=True)
except Exception as e:
    print(f"Error: {e}")
    time.sleep(15)