import sqlite3

from courses import Category, CourseFabric
from logs import Logger
from patterns import SmsNotifier, EmailNotifier
from patterns import UserMapper, CourseMapper, CategoryMapper
from users import UserFabric

logger = Logger('courses-models')
connection = sqlite3.connect('db.sqlite', check_same_thread=False)
connection.execute("PRAGMA foreign_keys = 1")


class SiteDbData:
    def __init__(self, user_mapper, course_mapper, category_mapper, connection, user_fabric, course_fabric,
                 observers=()):
        self.user_mapper = user_mapper(connection)
        self.course_mapper = course_mapper(connection)
        self.category_mapper = category_mapper(connection)
        self.users_fabric = user_fabric
        self.courses_fabric = course_fabric
        self.observers = observers

    def create_user(self, user_type, first_name, last_name, email):
        user = self.users_fabric.create(user_type, first_name, last_name, email)
        self.user_mapper.create(user)
        return user

    def get_users(self):
        return self.user_mapper.get_all()

    def get_user(self, id):
        return self.user_mapper.get_by_id(id)

    def get_users_by_id(self, users_id):
        users = []
        for user in self.get_users():
            if user.id in users_id:
                users.append(user)
        return users

    def delete_user(self, id):
        u = self.get_user(id)
        self.user_mapper.delete(u)

    @property
    def user_types(self):
        return self.users_fabric.user_types()

    def create_course(self, course_type, name, title, text, categories, links=None):
        course_categories = self.get_categories_by_id(categories)
        course = self.courses_fabric.create(course_type, name, title, text, course_categories, links)
        self.course_mapper.create(course)
        logger.log(f'[INFO] Course created: {course.name}')
        return course

    def attach_notifier(self, subject):
        for observer in self.observers:
            subject.attach(observer())

    def get_course(self, id):
        course = self.course_mapper.get_by_id(id)
        self.attach_notifier(course)
        return course

    def edit_course(self, id, name, title, text, categories, links=None):
        course = self.get_course(id)
        course_cats = self.get_categories_by_id(list(map(lambda x: int(x), categories)))
        course.set_vars(name, title, text, course_cats, links)
        self.course_mapper.update(course)

    def copy_course(self, id, new_name):
        course = self.get_course(id)
        new_course = course.clone()
        new_course.name = new_name
        new_course.update_subscribers(())
        self.course_mapper.create(new_course)

    def subscribe_users_to_course(self, id, users):
        course = self.get_course(id)
        users = self.get_users_by_id(users)
        course.update_subscribers(users)
        self.course_mapper.update(course)

    def delete_course(self, id):
        c = self.get_course(id)
        self.course_mapper.delete(c)

    def get_courses(self):
        return self.course_mapper.get_all_or_by_category()

    def get_courses_by_category(self, id):
        return self.course_mapper.get_all_or_by_category(id)

    def create_category(self, name):
        category = Category(name)
        self.category_mapper.create(category)
        logger.log(f'[INFO] Category created: {name}')

    def get_categories(self):
        return self.category_mapper.get_all()

    def get_categories_by_id(self, cats_id):
        categories = []
        for category in self.category_mapper.get_all():
            if category.id in cats_id:
                categories.append(category)
        return categories

    def get_category(self, id):
        return self.category_mapper.get_by_id(id)

    def delete_category(self, id):
        c = self.get_category(id)
        self.category_mapper.delete(c)


observers = (SmsNotifier, EmailNotifier)

site = SiteDbData(UserMapper, CourseMapper, CategoryMapper, connection, UserFabric, CourseFabric, observers)
