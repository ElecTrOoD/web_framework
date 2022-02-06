class SingletonByName(type):
    def __new__(cls, name, bases, dict):
        dict['__deepcopy__'] = dict['__copy__'] = lambda self, *args: self
        return super(SingletonByName, cls).__new__(cls, name, bases, dict)

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]
