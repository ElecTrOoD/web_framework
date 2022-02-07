class Layout:
    def __init__(self, prefix='/'):
        self.prefix = prefix
        self.urls = {}

    def route(self, url, methods=('GET',)):
        def wrapper(wrapped):
            new_url = {f'{self.prefix}{url}/'.replace('///', '/').replace('//', '/'): {'controller': wrapped,
                                                                                       'allowed_methods': methods}}
            self.urls.update(new_url)
            return wrapped

        return wrapper

    def get_urls(self):
        return self.urls
