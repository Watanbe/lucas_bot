from constants.constants import PAYMENT_STATUS_CREATED
from helpers.password_generators import PasswordGenerator

class UserDTO:
    def __init__(self, username, chat_id):
        self.username = username
        self.chat_id = str(chat_id)
        self.password = PasswordGenerator()
        self.payment_status = PAYMENT_STATUS_CREATED
        self.payment_checkout_uri = ""
        self.payment_id = ""

    def __repr__(self):
        return f"PaymentDTO(username={self.username}, chat_id={self.chat_id}, password={self.password}, payment_status={self.payment_status}, payment_id={self.payment_id}, payment_checkout_uri={self.payment_checkout_uri})"