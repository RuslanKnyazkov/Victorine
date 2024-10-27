import telebot.types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from scr.config.exceptions import AppException
from scr.config.logs import logger


class Key:
    @staticmethod
    def create_key_line(enum: dict[str] | list[str], filters: str) -> telebot.types.InlineKeyboardMarkup:
        if not isinstance(enum, (dict, list)):
            logger.exception(f'Was insert an invalid value {enum}')
            raise AppException('This format is not supported')

        keys: InlineKeyboardMarkup = InlineKeyboardMarkup()
        button: list = []
        try:
            for enum in enum:
                button.append(InlineKeyboardButton(text=enum, callback_data=f'{enum}:{filters}'))
        except Exception as error:
            logger.exception(error)
        keys.add(*button, row_width=2)
        return keys
