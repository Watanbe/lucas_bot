from constants.constants import PASSWORD_LENGTH
import random
import string
class PasswordGenerator:
    def __new__(cls):
        character_list = string.ascii_lowercase + string.ascii_uppercase + string.digits
        password_chars = []
        for i in range(PASSWORD_LENGTH):
            password_chars.append(random.choice(character_list))

        return "".join(password_chars)