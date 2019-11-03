from secret_santa.response import Response


class SuccessResponse(Response):
    def __init__(self, message, status_code=200, success=True):
        data = {"success": success, "message": message}
        super().__init__(status_code, data)
