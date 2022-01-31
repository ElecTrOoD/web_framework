# example '<path>': {'controller': <controller func>, 'allowed_methods': (<HTTP method>)}
#         '/': {'controller': index, 'allowed_methods': ('GET', )},

from main.controllers import IndexPage, AboutPage, ContactsPage

urlpatterns = {
    '/': {'controller': IndexPage, 'allowed_methods': ('GET',)},
    '/about/': {'controller': AboutPage, 'allowed_methods': ('GET', 'POST')},
    '/contacts/': {'controller': ContactsPage, 'allowed_methods': ('GET', 'POST')}
}


