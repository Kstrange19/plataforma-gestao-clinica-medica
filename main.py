import mysql.connector

try:
    cnx = mysql.connector.connect(
    host="127.0.0.1",  # ou "localhost"
    port="3308",         # Porta do Docker
    user="root",
    password="123", # A mesma do docker-compose
    database="Agendamentos" # O nome do banco de dados criado no container
    )
    print("Conexão bem-sucedida ao banco de dados.")
except:
    print("Erro ao conectar ao banco de dados.")
    exit(1)

cursor = cnx.cursor()
def register_client(name, age, email, phone, city):
    sql = "INSERT INTO clientes (nome, idade, email, telefone, cidade) VALUES (%s, %s, %s, %s, %s)"
    values = (name, age, email, phone, city)
    cursor.execute(sql, values)
    cnx.commit()
    print("Cliente registrado com sucesso.")

name = input("Nome: ")
age = input("Idade: ")
email = input("Email: ")
phone = input("Telefone: ")
city = input("Cidade: ")
register_client(name, age, email, phone, city)