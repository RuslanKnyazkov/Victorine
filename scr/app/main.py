# app/main.py
from scr.config.config import TOKEN
from key import Key
from scr.quiz.quiz import Quiz
from telebot.async_telebot import AsyncTeleBot
from scr.config.logs import logger
from scr.quiz.reviews import DataBase
import asyncio
from scr.app.smtp import send_mail


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
    with db.connect:
        unique_id = db.cursor.execute("""SELECT * FROM user WHERE user_id=?""", (message.from_user.id,))
        if unique_id.fetchone() is None:
            db.cursor.execute(f"""INSERT INTO user (user_id, user_first_name, user_last_name)
            VALUES(?,?,?)""", (message.from_user.id, message.from_user.first_name, message.from_user.last_name))

    logger.info(f'User {message.from_user.first_name} {message.from_user.last_name} is logger in.')


@tbot.message_handler(commands=['info'])
async def get_info(message):
    await tbot.send_message(message.chat.id, text='Вы обратились в справочную службу.\n'
                                                  'Данный бот имеет в наличие такие команды как:\n'
                                                  '/start - Запускает викторину на тему Ваше тотемное животное.\n'
                                                  '/info - Информационное сообщение.\n'
                                                  '/contact - Связаться с нашим сотрудником.'
                                                  'Вы можете оставить свой отзыв начав сообщение с "Мой отзыв"')
    logger.info(f'User {message.from_user.first_name} {message.from_user.last_name} called info.')


@tbot.message_handler(commands=['contact'])
async def create_request(message):
    with db.connect:
        user = db.cursor.execute(f"""SELECT user_id FROM user WHERE user_id={message.from_user.id}""")
        if user.fetchone() is None:
            await tbot.send_message(message.chat.id, text='Пожалуйста для начала пройдите нашу викторину.')
        else:
            await tbot.send_message(message.chat.id, text='Вы желаете связаться с нашим сотрудником.',
                                    reply_markup=Key().create_key_line(['Да', 'Нет'], filters='contact'))
    logger.info(f'User {message.from_user.first_name} trying contact')


@tbot.callback_query_handler(func=lambda callback: callback.data.split(':')[-1] == 'contact')
async def confirm_contact(callback):
    if 'Да' in callback.data:
        try:
            with db.connect:
                sql_result = db.cursor.execute(f"""SELECT * FROM result_quiz WHERE user_id={callback.message.chat.id}""")
                values = []
                for i in sql_result.fetchone():
                    values.append(i)
                await send_mail(subject='Need contact', msg=f'<h1>Поступил запрос для уточнения информации.</h1>\n'
                                                            f'<p1>Контактные данные {values[1]} {values[2]}.\n'
                                                            f'Результат викторины {values[3]}')
                await tbot.send_message(callback.message.chat.id,
                                        text='Запрос отправлен. Ожидайте скоро с вами свяжутся.')
            logger.info('User send request.')
        except Exception as e:
            await tbot.send_message(callback.message.chat.id, text=f'Пожалуйста для начала пройдите викторину.\n'
                                                                   f'Начать ее можно с помощью /start')
            logger.info(f'{e}\n'
                        f'User trying add request without passed victorine')
    elif 'Нет' in callback.data:
        await tbot.send_message(callback.message.chat.id, text='Запрос отменен.')


@tbot.callback_query_handler(func=lambda callback: callback.data.split(':')[-1] == 'quiz')
async def callback_result(callback):
    """
    This function responds to all command buttons that have a filter with the name quiz.
    """
    try:
        quiz = Quiz()
        quiz.find_overlap(callback=callback.data.split(':')[0])
        if quiz.is_empty():
            collect = quiz.get_element()
            question, answers = str(*collect.keys()), dict(*collect.values())
            await tbot.send_message(callback.message.chat.id, text=f'{question}',
                                    reply_markup=Key().create_key_line(enum=answers, filters='quiz'))

        elif not quiz.is_empty():
            result = quiz.get_result()
            await tbot.send_message(chat_id=callback.message.chat.id,
                                    text=f'Поздравляем мы закончили и теперь можем точно сказать, что ваше тотемное '
                                         f'животное это <b>{result[0][0]}.</b>\n'
                                         f'И кстати вы можете стать его опекуном в Московском Зоопарке об этом вы можете'
                                         f'узнать более подробнее нажав по кнопке "Узнать больше"',
                                    parse_mode='HTML',
                                    reply_markup=Key().create_key_line(['Узнать больше'], filters='description'))
            await tbot.send_sticker(chat_id=callback.message.chat.id, sticker=f'{result[0][1]}')
            with db.connect:
                db.cursor.execute(f"""INSERT INTO result_quiz Values (?,?,?,?)""", (callback.message.chat.id,
                                                                                    callback.message.chat.first_name,
                                                                                    callback.message.chat.last_name,
                                                                                    result[0][0]))

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
    """
    When calling this function, the user is provided with all commands to interact with the bot.
    """
    await tbot.send_message(callback.message.chat.id,
                            text='<b>Возьмите животное под опеку! Участие в программе '
                                 '«Клуб друзей зоопарка» — это помощь в содержании наших обитателей,'
                                 ' а также ваш личный вклад в дело сохранения биоразнообразия'
                                 ' Земли и развитие нашего зоопарка.\n'
                                 'Если вас это заинтересовало, вы можете перейти на сайт</b>'
                                 '<a href="https://moscowzoo.ru/about/guardianship"><b> Московского зоопарка.</b></a> ',
                            parse_mode='HTML')


@tbot.message_handler(content_types=['text'])
async def find_some_text(message):
    """
    Handler some text.
    """
    if 'отзыв' in message.text.lower():
        with db.connect:
            db.cursor.execute("""INSERT INTO review VALUES (?,?,?,?)""", (message.from_user.id,
                                                                          message.from_user.first_name,
                                                                          message.from_user.last_name,
                                                                          message.text,))
            await tbot.send_message(message.chat.id, text='Ваш отзыв был обработан.')
    else:
        await tbot.send_message(message.chat.id, text='Извините я не смог распознать ваше сообщение.'
                                                      'Пожалуйста обратитесь к справочнику через команду /info')


if __name__ == '__main__':
    asyncio.run(tbot.polling(non_stop=True))
