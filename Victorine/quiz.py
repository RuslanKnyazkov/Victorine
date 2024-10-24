from copy import deepcopy
import telebot.types
from Victorine.Questions import questions
from random import choice


class Quiz:
    """
    Class for victorine
    """
    animals = {'Тигр': {'value': 0, 'url': 'https://storage.moscowzoo.ru/storage/647edc2a70bb5462366280fc/'
                                           'images/animalsdetail/f00912dc-707c-42b9-9573-09eb0ed49523.jpeg'},
               'Белый медведь': {'value': 0, 'url': 'https://storage.moscowzoo.ru/storage/647edc2a70bb5462366280fc/'
                                                    'images/animalsdetail/a22417be-52a6-41fc-906a-f1cd5d4f7b13.jpeg'},
               'Лама': {'value': 0, 'url': 'https://storage.moscowzoo.ru/storage/647edc2a70bb5462366280fc/'
                                           'images/animalsdetail/8282bda3-e5a8-4cb6-b8f7-34215cf2a0af.jpeg'},
               'Верблюд': {'value': 0, 'url': 'https://storage.moscowzoo.ru/storage/647edc2a70bb5462366280fc/'
                                              'images/animals/80e7ccd4-56d1-49fb-a524-e7e2950ef60e.jpeg'}}
    __collection_questions = deepcopy(questions)

    @property
    def questions(self):
        return self.__collection_questions

    def is_empty(self) -> bool:
        """
        Check length object.
        """
        if self.__collection_questions:
            return True
        return False

    def get_element(self):
        """
        Return random question.
        """
        return choice(self.__collection_questions)

    def find_overlap(self, callback: telebot.TeleBot.callback_query_handler):
        """
        Find in iterable object.
        """
        for i in range(len(self.__collection_questions)):
            for elem in self.__collection_questions[i].values():
                if callback in elem:
                    self.animals[elem[callback]['value']] = self.animals[elem[callback]['value']] + 1
                    return self.questions.pop(i)

    def show_result(self):
        return max(self.animals.values, key= self.animals.get)
