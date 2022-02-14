class User:
    def __init__(self, id, first_name, last_name, email):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email


class Teacher(User):
    pass


class Student(User):
    pass


class UserFabric:
    types = {
        'student': Student,
        'teacher': Teacher
    }

    @classmethod
    def create(cls, user_type, first_name, last_name, email, id=None):
        if user_type not in cls.types:
            raise ValueError('unexpected user type')
        return cls.types[user_type](id, first_name, last_name, email)

    @classmethod
    def user_types(cls):
        return cls.types.keys()
