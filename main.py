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
            database="clinica",
        )
        print("Conexão bem-sucedida ao banco de dados.")
        return cnx
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def register_client(name, age, email, phone, blood_type):
    try:
        sql = "INSERT INTO pacientes (nome, cpf, telefone, data_nascimento, senha_hash) VALUES (%s, %s, %s, %s, %s)"
        values = (name, "00000000000", phone, date.today(), "dummyhash")
        cursor.execute(sql, values)
        cnx.commit()
        print("Paciente registrado com sucesso.")
    except Error as e:
        print(f"Erro ao registrar paciente: {e}")
# Função para preencher a ficha médica do paciente
def fill_medical_record(patient_id):
    # Perguntas baseadas no catálogo de condições
    print("Por favor, responda às perguntas de triagem:")
    
    # Pergunta 1: Fumante?
    response = input("O paciente é fumante? (s/n): ").lower()
    if response == 's':
        add_to_medical_record(patient_id, 'Tabagismo', 'Fumante', 'Paciente informou ser fumante')
    # Pergunta 2: Consumo de Álcool?
    response = input("Consome bebida alcoólica? (s/n): ").lower()
    if response == 's':
        frequency = input("Com qual frequência? ")
        add_to_medical_record(patient_id, 'Consumo de Álcool', 'Outros', f"Frequência: {frequency}")
    
    # Pergunta 3: Alergias?
    response = input("Possui alguma alergia? (s/n): ").lower()
    if response == 's':
        allergy = input("Qual alergia? ")
        add_to_medical_record(patient_id, 'Alergia Genérica', 'Alergia', f"Alergia a: {allergy}")

    print("Ficha médica atualizada com sucesso!")
# Função auxiliar para gravar no banco (Relacionamento N:M)
def add_to_medical_record(patient_id, condition_name, condition_type, note):
    try:
        cursor.execute("SELECT id FROM catalogo_condicoes WHERE nome = %s", (condition_name,))
        result = cursor.fetchone()
        if result:
            condition_id = result[0]

            # Insere na tabela associativa (FICHA)
            sql = "INSERT INTO ficha_paciente (cliente_id, condicao_id, observacoes) VALUES (%s, %s, %s)"
            cursor.execute(sql, (patient_id, condition_id, note))
            cnx.commit()
        else:
            print(f"Aviso: Condição '{condition_name}' não encontrada no catálogo.")
    except Error as e:
        print(f"Erro ao salvar no prontuário: {e}")

def register_doctor(name, crm, specialty_id, phone, city):
    try:
        sql = "INSERT INTO medicos (nome, crm, especialidade_id, telefone, cidade, senha_hash) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (name, crm, specialty_id, phone, city, "dummyhash"))
        cnx.commit()
        print("Médico registrado com sucesso.")
    except Error as e:
        print(f"Erro ao registrar médico: {e}")

def schedule_appointment(doctor_id, patient_id, appointment_date, appointment_time):
    try:
        sql = "INSERT INTO consultas (medico_id, paciente_id, data_consulta, hora_consulta, status) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (doctor_id, patient_id, appointment_date, appointment_time, 'agendado'))
        cnx.commit()
        print("Consulta agendada com sucesso.")
    except Error as e:
        print(f"Erro ao agendar consulta: {e}")

def check_appointment_availability(doctor_id, appointment_date, appointment_time):
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
    weekday = days_translation[english_day]
    
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
       return False
    # Verificar se já existe consulta marcada (prevenir conflito)
    conflict_query = """
        SELECT id FROM consultas 
        WHERE medico_id = %s 
        AND data_consulta = %s 
        AND hora_consulta = %s
        AND status != 'cancelado'
    """
    cursor.execute(conflict_query, (doctor_id, appointment_date, appointment_time))
    if cursor.fetchone():
        return False

    return True

def list_full_appointments():
    try:
        cursor.execute("SELECT * FROM view_consultas_completas")
        results = cursor.fetchall()
        if not results:
            print("Nenhuma consulta encontrada.")
            return
        print("\n=== Consultas Registradas ===")
        for row in results:
            print(f"ID Consulta: {row[0]}")
            print(f"Paciente: {row[1]}")
            print(f"Médico: {row[2]}")
            print(f"Especialidade: {row[3]}")
            print(f"Data: {row[4]}")
            print(f"Hora: {row[5]}")
            print(f"Status: {row[6]}")
            print("---------------------------")
    except Error as e:
        print(f"Erro ao listar consultas: {e}")

# Conexão
cnx = connect_db()
if cnx is None:
    sys.exit(1)

cursor = cnx.cursor()

# Menu principal
menu = {
    1: 'Verificar disponibilidade',
    2: 'Agendar consulta',
    3: 'Cadastrar paciente',
    4: 'Cadastrar médico',
    5: 'Listar consultas completas',
    0: 'Sair do programa'
}

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
        is_available = check_appointment_availability(doctor_id, appointment_date, appointment_time)
        if is_available:
            print("O horário está disponível para agendamento.")
        else:
            print("O horário não está disponível para agendamento.")

    elif choice == 2:
        try:
            doctor_id = int(input("ID do Médico: "))
            patient_id = int(input("ID do Paciente: "))
        except ValueError:
            print("ID inválido. Tente novamente.")
            continue
        date_input = input("Data da Consulta (YYYY-MM-DD): ")
        time_input = input("Hora da Consulta (HH:MM:SS): ")
        appointment_date = datetime.strptime(date_input, '%Y-%m-%d').date()
        appointment_time = datetime.strptime(time_input, '%H:%M:%S').time()
        if check_appointment_availability(doctor_id, appointment_date, appointment_time):
            schedule_appointment(doctor_id, patient_id, appointment_date, appointment_time)
        else:
            print("O horário não está disponível para agendamento.")

    elif choice == 3:
        name = input("Nome: ")
        age = input("Idade: ")
        email = input("Email: ")
        phone = input("Telefone: ")
        blood_type = input("Tipo Sanguíneo: ")
        register_client(name, age, email, phone, blood_type)

    elif choice == 4:
        name = input("Nome: ")
        crm = input("CRM: ")
        specialty_id = int(input("ID da Especialidade: "))
        phone = input("Telefone: ")
        city = input("Cidade: ")
        register_doctor(name, crm, specialty_id, phone, city)

    elif choice == 5:
        list_full_appointments()

    elif choice == 0:
        print("Saindo do programa.")
        break
 
