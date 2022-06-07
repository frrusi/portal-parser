import hashlib
import re
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

    @staticmethod
    def check_password_steps(password):
        length_error = len(password) >= 8
        uppercase_error = re.search(r"[A-Z]", password) is not None
        lowercase_error = re.search(r"[a-z]", password) is not None
        digit_error = re.search(r"\d", password) is not None
        symbol_error = re.search(r"[!@#$%^&*]", password) is not None

        return {
            'length_error': length_error,
            'uppercase_error': uppercase_error,
            'lowercase_error': lowercase_error,
            'digit_error': digit_error,
            'symbol_error': symbol_error,
        }

