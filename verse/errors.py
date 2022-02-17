class InvalidFormException(Exception):
    def __init__(self, message):
        super().__init__(f'Form error: {message}')