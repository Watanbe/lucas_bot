from peewee import MySQLDatabase

# Configuração da instância do banco de dados
database = MySQLDatabase(
    database='posts',
    user='root',
    password='123456789',
    host='127.0.0.1',
    port=3306
)
