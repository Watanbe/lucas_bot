from peewee import MySQLDatabase

# Configuração da instância do banco de dados
database = MySQLDatabase(
    database='posts',
    user='root',
    password='123456789',
    host='ec2-3-93-143-49.compute-1.amazonaws.com',
    port=3306
)
