import hashlib
import uuid


class SecurityUtils:
    def __init__(self, config):
        self.config = config

    @staticmethod
    def hash_password(password):
        salt = uuid.uuid4().hex
        return hashlib.sha512(salt.encode() + password.encode()).hexdigest() + ':' + salt

    @staticmethod
    def check_password(hashed_password, user_password):
        password, salt = hashed_password.split(':')
        return password == hashlib.sha512(salt.encode() + user_password.encode()).hexdigest()

    def get_answer_check_password(self, hashed_password, entered_password):
        if self.check_password(hashed_password, entered_password):
            return self.config.successful_code
        return self.config.error_code
