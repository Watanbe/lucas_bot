import mercadopago
from constants.payment_constants import ACCESS_TOKEN
from constants.product_constants import PRODUCT_PRICE, PRODUCT_TITLE, PRODUCT_CURRENCY
class PaymentService:
    def __new__(cls):
        sdk = mercadopago.SDK(access_token=ACCESS_TOKEN)

        payment_data = {
            "items": [
                {
                    "id": "1",
                    "title": PRODUCT_TITLE,
                    "quantity": 1,
                    "currency_id": PRODUCT_CURRENCY,
                    "unit_price": PRODUCT_PRICE
                }
            ],
            "back_urls": {
                "success": "https://127.0.0.1:5000/webhook/success",
                "failure": "https://127.0.0.1:5000/webhook/failure"
            },
            "auto_return": "all"
        }

        preference_response = sdk.preference().create(payment_data)
        preference = preference_response["response"]

        return {
            "id": preference["id"],
            "init_point": preference["init_point"],
            "sandbox_init_point": preference["sandbox_init_point"]
        }