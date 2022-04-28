import hashlib
import uuid


def hash_password(password):
    salt = uuid.uuid4().hex
    return hashlib.sha512(salt.encode() + password.encode()).hexdigest() + ':' + salt


def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha512(salt.encode() + user_password.encode()).hexdigest()


def get_answer_check_password(hashed_password, entered_password, config):
    if check_password(hashed_password, entered_password):
        return config.successful_code
    else:
        return config.error_code
