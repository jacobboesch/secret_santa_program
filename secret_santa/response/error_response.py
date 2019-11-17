from secret_santa.response import SuccessResponse


class ErrorResponse(SuccessResponse):
    def __init__(self, status_code, message):
        super().__init__(message, status_code, False)
