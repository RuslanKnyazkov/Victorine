from copy import deepcopy
import telebot.types
from Victorine.Questions import questions


class Quiz:
    """
    Class for victorine
    """
    step = 0
    animals = {'Тигр': 0, 'Белый медведь': 0, 'Лама': 0, 'Верблюд': 0}

    @classmethod
    def plus_one(cls):
        cls.step += 1

    def __init__(self):
        self.queue = deepcopy(questions)

    def is_end(self) -> bool:
        """
        Check length object.
        """
        if Quiz.step < len(self.queue):
            return True
        return False

    def get_element(self):
        """
        Delete first index in list.
        """
        if self.is_end():
            return self.queue[self.step]

    def find_animal(self, callback: telebot.TeleBot.callback_query_handler):
        for i in range(len(self.queue)):
            for elem in self.queue[i].values():
                if callback in elem:
                    self.animals[elem[callback]] = self.animals[elem[callback]] + 1
                    self.plus_one()
        print(self.animals)


