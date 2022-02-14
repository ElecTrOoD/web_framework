import abc


class Observer(metaclass=abc.ABCMeta):
    def __init__(self):
        self._subject = None

    @abc.abstractmethod
    def update(self):
        pass


class SmsNotifier(Observer):
    def update(self):
        print(f'[INFO] Отправлены смс уведомления об изменение курса "{self._subject.name}" '
              f'пользователям: {[f"{user.first_name} {user.last_name}" for user in self._subject]}')


class EmailNotifier(Observer):
    def update(self):
        print(f'[INFO] Отправлены email уведомления об изменение курса "{self._subject.name}" '
              f'пользователям: {[user.email for user in self._subject]}')
