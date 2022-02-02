import os

from patterns import SingletonByName


class Logger(metaclass=SingletonByName):
    def __init__(self, name):
        self.name = name
        self.path = f'{os.getcwd()}\\logs\\{name}.log'

    def log(self, text):
        with open(self.path, 'a', encoding='utf-8') as file:
            file.write(f'{text}\n')
