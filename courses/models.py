import os
import pickle

from logs import Logger
from patterns import PrototypeMixin, SingletonByName

logger = Logger('courses-models')


class User:
    def __init__(self, name):
        self.name = name


class Teacher(User):
    pass


class Student(User):
    pass


class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher
    }

    @classmethod
    def create(cls, user_type, name):
        if user_type not in cls.types:
            raise ValueError('unexpected user type')
        return cls.types[user_type](name)


class Category(metaclass=SingletonByName):
    def __init__(self, name):
        self.name = name


class Course(PrototypeMixin):
    def __init__(self, name, title, text, categories, links=None):
        self.name = name
        self.title = title
        self.text = text
        self.categories = categories
        self.links = links


class OnlineCourse(Course):
    pass


class OfflineCourse(Course):
    pass


class CourseFactory:
    types = {
        'online': OnlineCourse,
        'offline': OfflineCourse
    }

    @classmethod
    def create(cls, course_type):
        if course_type not in cls.types:
            raise ValueError('unexpected course type')
        return cls.types[course_type]


class SiteData:
    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []
        self.load_data()

    def create_user(self, user_type, name):
        user = UserFactory.create(user_type, name)
        if user_type == 'teacher':
            self.teachers.append(user)
        elif user_type == 'student':
            self.students.append(user)
        else:
            raise ValueError('Incorrect user type')
        self.save_data()
        return user

    def create_course(self, course_type, name, title, text, categories, links=None):
        # course = CourseBuilder(course_type).name(name).title(title).text(text).categories(categories)
        # if links:
        #     course = course.additional_links(links)
        # course = course.build()
        course = CourseFactory.create(course_type)
        course_categories = []
        for category in self.categories:
            if category.name in categories:
                course_categories.append(category)
        new_course = course(name, title, text, course_categories, links)

        self.courses.append(new_course)
        self.save_data()
        logger.log(f'[INFO] Course created: {new_course.name}')
        return course

    def get_course_by_name(self, name):
        for course in self.courses:
            if course.name == name:
                return course
        return None

    def copy_course(self, name, new_name):
        course = self.get_course_by_name(name)
        new_course = course.clone()
        new_course.name = new_name
        self.courses.append(new_course)
        self.save_data()

    def delete_course(self, name):
        for course in self.courses:
            if course.name == name:
                self.courses.remove(course)
                self.save_data()
                break

    def get_courses(self):
        return self.courses

    def get_courses_by_category(self, name):
        category = self.get_category_by_name(name)
        courses_by_category = []
        for course in self.courses:
            if category in course.categories:
                courses_by_category.append(course)
        return courses_by_category

    def create_category(self, name):
        category = Category(name)
        if category not in self.categories:
            self.categories.append(category)
            self.save_data()
            logger.log(f'[INFO] Category created: {name}')

    def get_categories(self):
        return self.categories

    def get_category_by_name(self, name):
        for category in self.categories:
            if category.name == name:
                return category

    def delete_category(self, name):
        category = self.get_category_by_name(name)
        self.categories.remove(category)
        self.save_data()

    def save_data(self):
        data = {
            'teachers': self.teachers,
            'students': self.students,
            'courses': self.courses,
            'categories': self.categories
        }
        print(data)
        with open('data.pkl', 'wb') as file:
            pickle.dump(data, file, pickle.HIGHEST_PROTOCOL)
        logger.log(f'[INFO] Data saved: {data}')

    def load_data(self):
        if not os.path.isfile('data.pkl'):
            with open('data.pkl', 'wb') as file:
                pickle.dump({'teachers': [], 'students': [], 'courses': [], 'categories': []}, file,
                            pickle.HIGHEST_PROTOCOL)
        with open('data.pkl', 'rb') as file:
            data = pickle.load(file)
            self.teachers = data['teachers']
            self.students = data['students']
            self.courses = data['courses']
            self.categories = data['categories']
        logger.log(f'[INFO] Data loaded: {data}')
