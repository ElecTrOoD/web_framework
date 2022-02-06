from courses.models import SiteData
from logs import Logger
from verse import TemplateController, FormController, Layout

courses = Layout('/courses')
categories = Layout('/categories')
site = SiteData()
logger = Logger('courses-controllers')


@courses.route('/')
class CoursesListPage(TemplateController):
    template_name = 'courses/courses_list.html'

    def set_context(self):
        self.context = {'title': 'Courses'}

    def get_logic(self):
        category = self.request['request_params'].get('category')
        if category:
            self.context['courses'] = site.get_courses_by_category(category)
        else:
            self.context['courses'] = site.get_courses()
        logger.log(f'[INFO] CoursesListPage called')


@courses.route('/course')
class CoursePage(TemplateController):
    template_name = 'courses/course.html'

    def set_context(self):
        self.context = {'title': 'Course', 'course': site.get_course_by_name(self.request['request_params']['name'])}

    def get_logic(self):
        logger.log(f'[INFO] CoursePage called: {self.context["course"].name}')


@courses.route('/delete')
class CourseDelete(TemplateController):
    redirect_url = '/courses/'

    def set_context(self):
        pass

    def get_logic(self):
        site.delete_course(self.request['request_params']['name'])
        logger.log(f'[INFO] CourseDelete called: {self.request["request_params"]["name"]}')


@courses.route('/create', methods=('GET', 'POST'))
class CoursesCreatePage(FormController):
    template_name = 'courses/create_course.html'
    redirect_url = '/courses/'
    form_fields = ['name', 'title', 'text', 'categories', 'type', 'links']

    def set_context(self):
        self.context = {'title': 'Create Course', 'categories': site.get_categories()}

    def post_logic(self):
        data = self.request['form']
        site.create_course(data['type'], data['name'], data['title'], data['text'], data['categories'],
                           data['links'] if data['links'] else None)
        logger.log(f'[INFO] CoursesCreatePage called: {data["name"]}')


@courses.route('/copy')
class CoursesCopyPage(FormController):
    redirect_url = '/courses/'
    form_fields = ['name']

    def set_context(self):
        pass

    def post_logic(self):
        site.copy_course(self.request['request_params']['name'], self.request['form']['name'])
        logger.log(f'[INFO] CoursesCopyPage called: {self.request["request_params"]["name"]}')


@categories.route('/')
class CategoriesListPage(TemplateController):
    template_name = 'courses/categories_list.html'

    def set_context(self):
        self.context = {'title': 'Categories', 'categories': site.get_categories()}

    def get_logic(self):
        logger.log(f'[INFO] CoursesCreatePage called')


@categories.route('/create', methods=('GET', 'POST'))
class CategoryCreatePage(FormController):
    template_name = 'courses/create_category.html'
    redirect_url = '/categories/'
    form_fields = ['name']

    def set_context(self):
        self.context = {'title': 'Create Category'}

    def post_logic(self):
        site.create_category(self.request['form']['name'])
        logger.log(f'[INFO] CategoryCreatePage called: {self.request["form"]["name"]}')


@categories.route('/delete')
class CategoryDelete(TemplateController):
    redirect_url = '/categories/'

    def set_context(self):
        pass

    def get_logic(self):
        site.delete_category(self.request['request_params']['name'])
        logger.log(f'[INFO] CategoryDelete called: {self.request["request_params"]["name"]}')
