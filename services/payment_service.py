import mercadopago
from constants.payment_constants import ACCESS_TOKEN
from constants.product_constants import PRODUCT_PRICE, PRODUCT_TITLE, PRODUCT_CURRENCY
from constants.constants import WEBHOOK_DNS

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
                "success": f"{WEBHOOK_DNS}/webhook/success",
                "failure": f"{WEBHOOK_DNS}/webhook/failure"
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