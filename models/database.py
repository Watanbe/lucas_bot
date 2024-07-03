from peewee import MySQLDatabase

# Configuração da instância do banco de dados
database = MySQLDatabase(
    database='posts',
    user='root',
    password='root',
    host='localhost',
    port=3306
)
