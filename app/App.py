from Config.config import TOKEN
from telebot import TeleBot
from KeyBoard import Key
from Victorine.quiz import Quiz

tbot = TeleBot(token=TOKEN)


@tbot.message_handler(commands=['start'])
def start_quiz(message):
    tbot.send_message(message.chat.id, text='Добро пожаловать к нам. Хотели бы предложить пройти нашу '
                                            'викторину и узнать вашего тотемного животного',
                      reply_markup=Key().create_key_line(['Я готов']))


@tbot.callback_query_handler(func=lambda callback: True)
def foo(callback):
    quiz = Quiz()
    quiz.find_animal(callback=callback.data)
    collect = quiz.get_element()
    question, answers = collect.keys(), dict(*collect.values())

    key = Key()
    tbot.send_message(callback.message.chat.id, text=question,
                      reply_markup=key.create_key_line(answers))


if __name__ == '__main__':
    tbot.polling(non_stop=True)
