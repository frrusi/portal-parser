import os


class AuthError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Exceptions:
    def __init__(self, config):
        self.config = config

    def check_file_path(self, file_path: str):
        if not os.path.exists(file_path):
            raise FileNotFoundError(self.config.file_not_found_error)

    def check_auth(self, response_code: str):
        if response_code != self.config.successful_code:
            raise AuthError(self.config.auth_error)

    @staticmethod
    def check_none(value):
        if value is None:
            raise ValueError("Value must not be None")
