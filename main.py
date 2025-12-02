import sys
from datetime import datetime
import mysql.connector
from mysql.connector import Error

# Dicionário de Tipos Sanguíneos para o menu e validação
BLOOD_TYPES = {
    1: 'A+', 2: 'A-',
    3: 'B+', 4: 'B-',
    5: 'AB+', 6: 'AB-',
    7: 'O+', 8: 'O-'
}

# Conexão com o banco de dados
def connect_db():
    try:
        cnx = mysql.connector.connect(
            host="127.0.0.1",
            port=3308,
            user="root",
            password="123",
            database="clinica_medica"
        )
        print("Conexão bem-sucedida ao banco de dados.")
        return cnx
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}", file=sys.stderr)
        return None

# Validações de Entrada
def validate_input(value, length, name):
    """Verifica se o valor é numérico e tem o comprimento correto."""
    value_clean = str(value).strip()
    if not value_clean.isdigit():
        print(f"Erro: O campo {name} deve conter apenas números.")
        return None
    if len(value_clean) != length:
        print(f"Erro: O campo {name} deve ter exatamente {length} dígitos.")
        return None
    return value_clean

def get_blood_type_from_menu():
    """Apresenta um menu e retorna o tipo sanguíneo válido."""
    print("\n--- Seleção de Tipo Sanguíneo ---")
    for key, value in BLOOD_TYPES.items():
        print(f"{key}. {value}")
    
    while True:
        try:
            choice = int(input("Escolha o número do Tipo Sanguíneo: "))
            if choice in BLOOD_TYPES:
                return BLOOD_TYPES[choice]
            else:
                print("Opção inválida. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número.")

