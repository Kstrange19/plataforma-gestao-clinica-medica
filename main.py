import sys
import mysql.connector
from mysql.connector import Error

def connect_db():
    try:
        cnx = mysql.connector.connect(
            host="127.0.0.1",
            port=3308,
            user="root",
            password="123",
            database="Agendamentos",
        )
        print("Conexão bem-sucedida ao banco de dados.")
        return cnx
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def register_client(name, age, email, phone):
    try:
        sql = "INSERT INTO clientes (nome, idade, email, telefone) VALUES (%s, %s, %s, %s)"
        values = (name, age if age != '' else None, email, phone)
        cursor.execute(sql, values)
        cnx.commit()
        print("Cliente registrado com sucesso.")
    except Error as e:
        print(f"Erro ao registrar cliente: {e}")

cnx = connect_db()
if cnx is None:
    sys.exit(1)

cursor = cnx.cursor()

# Cria a tabela 'clientes' se não existir
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS clientes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(255) NOT NULL,
        idade INT,
        email VARCHAR(255),
        telefone VARCHAR(50)
    ) ENGINE=InnoDB;
    """
)

cnx.commit()

menu = {1: 'Registrar novo cliente', 2: 'Sair do programa'}

while True:
    print("Bem-vindo ao sistema de gestão de clínica médica.")
    for key, value in menu.items():
        print(f"{key}. {value}")
    try:
        choice = int(input("Escolha uma opção: "))
    except ValueError:
        print("Opção inválida. Tente novamente.")
        continue
    if choice == 1:
        name = input("Nome: ")
        age = input("Idade: ")
        email = input("Email: ")
        phone = input("Telefone: ")
        register_client(name, age, email, phone)
    elif choice == 2:
        print("Saindo do programa.")
        break