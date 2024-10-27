# app/main.py

from scr.config.config import TOKEN
from key import Key
from scr.quiz.quiz import Quiz
from scr.config.exceptions import AppException
from telebot.async_telebot import AsyncTeleBot
import asyncio

tbot = AsyncTeleBot(token=TOKEN)


@tbot.message_handler(commands=['start'])
async def start_quiz(message):
    """
    Command call module quiz.
    """

    await tbot.send_message(message.chat.id, text=f'Добро пожаловать {message.from_user.first_name} '
                                                  f'{message.from_user.last_name} к нам.'
                                                  f' Хотели бы предложить пройти нашу '
                                                  'викторину на тему "Ваше тотемное животное"',
                            reply_markup=Key().create_key_line(['Я готов'], filters='quiz'))


@tbot.message_handler(commands=['info'])
async def get_info(message):
    await tbot.send_message(message.chat.id, text='Вы обратились в справочную службу.\n'
                                                  'Данный бот имеет в наличие такие команды как:\n'
                                                  '/start - Запускает викторину на тему Ваше тотемное животное.'
                                                  '')


@tbot.callback_query_handler(func=lambda callback: callback.data.split(':')[-1] == 'quiz')
async def callback_result(callback):
    quiz = Quiz()
    quiz.find_overlap(callback=callback.data.split(':')[0])
    if quiz.is_empty():
        collect = quiz.get_element()
        question, answers = str(*collect.keys()), dict(*collect.values())
        await tbot.send_message(callback.message.chat.id, text=f'{question}',
                                reply_markup=Key().create_key_line(enums=answers,
                                                                   filters='quiz'))

    elif not quiz.is_empty():
        result = quiz.get_animal()
        await tbot.send_message(chat_id=callback.message.chat.id,
                                text=f'Поздравляем мы закончили и теперь можем точно сказать, что ваше тотемное '
                                     f'животное это <b>{result[0][0]}.</b>\n'
                                     f'И кстати вы можете стать его опекуном в Московском Зоопарке об этом вы можете'
                                     f'узнать более подробнее нажав по кнопке "Узнать больше"',
                                parse_mode='HTML',
                                reply_markup=Key().create_key_line(['Узнать больше'], filters='info'))
        await tbot.send_sticker(chat_id=callback.message.chat.id, sticker=f'{result[0][1]}')

        Quiz.restart()
        await tbot.send_message(callback.message.chat.id,
                                text='Если вы снова хотите пройти нашу викторину тогда чего тянуть,'
                                     'жмите кнопку и вперед.',
                                reply_markup=Key().create_key_line(['Попробовать заново'], filters='quiz'))


@tbot.callback_query_handler(func=lambda callback: callback.data.split(':')[-1] == 'info')
async def show_info(callback):
    await tbot.send_message(callback.message.chat.id,
                            text='<b>Возьмите животное под опеку! Участие в программе '
                                 '«Клуб друзей зоопарка» — это помощь в содержании наших обитателей,'
                                 ' а также ваш личный вклад в дело сохранения биоразнообразия'
                                 ' Земли и развитие нашего зоопарка.\n'
                                 'Если вас это заинтересовало, вы можете перейти на сайт</b>'
                                 '<a href="https://moscowzoo.ru/about/guardianship"><b> Московского зоопарка.</b></a> ',
                            parse_mode='HTML')


@tbot.message_handler(content_types=['text'])
async def handler_text(message):
    await tbot.send_message(message.chat.id, text='Извините я не смог распознать ваше сообщение.'
                                                  ' Пожалуйста обратитесь к справочнику через команду /info')


if __name__ == '__main__':
    asyncio.run(tbot.polling(non_stop=True))
