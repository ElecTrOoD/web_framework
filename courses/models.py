from patterns import PrototypeMixin


class Category:
    def __init__(self, name, id=None):
        self.name = name
        self.id = id


class Course(PrototypeMixin):
    def __init__(self, name, title, text, categories, links=None, id=None):
        self.id = id
        self.name = name
        self.title = title
        self.text = text
        self.categories = categories
        self.links = links
        self._subscribers = set()
        self._observers = set()

    def set_vars(self, name, title, text, categories, links):
        self.name = name if name else self.name
        self.title = title if title else self.title
        self.text = text if text else self.text
        self.categories = categories if categories else self.categories
        self.links = links
        self._notify()

    def get_vars(self):
        data = {'id': self.id,
                'name': self.name,
                'title': self.title,
                'text': self.text,
                'categories': self.categories,
                'links': self.links}
        return data

    def update_subscribers(self, users):
        self._subscribers.difference_update(self._subscribers.difference(users))
        self._subscribers.update(users)

    @property
    def subscribers(self):
        return self._subscribers

    def attach(self, observer):
        observer._subject = self
        self._observers.add(observer)

    def detach(self, observer):
        observer._subject = None
        self._observers.discard(observer)

    def _notify(self):
        for observer in self._observers:
            observer.update()

    def __iter__(self):
        for user in self._subscribers:
            yield user


class OnlineCourse(Course):
    pass


class OfflineCourse(Course):
    pass


class CourseFabric:
    types = {
        'online': OnlineCourse,
        'offline': OfflineCourse
    }

    @classmethod
    def create(cls, course_type, name, title, text, categories, links=None, id=None):
        if course_type not in cls.types:
            raise ValueError('unexpected course type')
        return cls.types[course_type](name, title, text, categories, links, id)

    @classmethod
    def course_types(cls):
        return cls.types.keys()
