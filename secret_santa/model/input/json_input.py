###
# intend to be a base class for all inputs
###
from secret_santa.response import ErrorException


class JsonInput():
    id = None

    def __init__(self, identifier=None):
        self.id = identifier

    def init_from_json(self, json_input):
        missing_keys = []
        for key, value in self.__dict__.items():
            if value is not None and json_input.get(key) is None:
                missing_keys.append(key)
            self.__dict__[key] = json_input.get(key)
        if len(missing_keys) > 0:
            raise ErrorException("Missing the following keys: {keys}"
                                 .format(keys=missing_keys), 400)
