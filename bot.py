import telebot
from DTO.userDTO import UserDTO
from services.user_service import UserService
from constants.constants import BOT_API_KEY, PAYMENT_STATUS_CREATED, PAYMENT_STATUS_ERROR, PAYMENT_STATUS_PAYD

bot = telebot.TeleBot(BOT_API_KEY)

@bot.message_handler(commands=["comprar"])
def buy(message):
    user_service = UserService()
    user = message.from_user
    chat = message.chat

    user_dto = UserDTO(username=user.username, chat_id=chat.id)

    has_user = user_service.get_user(user_dto)
    if (has_user == None):
        user = user_service.create_user(user_dto)
        bot.send_message(chat.id, f"""
        Olá {user.username},
        
    Segue o seu link de pagamento: {user.payment_checkout_uri}
    
    Após efetuar o pagamento liberaremos o seu acesso
        """)
    elif (has_user.payment_status == PAYMENT_STATUS_CREATED or has_user.payment_status == PAYMENT_STATUS_ERROR):
        bot.send_message(chat.id, f"""
        Olá {has_user.username},
Você já realizou o seu cadastro anteriormente, o próximo passo será realizar o pagamento.
Segue o seu link de pagamento: {has_user.payment_checkout_uri}

Após efetuar o pagamento liberaremos o seu acesso
        """)
    else:
        bot.send_message(chat.id, f"""
        Olá {has_user.username},
        
Você já realizou o seu cadastro anteriormente, e o pagamento já foi realizado.
Caso não lembre as suas credenciais use o comando /redefinir para redefinirmos sua senha.     
        """)

@bot.message_handler(commands=["redefinir"])
def change_password(message):
    user_service = UserService()

    user = message.from_user
    chat = message.chat

    user_dto = UserDTO(username=user.username, chat_id=chat.id)

    has_user = user_service.get_user(user_dto)

    if (has_user == None):
        bot.send_message(chat.id, f"""
    Olá {user.username},
    
    Não encontramos o seu perfil.

    Digite /comprar para criar o seu acesso.
    """)
    
    elif (has_user != None and has_user.payment_status == PAYMENT_STATUS_CREATED ):
        bot.send_message(chat.id, f"""
        Olá {has_user.username},
Seu cadastro ainda não está ativo, para ativar realize o pagamento.
Segue o seu link de pagamento: {has_user.payment_checkout_uri}

Após efetuar o pagamento liberaremos o seu acesso.
        """)

    else:

        user = user_service.change_password(user_dto)

        bot.send_message(chat.id, f"""
        Olá {user.username},

    suas credenciais são: 
    usuário - {user.username}
    senha - {user.password}
        """)

@bot.message_handler(commands=["cobranca"])
def payment_link(message):
    user_service = UserService()

    user = message.from_user
    chat = message.chat

    user_dto = UserDTO(username=user.username, chat_id=chat.id)

    has_user = user_service.get_user(user_dto)

    if (has_user == None):
        bot.send_message(chat.id, f"""
    Olá {user.username},
    
    Não encontramos o seu perfil.

    Digite /comprar para criar o seu acesso.
    """)
    elif (has_user != None and has_user.payment_status == PAYMENT_STATUS_PAYD ):
        bot.send_message(chat.id, f"""
    Olá {user.username},
    
    Você já tem cadastro ativo, caso não lembre as suas credenciais digite /redefinir
    """)
    else:
        payment_link = user_service.get_payment_link(user_dto)
        bot.send_message(chat.id, f"""
        Olá {user.username},

    Segue o seu link de pagamento: {payment_link}

    Após efetuar o pagamento liberaremos o seu acesso
        """)


def verify(message):
    user = message.from_user

    if (user.is_bot == True):
        return False

    return True

@bot.message_handler(func=verify)
def start(message):
    user_service = UserService()
    user = message.from_user
    chat = message.chat

    user_dto = UserDTO(username=user.username, chat_id=chat.id)

    user = user_service.get_user(user_dto)

    if (user is not None and user.payment_status == PAYMENT_STATUS_PAYD):
        bot.send_message(message.chat.id, """
    Verificamos que você já tem cadastro ativo, segue o comando para redefinir a senha 
    /redefinir Redefinir senha
        """)
    elif (user is not None and user.payment_status == PAYMENT_STATUS_CREATED):
        bot.send_message(message.chat.id, """
    Escolha uma opção para continuar (Clique no item em azul):
    /cobranca Enviar cobrança novamente
        """)
    else:
        bot.send_message(message.chat.id, """
    Escolha uma opção para continuar (Clique no item em azul):
    /comprar Comprar o app
        """)

bot.polling()