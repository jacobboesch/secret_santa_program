import json


class Response():
    def __init__(self, status_code, data):
        self.status_code = status_code
        self.data = data
        try:
            self.json_data = json.dumps(self.data)
        except Exception:
            self.json_data = None
