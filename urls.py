# example '<path>': {'controller': <controller func>, 'allowed_methods': (<HTTP method>)}
#         '/': {'controller': index, 'allowed_methods': ('GET', )},
from courses.controllers import CoursesListPage, CoursesCreatePage, CoursePage, CourseDelete, \
    CategoriesListPage, CategoryCreatePage, CategoryDelete, CoursesCopyPage
from main.controllers import IndexPage, AboutPage, ContactsPage

urlpatterns = {
    '/': {'controller': IndexPage, 'allowed_methods': ('GET',)},
    '/about/': {'controller': AboutPage, 'allowed_methods': ('GET', 'POST')},
    '/contacts/': {'controller': ContactsPage, 'allowed_methods': ('GET', 'POST')},
    '/courses/': {'controller': CoursesListPage, 'allowed_methods': ('GET',)},
    '/course/': {'controller': CoursePage, 'allowed_methods': ('GET',)},
    '/courses/create/': {'controller': CoursesCreatePage, 'allowed_methods': ('GET', 'POST')},
    '/courses/copy/': {'controller': CoursesCopyPage, 'allowed_methods': ('POST',)},
    '/courses/delete/': {'controller': CourseDelete, 'allowed_methods': ('GET',)},
    '/categories/': {'controller': CategoriesListPage, 'allowed_methods': ('GET',)},
    '/categories/create/': {'controller': CategoryCreatePage, 'allowed_methods': ('GET', 'POST')},
    '/categories/delete/': {'controller': CategoryDelete, 'allowed_methods': ('GET',)},
}
