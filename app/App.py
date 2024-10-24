from Config.config import TOKEN
from telebot import TeleBot, types
from KeyBoard import Key
from Victorine.quiz import Quiz

tbot = TeleBot(token=TOKEN)


@tbot.message_handler(commands=['start', 'restart'])
def start_quiz(message):
    """
    Call victorine with first questions.
    """
    tbot.send_message(message.chat.id, text='Добро пожаловать к нам. Хотели бы предложить пройти нашу '
                                            'викторину и узнать вашего тотемного животного',
                      reply_markup=Key().create_key_line(['Я готов']))


@tbot.callback_query_handler(func=lambda callback: True)
def foo(callback):
    quiz = Quiz()
    quiz.find_overlap(callback=callback.data)
    if quiz.is_empty():
        collect = quiz.get_element()
        question, answers = collect.keys(), dict(*collect.values())
        tbot.send_message(callback.message.chat.id, text=question,
                          reply_markup=Key().create_key_line(answers))
    else:
        tbot.send_message(chat_id=callback.message.chat.id,
                          text=f'Викторина закончилась ваше животное это ЛАМА'
                               f'{''}',
                          disable_web_page_preview=True)


if __name__ == '__main__':
    tbot.polling(non_stop=True)
