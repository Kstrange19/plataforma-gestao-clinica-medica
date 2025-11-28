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
        sql = "INSERT INTO clientes (nome, idade, email, telefone, tipo_sanguineo) VALUES (%s, %s, %s, %s, %s)"
        values = (name, age if age != '' else None, email, phone)
        cursor.execute(sql, values)
        cnx.commit()
        print("Cliente registrado com sucesso.")
    except Error as e:
        print(f"Erro ao registrar cliente: {e}")

# Função para preencher a ficha médica do paciente
def fill_medical_record(client_id):
    # Perguntas baseadas no catálogo de condições
    print("Por favor, responda às perguntas de triagem:")
    
    # Pergunta 1: Fumante?
    response = input("O paciente é fumante? (s/n): ").lower()
    if response == 's':
        add_to_medical_record(client_id, 'Tabagismo', 'Fumante', 'Paciente informou ser fumante')

    # Pergunta 2: Consumo de Álcool?
    response = input("Consome bebida alcoólica? (s/n): ").lower()
    if response == 's':
        frequency = input("Com qual frequência? ")
        add_to_medical_record(client_id, 'Consumo de Álcool', 'Outros', f"Frequência: {frequency}")

    # Pergunta 3: Alergias?
    response = input("Possui alguma alergia? (s/n): ").lower()
    if response == 's':
        allergy = input("Qual alergia? ")
        # Aqui o ideal seria buscar no catálogo, mas vamos simplificar inserindo diretamente
        add_to_medical_record(client_id, 'Alergia Genérica', 'Alergia', f"Alergia a: {allergy}")

    print("Ficha médica atualizada com sucesso!")

# Função auxiliar para gravar no banco (Relacionamento N:M)
def add_to_medical_record(client_id, condition_name, condition_type, note):
    try:
        cursor.execute("SELECT id FROM catalogo_condicoes WHERE nome = %s", (condition_name,))
        result = cursor.fetchone()
        
        if result:
            condition_id = result[0]
            
            # Insere na tabela associativa (FICHA)
            sql = """
                INSERT INTO ficha_paciente (cliente_id, condicao_id, observacoes) 
                VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (client_id, condition_id, note))
            cnx.commit()
        else:
            print(f"Aviso: Condição '{condition_name}' não encontrada no catálogo.")
            
    except Error as e:
        print(f"Erro ao salvar no prontuário: {e}")

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

def schedule_appointment(doctor_id, client_id, appointment_date, appointment_time):
    try:
        sql = "INSERT INTO consultas (medico_id, cliente_id, data_consulta, horario, status) VALUES (%s, %s, %s, %s, %s)"
        values = (doctor_id, client_id, appointment_date, appointment_time, 'Agendada')
        cursor.execute(sql, values)
        cnx.commit()
        print("Consulta agendada com sucesso.")
    except Error as e:
        print(f"Erro ao agendar consulta: {e}")

def check_appointment_availability(doctor_id, appointment_date, appointment_time):
    """ Verifica se o médico está disponível para agendamento na data e hora fornecidas. """
    days_translation = {
    'Monday': 'Segunda',
    'Tuesday': 'Terca',
    'Wednesday': 'Quarta',
    'Thursday': 'Quinta',
    'Friday': 'Sexta',
    'Saturday': 'Sabado',
    'Sunday': 'Domingo'
    }
    english_day = appointment_date.strftime('%A')
    weekday = days_translation[english_day] # Busca em Português

    # Verifica se existe horário cadastrado
    time_query = """
        SELECT id FROM horarios_atendimento 
        WHERE medico_id = %s 
        AND dia_semana = %s
        AND horario_inicio <= %s 
        AND horario_fim > %s
    """

    cursor.execute(time_query, (doctor_id, weekday, appointment_time, appointment_time))
    if not cursor.fetchone():
        return False # Médico não atende nesse horário

    # Verificar se já existe consulta marcada (prevenir conflito)
    conflict_query = """
        SELECT id FROM consultas 
        WHERE medico_id = %s 
        AND data_consulta = %s 
        AND horario = %s
        AND status != 'Cancelada'
    """
    cursor.execute(conflict_query, (doctor_id, appointment_date, appointment_time))
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

menu = {1: 'Verificar disponibilidade', 2: 'Agendar consulta', 3: 'Cadastrar cliente', 4: 'Cadastrar médico', 0: 'Sair do programa'}

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
        try:
            doctor_id = int(input("ID do Médico: "))
        except ValueError:
            print("ID inválido. Tente novamente.")
            continue
        date_input = input("Data da Consulta (YYYY-MM-DD): ")
        time_input = input("Hora da Consulta (HH:MM:SS): ")
        appointment_date = datetime.strptime(date_input, '%Y-%m-%d').date()
        appointment_time = datetime.strptime(time_input, '%H:%M:%S').time()
        try:
            is_available = check_appointment_availability(doctor_id, appointment_date, appointment_time)
            if is_available:
                print("O horário está disponível para agendamento.")
            else:
                print("O horário não está disponível para agendamento.")
        except Error as e:
            print(f"Erro ao verificar disponibilidade: {e}")
    elif choice == 2:
        try:
            doctor_id = int(input("ID do Médico: "))
            client_id = int(input("ID do Cliente: "))
        except ValueError:
            print("ID inválido. Tente novamente.")
            continue
        date_input = input("Data da Consulta (YYYY-MM-DD): ")
        time_input = input("Hora da Consulta (HH:MM:SS): ")
        appointment_date = datetime.strptime(date_input, '%Y-%m-%d').date() # Converte para o formato date
        appointment_time = datetime.strptime(time_input, '%H:%M:%S').time() # Converte para o formato time
        is_available = check_appointment_availability(doctor_id, appointment_date, appointment_time)
        if is_available:
            schedule_appointment(doctor_id, client_id, appointment_date, appointment_time)
        else:
            print("O horário não está disponível para agendamento.")
    elif choice == 3:
        name = input("Nome: ")
        age = input("Idade: ")
        email = input("Email: ")
        phone = input("Telefone: ")
        blood_type = input("Tipo Sanguíneo: ")
        register_client(name, age, email, phone)
    elif choice == 4:
        name = input("Nome: ")
        specialty = input("Especialidade: ")
        phone = input("Telefone: ")
        email = input("Email: ")
        register_doctor(name, specialty, phone, email)
    elif choice == 0:
        print("Saindo do programa.")
        break