# Cadastro de pacientes
def register_client(name, age, email, phone, blood_type, cpf, cursor, cnx):
    try:
        sql = """
            INSERT INTO pacientes
            (nome, idade, email, telefone, tipo_sanguineo, cpf, senha_hash)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (name, age, email, phone, blood_type, cpf, "dummyhash")
        cursor.execute(sql, values)
        cnx.commit()
        print("Paciente registrado com sucesso.")
    except Error as e:
        print(f"Erro ao registrar paciente: {e}")

# Cadastro de médicos
def register_doctor(name, specialty, phone, cursor, cnx):
    try:
        sql = """
            INSERT INTO medicos
            (nome, especialidade, email, telefone, senha_hash)
            VALUES (%s, %s, %s, %s, %s)
        """
        email_fake = f"{name.replace(' ', '').lower()}@clinica.com"
        cursor.execute(sql, (name, specialty, email_fake, phone, "dummyhash"))
        cnx.commit()
        print("Médico registrado com sucesso.")
    except Error as e:
        print(f"Erro ao registrar médico: {e}")

# Agendamento de consultas
def schedule_appointment(doctor_id, patient_id, appointment_date, appointment_time, motivo, cursor, cnx):
    try:
        sql = """
            INSERT INTO consultas
            (medico_id, paciente_id, data_consulta, hora_consulta, motivo, status)
            VALUES (%s, %s, %s, %s, %s, 'Agendada')
        """
        cursor.execute(sql, (doctor_id, patient_id, appointment_date, appointment_time, motivo))
        cnx.commit()
        print("Consulta agendada com sucesso.")
    except Error as e:
        print(f"Erro ao agendar consulta: {e}")

# Verificação de disponibilidade
def check_appointment_availability(doctor_id, appointment_date, appointment_time, cursor):
    days_translation = {
        'Monday': 'Segunda',
        'Tuesday': 'Terca',
        'Wednesday': 'Quarta',
        'Thursdy': 'Quinta', # <--- CORRIGIDO: Era 'Thursdy'
        'Friday': 'Sexta',
        'Saturday': 'Sabado',
        'Sunday': 'Domingo'
    }
    english_day = appointment_date.strftime('%A')
    weekday = days_translation.get(english_day, 'DiaInvalido')

    # Verifica se o médico atende nesse horário
    time_query = """
        SELECT id FROM horarios_atendimento
        WHERE medico_id = %s
        AND da_semana = %s
        AND horario_inicio <= %s
        AND horario_fim > %s
    """
    cursor.execute(time_query, (doctor_id, weekday, appointment_time, appointment_time))
    if not cursor.fetchone():
        print(f"Médico ID {doctor_id} não atende em {weekday} neste horário.")
        return False

    # Verifica conflitos com consultas já agendadas
    conflict_query = """
        SELECT id FROM consultas
        WHERE medico_id = %s
        AND data_consulta = %s
        AND hora_consulta = %s
        AND status != 'cancelado'
    """
    cursor.execute(conflict_query, (doctor_id, appointment_date, appointment_time))
    if cursor.fetchone():
        print("Já existe uma consulta agendada para este médico e horário.")
        return False

    return True

# Listagem de Médicos e Pacientes
def list_doctors(cursor):
    """Lista IDs e nomes de médicos disponíveis."""
    try:
        cursor.execute("SELECT id, nome, especialidade FROM medicos")
        results = cursor.fetchall()
        print("\n=== Médicos Cadastrados ===")
        if not results:
            print("Nenhum médico encontrado.")
            return
        for row in results:
            print(f"ID: {row[0]} | Nome: {row[1]} | Especialidade: {row[2]}")
        print("---------------------------")
    except Error as e:
        print(f"Erro ao listar médicos: {e}")

def list_patients(cursor):
    """Lista IDs e nomes de pacientes cadastrados."""
    try:
        cursor.execute("SELECT id, nome, cpf FROM pacientes")
        results = cursor.fetchall()
        print("\n=== Pacientes Cadastrados ===")
        if not results:
            print("Nenhum paciente encontrado.")
            return
        for row in results:
            print(f"ID: {row[0]} | Nome: {row[1]} | CPF: {row[2]}")
        print("---------------------------")
    except Error as e:
        print(f"Erro ao listar pacientes: {e}")

# Listagem de Horários dos Médicos
def list_doctor_availability(cursor):
    """Lista o dia da semana e o horário de atendimento de todos os médicos."""
    try:
        sql = """
            SELECT m.nome, m.especialidade, h.dia_semana, h.horario_inicio, h.horario_fim
            FROM horarios_atendimento h
            JOIN medicos m ON h.medico_id = m.id
            ORDER BY m.nome, 
                     FIELD(h.dia_semana, 'Segunda', 'Terca', 'Quarta', 'Quinta', 'Sexta', 'Sabado', 'Domingo'),
                     h.horario_inicio;
        """
        cursor.execute(sql)
        results = cursor.fetchall()
        
        if not results:
            print("Nenhum horário de atendimento encontrado.")
            return

        print("\n=== Horários de Atendimento dos Médicos ===")
        
        current_doctor = None
        
        for nome, especialidade, dia, inicio, fim in results:
            if nome != current_doctor:
                if current_doctor is not None:
                    print("---")
                print(f"**Médico:** {nome} ({especialidade})")
                current_doctor = nome
            
            # Formata os horários para melhor leitura
            inicio_str = str(inicio)
            fim_str = str(fim)
            
            print(f"  - {dia}: {inicio_str[:5]} às {fim_str[:5]}")
            
        print("===========================================")
        
    except Error as e:
        print(f"Erro ao listar horários de atendimento: {e}")

# Listar consultas completas
def list_full_appointments(cursor):
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
            print(f"Motivo: {row[6]}")
            print(f"Status: {row[7]}")
            print("---------------------------")
    except Error as e:
        print(f"Erro ao listar consultas: {e}")

# Inicialização
cnx = connect_db()
if cnx is None:
    sys.exit(1)

cursor = cnx.cursor()

menu = {
    1: 'Verificar disponibilidade',
    2: 'Agendar consulta',
    3: 'Cadastrar paciente',
    4: 'Cadastrar médico',
    5: 'Listar consultas (Completo)',
    6: 'Listar Médicos e Pacientes (Para IDs)',
    7: 'Listar Horários dos Médicos',
    0: 'Sair do programa'
}

# Loop principal
while True:
    print("\nBem-vindo ao sistema de gestão de clínica médica.")
    for key, value in menu.items():
        print(f"{key}. {value}")

    try:
        choice = int(input("Escolha uma opção: "))
    except ValueError:
        print("Opção inválida.")
        continue

    if choice == 1:
        # Verifica disponibilidade
        doctor_id = int(input("ID do Médico: "))
        date_input = input("Data (YYYY-MM-DD): ")
        time_input = input("Hora (HH:MM:SS): ")
        try:
            appointment_date = datetime.strptime(date_input, '%Y-%m-%d').date()
            appointment_time = datetime.strptime(time_input, '%H:%M:%S').time()
            if check_appointment_availability(doctor_id, appointment_date, appointment_time, cursor):
                print("Horário disponível.")
            else:
                pass
        except ValueError:
            print("Formato de data ou hora inválido. Tente novamente.")

    elif choice == 2:
        # Agendar consulta - Validação de ID
        print("\n--- Agendamento de Consulta ---")
        try:
            doctor_id = int(input("ID do Médico: "))
            patient_id = int(input("ID do Paciente: "))
        except ValueError:
            print("IDs devem ser números inteiros.")
            continue
            
        date_input = input("Data (YYYY-MM-DD): ")
        time_input = input("Hora (HH:MM:SS): ")
        motivo_input = input("Motivo da Consulta: ")
        
        try:
            appointment_date = datetime.strptime(date_input, '%Y-%m-%d').date()
            appointment_time = datetime.strptime(time_input, '%H:%M:%S').time()
            
            if check_appointment_availability(doctor_id, appointment_date, appointment_time, cursor):
                schedule_appointment(doctor_id, patient_id, appointment_date, appointment_time, motivo_input, cursor, cnx)
            else:
                print("Consulta não pode ser agendada. Horário indisponível.")
        except ValueError:
            print("Formato de data ou hora inválido. Tente novamente.")


    elif choice == 3:
        # Cadastrar paciente - COM VALIDAÇÃO
        print("\n--- Cadastro de Paciente ---")
        name = input("Nome: ")
        try:
            age = int(input("Idade: "))
        except ValueError:
            print("Idade deve ser um número.")
            continue
        email = input("Email: ")
        
        # 1. Validação de Telefone
        phone = None
        while phone is None:
            phone_input = input("Telefone (11 dígitos, ex: 21987654321): ")
            phone = validate_input(phone_input, 11, "Telefone")
            if phone is None:
                continue

        # 2. Validação de Tipo Sanguíneo (Menu)
        blood_type = get_blood_type_from_menu()

        # 3. Validação de CPF
        cpf = None
        while cpf is None:
            cpf_input = input("CPF (11 dígitos): ")
            cpf = validate_input(cpf_input, 11, "CPF")
            if cpf is None:
                continue
        
        register_client(name, age, email, phone, blood_type, cpf, cursor, cnx)

    elif choice == 4:
        # Cadastrar médico - COM VALIDAÇÃO (adaptado)
        print("\n--- Cadastro de Médico ---")
        name = input("Nome: ")
        specialty = input("Especialidade: ")
        
        # Validação de Telefone para o médico
        phone = None
        while phone is None:
            phone_input = input("Telefone (11 dígitos, ex: 21987654321): ")
            phone = validate_input(phone_input, 11, "Telefone")
            if phone is None:
                continue
                
        register_doctor(name, specialty, phone, cursor, cnx)

    elif choice == 5:
        # Listar consultas
        list_full_appointments(cursor)
        
    elif choice == 6:
        # Listar médicos e pacientes para obter IDs
        list_doctors(cursor)
        list_patients(cursor)
        
    elif choice == 7:
        # Listar horários de atendimento
        list_doctor_availability(cursor)

    elif choice == 0:
        print("Saindo...")
        break

# Fechamento de recursos ao sair do loop principal
if 'cursor' in locals() and cursor:
    cursor.close()
if 'cnx' in locals() and cnx:
    cnx.close()
    print("Conexão com o banco de dados encerrada.")
