# app/main.py

from scr.config.config import TOKEN
from key import Key
from scr.quiz.quiz import Quiz
from telebot.async_telebot import AsyncTeleBot
from scr.config.logs import logger
from scr.quiz.reviews import DataBase
import asyncio

tbot = AsyncTeleBot(token=TOKEN)
db = DataBase()


@tbot.message_handler(commands=['start', 'restart'])
async def start_quiz(message):
    """
    Command call module quiz.
    """
    Quiz.restart()
    await tbot.send_message(message.chat.id, text=f'Добро пожаловать {message.from_user.first_name} '
                                                  f'{message.from_user.last_name} к нам.'
                                                  f' Хотели бы предложить пройти нашу '
                                                  'викторину на тему "Ваше тотемное животное"',
                            reply_markup=Key().create_key_line(['Я готов'], filters='quiz'))
    db.connect.execute("""CREATE TABLE IF NOT EXISTS reviews (User_first_name Text, User_last_name Text,
                        Reviews Text,
                        Result_quiz Text)""")
    logger.info(f'User {message.from_user.first_name} {message.from_user.last_name} is logger in.')


@tbot.message_handler(commands=['info'])
async def get_info(message):
    await tbot.send_message(message.chat.id, text='Вы обратились в справочную службу.\n'
                                                  'Данный бот имеет в наличие такие команды как:\n'
                                                  '/start - Запускает викторину на тему Ваше тотемное животное.\n'
                                                  '/info - Информационное сообщение.')
    logger.info(f'User {message.from_user.first_name} {message.from_user.last_name} called info.')


@tbot.callback_query_handler(func=lambda callback: callback.data.split(':')[-1] == 'quiz')
async def callback_result(callback):
    try:
        quiz = Quiz()
        quiz.find_overlap(callback=callback.data.split(':')[0])
        if quiz.is_empty():
            collect = quiz.get_element()
            question, answers = str(*collect.keys()), dict(*collect.values())
            await tbot.send_message(callback.message.chat.id, text=f'{question}',
                                    reply_markup=Key().create_key_line(enum=answers, filters='quiz'))
            #await tbot.reply_to(callback.message, text=f'{callback}')

        elif not quiz.is_empty():
            result = quiz.get_result()
            db.update_reviews(param=(callback.from_user.first_name,
                                    callback.from_user.last_name))
            await tbot.send_message(chat_id=callback.message.chat.id,
                                    text=f'Поздравляем мы закончили и теперь можем точно сказать, что ваше тотемное '
                                         f'животное это <b>{result[0][0]}.</b>\n'
                                         f'И кстати вы можете стать его опекуном в Московском Зоопарке об этом вы можете'
                                         f'узнать более подробнее нажав по кнопке "Узнать больше"',
                                    parse_mode='HTML',
                                    reply_markup=Key().create_key_line(['Узнать больше'], filters='description'))
            await tbot.send_sticker(chat_id=callback.message.chat.id, sticker=f'{result[0][1]}')

            Quiz.restart()
            await tbot.send_message(callback.message.chat.id,
                                    text='Если вы снова хотите пройти нашу викторину тогда чего тянуть,'
                                         'жмите кнопку и вперед.',
                                    reply_markup=Key().create_key_line(['Попробовать заново'], filters='quiz'))
    except Exception as error:
        await tbot.send_message(callback.message.chat.id, text=f'Нам очень жаль , но что то поломалось.')
        await tbot.send_sticker(callback.message.chat.id,
                                sticker='CAACAgIAAxkBAAIE7Gceg2rPAxAMjqn7IFPQlsW-bLDSAAJtAAOWn4wOh4Xo4eaCW_02BA')
        logger.exception(f'{error}')


@tbot.callback_query_handler(func=lambda callback: callback.data.split(':')[-1] == 'description')
async def show_description(callback):
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


# @tbot.message_handler(content_types=['sticker'])
# async def handler_s(message):
#     await tbot.send_message(message.chat.id, text=f'{message.sticker}')


if __name__ == '__main__':
    asyncio.run(tbot.polling(non_stop=True))
