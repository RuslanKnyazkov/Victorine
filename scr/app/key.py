import telebot.types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

class Key:
    @staticmethod
    def create_key_line(enums: dict[str] | list[str], filters: str) -> telebot.types.InlineKeyboardMarkup:
        keys = InlineKeyboardMarkup()
        for enum in enums:
            keys.add(InlineKeyboardButton(text=enum, callback_data=f'{enum}:{filters}'), row_width=2)

        return keys
