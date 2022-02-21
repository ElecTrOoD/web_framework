import abc

import courses.models as c
import users.models as u


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class DataMapper(metaclass=abc.ABCMeta):
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    @abc.abstractmethod
    def get_by_id(self, id):
        pass

    @abc.abstractmethod
    def create(self, obj):
        pass

    @abc.abstractmethod
    def update(self, obj):
        pass

    @abc.abstractmethod
    def delete(self, obj):
        pass


class UserMapper(DataMapper):
    def get_by_id(self, id):
        statement = f'SELECT type, first_name, last_name, email, id FROM USERS WHERE id=?'

        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return u.UserFabric.create(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def get_subscribers_id_by_course_id(self, id):
        statement = f'SELECT user_id ' \
                    f'FROM SUBSCRIBERS ' \
                    f'WHERE course_id=?'
        self.cursor.execute(statement, (id,))
        result = [x[0] for x in self.cursor.fetchall()]
        return result

    def get_all(self):
        statement = f'SELECT type, first_name, last_name, email, id FROM USERS'
        users = []

        self.cursor.execute(statement)
        result = self.cursor.fetchall()
        if result:
            for item in result:
                users.append(u.UserFabric.create(*item))
        return users

    def create(self, obj):
        statement = f'INSERT INTO USERS (first_name, last_name, email, type) VALUES (?, ?, ?, ?)'
        self.cursor.execute(statement, (obj.first_name, obj.last_name, obj.email, obj.__class__.__name__.lower()))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f'UPDATE USERS SET first_name=?, last_name=?, email=?, type=? WHERE id=?'
        self.cursor.execute(statement,
                            (obj.first_name, obj.last_name, obj.email, obj.__class__.__name__.lower(), obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f'DELETE FROM USERS WHERE id=?'
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class CourseMapper(DataMapper):
    def get_by_id(self, id):
        course_statement = f'SELECT type, name, title, text, links, id ' \
                           f'FROM COURSES ' \
                           f'WHERE id=?'

        self.cursor.execute(course_statement, (id,))
        course_data = self.cursor.fetchone()

        if course_data:
            result = {
                'course_type': course_data[0],
                'name': course_data[1],
                'title': course_data[2],
                'text': course_data[3],
                'links': course_data[4],
                'id': course_data[5],
                'categories': CategoryMapper(self.connection).get_by_course_id(id),
            }
            course = c.CourseFabric.create(**result)

            course_subs_id = UserMapper(self.connection).get_subscribers_id_by_course_id(id)
            all_users = UserMapper(self.connection).get_all()
            subscribers = []

            for user in all_users:
                if user.id in course_subs_id:
                    subscribers.append(user)
            course.update_subscribers(subscribers)
            return course
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def get_all_or_by_category(self, category=None):
        courses_statement = f'SELECT type, name, title, text, links, id FROM COURSES'
        courses = []

        all_users = UserMapper(self.connection).get_all()

        self.cursor.execute(courses_statement)
        result = self.cursor.fetchall()
        if result:
            for item in result:
                categories_data = CategoryMapper(self.connection).get_by_course_id(item[5])
                categories_id = [item.id for item in categories_data]
                if category and int(category) not in categories_id:
                    continue

                data = {
                    'course_type': item[0],
                    'name': item[1],
                    'title': item[2],
                    'text': item[3],
                    'links': item[4],
                    'id': item[5],
                    'categories': categories_data,
                }

                course = c.CourseFabric.create(**data)
                course_subs_id = UserMapper(self.connection).get_subscribers_id_by_course_id(course.id)
                if course_subs_id:
                    subscribers = []
                    for user in all_users:
                        if user.id in course_subs_id:
                            subscribers.append(user)
                    course.update_subscribers(subscribers)

                courses.append(course)
        return courses

    def create(self, obj):
        course_statement = f'INSERT INTO COURSES (name, title, text, links, type) VALUES (?, ?, ?, ?, ?)'
        course_cat_statement = f'INSERT INTO COURSE_CATEGORIES (course_id, category_id) VALUES (?, ?)'

        self.cursor.execute(course_statement, (
            obj.name, obj.title, obj.text, obj.links, obj.__class__.__name__.lower().replace('course', '')))
        self.cursor.execute('SELECT last_insert_rowid()')
        course_id = self.cursor.fetchone()[0]

        for category in obj.categories:
            self.cursor.execute(course_cat_statement, (course_id, category.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        course_statement = f'UPDATE COURSES SET name=?, title=?, text=?, links=?, type=? WHERE id=?'
        insert_subscibers_statement = f'INSERT INTO SUBSCRIBERS (user_id, course_id) VALUES (?, ?)'
        delete_subscibers_statement = f'DELETE FROM SUBSCRIBERS WHERE user_id=? and course_id=?'
        insert_course_cat_statement = f'INSERT INTO COURSE_CATEGORIES (course_id, category_id) VALUES (?, ?)'
        delete_course_cat_statement = f'DELETE FROM COURSE_CATEGORIES WHERE course_id=? and category_id=?'

        self.cursor.execute(course_statement,
                            (obj.name, obj.title, obj.text, obj.links,
                             obj.__class__.__name__.lower().replace('course', ''), obj.id))
        course_cats = CategoryMapper(self.connection).get_by_course_id(obj.id)
        course_subs = UserMapper(self.connection).get_subscribers_id_by_course_id(obj.id)

        for sub in course_subs:
            if sub not in [x.id for x in obj.subscribers]:
                self.cursor.execute(delete_subscibers_statement, (sub, obj.id))

        for subscriber in obj.subscribers:
            if subscriber.id not in course_subs:
                self.cursor.execute(insert_subscibers_statement, (subscriber.id, obj.id))

        for category in obj.categories:
            if category.id not in [item.id for item in course_cats]:
                self.cursor.execute(insert_course_cat_statement, (obj.id, category.id))

        for category in course_cats:
            if category.id not in [x.id for x in obj.categories]:
                self.cursor.execute(delete_course_cat_statement, (obj.id, category.id))

        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM COURSES WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class CategoryMapper(DataMapper):
    def get_by_id(self, id):
        statement = f'SELECT name, id FROM CATEGORIES WHERE id=?'

        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return c.Category(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def get_by_name(self, name):
        statement = f'SELECT name, id FROM CATEGORIES WHERE name=?'

        self.cursor.execute(statement, (name,))
        result = self.cursor.fetchone()
        if result:
            return c.Category(*result)
        else:
            raise RecordNotFoundException(f'record with name={name} not found')

    def get_by_course_id(self, id):
        statement = f'SELECT cat.id, cat.name ' \
                    f'FROM CATEGORIES as cat, course_categories as c_cat ' \
                    f'WHERE c_cat.course_id=? and cat.id = c_cat.category_id'
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchall()
        if result:
            return [c.Category(item[1], item[0]) for item in result]

    def get_all(self):
        statement = f'SELECT name, id FROM CATEGORIES'
        categories = []

        self.cursor.execute(statement)
        result = self.cursor.fetchall()
        if result:
            for item in result:
                categories.append(c.Category(*item))
        return categories

    def create(self, obj):
        statement = f'INSERT INTO CATEGORIES (name) VALUES (?)'
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f'UPDATE CATEGORIES SET name=? WHERE id=?'
        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f'DELETE FROM CATEGORIES WHERE id=?'
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)
