from constants.constants import BOT_API_KEY, PAYMENT_STATUS_PAYD, PAYMENT_STATUS_ERROR
import telebot
from flask import Flask, request, render_template
from services.user_service import UserService
from DTO.userDTO import UserDTO

import logging

app = Flask(__name__)

bot = telebot.TeleBot(BOT_API_KEY)

logging.basicConfig(filename='/var/www/lucas_bot/webhook/app.log', level=logging.DEBUG)

@app.route('/webhook/success', methods=['GET', 'POST'])
def success():
    user_service = UserService()
    preference_id = request.args.get('preference_id')
    user = user_service.get_user_by_preference_id(preference_id)
    user.payment_status = PAYMENT_STATUS_PAYD
    user.save()

    user_dto = UserDTO(user.username, user.chat_id)
    user_dto.payment_id = user.payment_id
    user_dto.payment_status = user.payment_status
    user_dto.payment_checkout_uri = user.payment_checkout_uri

    try:
        user_service.change_password(user_dto)
    except Exception as e:
        logging.error("Erro na troca de senha", e)

    bot.send_message(user.chat_id, f"""
Olá {user.username}, seu pagamento foi aprovado.

suas credenciais são: 
usuário - {user_dto.username}
senha - {user_dto.password}
    """)
    return render_template('success.html')

@app.route('/webhook/failure')
def failure():
    user_service = UserService()
    preference_id = request.args.get('preference_id')

    user = user_service.get_user_by_preference_id(preference_id)

    print(f"Preference id: {preference_id}")
    print(f"User: {user}")
    user.payment_status = PAYMENT_STATUS_ERROR
    user.save()
    bot.send_message(user.chat_id, f"""
Olá {user.username}, seu pagamento foi recusado.

Segue o link para tentar novamente: {user.payment_checkout_uri}
    """)
    return render_template('success.html')

if __name__ == '__main__':
    context = ('/home/eduardo/projects/freela/lucas_crud/bot/bot/certificate.crt', '/home/eduardo/projects/freela/lucas_crud/bot/bot/certificate.key')
    # app.run(port=5000, debug=True, ssl_context=context)
    app.run(port=5000)