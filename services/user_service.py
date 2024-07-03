from .payment_service import PaymentService
from DTO.userDTO import UserDTO
from models.users import Users
from peewee import DoesNotExist
from passlib.hash import bcrypt
import requests
import json
from constants.constants import API_URI
class UserService:

    def create_user(self, user_dto: UserDTO):
        payment_preference = PaymentService()
        user_dto.payment_id = payment_preference["id"]
        user_dto.payment_checkout_uri = payment_preference["sandbox_init_point"]

        self.user_dto = user_dto

        url = API_URI + "register"

        self.send_to_api(url)

        return user_dto

    def get_user(self, user_dto: UserDTO):
        try:
            user = Users.select().where(Users.username == user_dto.username, Users.chat_id == user_dto.chat_id).get()
            return user
        except DoesNotExist:
            return None

    def change_password(self, user_dto: UserDTO):
        user = self.get_user(user_dto)

        user_dto.payment_id = user.payment_id
        user_dto.payment_status = user.payment_status
        user_dto.payment_checkout_uri = user.payment_checkout_uri

        self.user_dto = user_dto

        url = API_URI + f"update-password/{user.id}"

        self.send_to_api(url)

        return user_dto

    def get_payment_link(self, user_dto: UserDTO):
        user = self.get_user(user_dto)
        return user.payment_checkout_uri

    def get_user_by_preference_id(self, preference_id):
        try:
            user = Users.select().where(Users.payment_id == preference_id).get()
            return user
        except DoesNotExist:
            return None

    def send_to_api(self, url):
        data = json.dumps({
            'username': self.user_dto.username,
            'password': self.user_dto.password,
            'chat_id': self.user_dto.chat_id,
            'payment_status': self.user_dto.payment_status,
            'payment_checkout_uri': self.user_dto.payment_checkout_uri,
            'payment_id': self.user_dto.payment_id
        })

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=data)