
# example '<path>': {'controller': <controller func>, 'allowed_methods': (<HTTP method>)}
#         '/': {'controller': index, 'allowed_methods': ('GET', )},

from main.controllers import about_page, index_page

urlpatterns = {
    '/': {'controller': index_page, 'allowed_methods': ('GET', )},
    '/about/': {'controller': about_page, 'allowed_methods': ('GET', 'POST')}
}
