from Config.config import TOKEN
from telebot import TeleBot

tbot = TeleBot(token=TOKEN)

if __name__ == '__main__':
    tbot.polling(non_stop=True)
