from app.settings import fronts
from app.urls import urlpatterns


def get_fronts():
    return fronts


def get_routes():
    return urlpatterns


class NotFoundPage:
    def __call__(self, request):
        return '404 Not Found', b'404 page not found'


class Redirect:
    def __call__(self, request):
        return '301 Moved Permanently', b'Redirected'
