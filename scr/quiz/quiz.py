from copy import deepcopy
import telebot.types
from scr.quiz.question import questions
from random import choice
from scr.config.logs import logger

class Animal:
    def __init__(self):
        self.animals = {'Тигр':
                            {'value': 0,
                             'sticker': 'CAACAgIAAxkBAAIEdmcbymCZzW466YH7OsMDfwWazySvAAJcAANZu_wlj1s_8uLbhRA2BA'},
                        'Белый медведь':
                            {'value': 0,
                             'sticker': 'CAACAgIAAxkBAAIEeWcbysUcjlNO4XrvGWvqLKzTliQaAAKPEgADyeFJiI2cXs9qMe42BA'},
                        'Лама':
                            {'value': 0,
                             'sticker': 'CAACAgIAAxkBAAIENmcbtJRxyr1vSrKv1jl_YjJnKvdyAAKXAAM7YCQUs-NVIets3tk2BA'},
                        'Верблюд':
                            {'value': 0,
                             'sticker': 'CAACAgIAAxkBAAIEoWcb0ZICtysZQRNxhcy_Dqfk9dAgAAIEAAOYv4ANbu82-byyOfU2BANone'}}

        self.__collection_questions = deepcopy(questions)

    @property
    def get_questions(self):
        """
        Return list.
        """
        return self.__collection_questions


class Quiz:
    """
    Class for victorine
    """

    datacls = Animal()

    @classmethod
    def restart(cls):
        """
        Create new templates when user choise start new quiz.
        """
        if cls.datacls is not None:
            cls.datacls = None
        cls.datacls = Animal()

    def is_empty(self) -> bool:
        """
        Check length object.
        """
        if self.datacls.get_questions:
            return True
        return False

    def get_element(self):
        """
        Return random question.
        """
        return choice(self.datacls.get_questions)

    def find_overlap(self, callback: telebot.TeleBot.callback_query_handler):
        """
        Find in iterable object.
        """
        for i in range(len(self.datacls.get_questions)):
            for elem in self.datacls.get_questions[i].values():
                if callback in elem:
                    self.datacls.animals[elem[callback]]['value'] = self.datacls.animals[elem[callback]]['value'] + 1
                    return self.datacls.get_questions.pop(i)

    def get_result(self):
        """
        Return name animal and url.
        """
        max_point = max(self.datacls.animals.values(), key=lambda x: x['value'])
        return [[name, values['sticker']] for name, values in self.datacls.animals.items() if max_point == values]
