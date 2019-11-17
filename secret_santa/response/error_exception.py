

class ErrorException(Exception):
    def __init__(self, message, status_code):
        Exception.__init__(self, message)
        self.message = message
        self.status_code = status_code
