import main.controllers as main

urlpatterns = {
    '/': main.index_page,
    '/about/': main.about_page
}
