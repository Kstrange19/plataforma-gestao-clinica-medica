import sys
from datetime import datetime, date
import mysql.connector
from mysql.connector import Error

def connect_db():
    try:
        cnx = mysql.connector.connect(
            host="127.0.0.1",
            port=3308,
            user="root",
            password="123",
            database="clinica_medica",
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

def register_doctor(name, specialty, phone, email):
    try:
        sql = "INSERT INTO medicos (nome, especialidade, telefone, email) VALUES (%s, %s, %s, %s)"
        credential = "SELECT * FROM medicos WHERE nome = %s"
        values = (name, specialty, phone, email)
        cursor.execute(sql, values)
        cnx.commit()
        print("Médico registrado com sucesso.\n")
        cursor.execute(credential, (name,))
        credential = cursor.fetchall()
        for row in credential:
            print(f"= Credenciais do médico =\nID: {row[0]}\nNome: {row[1]}\nEspecialidade: {row[2]}\nTelefone: {row[3]}\nEmail: {row[4]}")
    except Error as e:
        print(f"Erro ao registrar médico: {e}")

def verificar_disponibilidade_para_agendamento(medico_id, data_consulta, hora_consulta):
    # 1. Descobrir qual é o dia da semana dessa data (Python datetime)
    # Supondo que você já converteu a data para dia da semana (ex: 'Segunda')
    dia_semana = data_consulta.strftime('%A')  # Exemplo: 'Monday', 'Tuesday', etc.

    # 2. Verificar se existe horário cadastrado
    query_horario = """
        SELECT id FROM disponibilidade_medicos 
        WHERE medico_id = %s 
        AND dia_semana = %s
        AND horario_inicio <= %s 
        AND horario_fim > %s
    """
    cursor.execute(query_horario, (medico_id, dia_semana, hora_consulta, hora_consulta))
    if not cursor.fetchone():
        return False # Médico não atende nesse horário

    # 3. Verificar se já existe consulta marcada (conflito)
    query_conflito = """
        SELECT id FROM consultas 
        WHERE medico_id = %s 
        AND data_consulta = %s 
        AND horario = %s
        AND status != 'Cancelada'
    """
    cursor.execute(query_conflito, (medico_id, data_consulta, hora_consulta))
    if cursor.fetchone():
        return False # Já tem alguém marcado

    return True # Livre!

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

menu = {1: 'Verificar disponibilidade', 2: 'Cadastrar cliente', 3: 'Cadastrar médico', 0: 'Sair do programa'}

while True:
    print("\nBem-vindo ao sistema de gestão de clínica médica.")
    for key, value in menu.items():
        print(f"{key}. {value}")
    try:
        choice = int(input("Escolha uma opção: "))
    except ValueError:
        print("Opção inválida. Tente novamente.")
        continue
    if choice == 1:
        medico_id = input("ID do Médico: ")
        data_input = input("Data da Consulta (YYYY-MM-DD): ")
        hora_input = input("Hora da Consulta (HH:MM:SS): ")
        data_consulta = datetime.strptime(data_input, '%Y-%m-%d').date()
        hora_consulta = datetime.strptime(hora_input, '%H:%M:%S').time()
        disponivel = verificar_disponibilidade_para_agendamento(medico_id, data_consulta, hora_consulta)
        if disponivel:
            print("O horário está disponível para agendamento.")
        else:
            print("O horário não está disponível para agendamento.")
    elif choice == 2:
        name = input("Nome: ")
        age = input("Idade: ")
        email = input("Email: ")
        phone = input("Telefone: ")
        register_client(name, age, email, phone)
    elif choice == 3:
        name = input("Nome: ")
        specialty = input("Especialidade: ")
        phone = input("Telefone: ")
        email = input("Email: ")
        register_doctor(name, specialty, phone, email)
    elif choice == 0:
        print("Saindo do programa.")
        break