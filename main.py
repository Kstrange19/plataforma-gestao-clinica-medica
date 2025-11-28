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

def register_client(name, age, email, phone, blood_type):
    try:
        sql = "INSERT INTO clientes (nome, idade, email, telefone, tipo_sanguineo) VALUES (%s, %s, %s, %s, %s)"
        values = (name, age if age != '' else None, email, phone, blood_type)
        cursor.execute(sql, values)
        cnx.commit()
        
        # Pega o ID do cliente recém-criado para vincular a ficha
        client_id = cursor.lastrowid
        print("Cliente registrado com sucesso.")
        
        # Chama a triagem automaticamente
        print("\n--- Iniciando Preenchimento da Ficha Médica ---")
        fill_medical_record(client_id)
        
    except Error as e:
        print(f"Erro ao registrar cliente: {e}")

# Nova Funcionalidade: Preenchimento da Ficha (Triagem)
def fill_medical_record(client_id):
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
        add_to_medical_record(client_id, 'Alergia Genérica', 'Alergia', f"Alergia a: {allergy}")

    print("Ficha médica atualizada com sucesso!")

# Função auxiliar para gravar no banco (Relacionamento N:M)
def add_to_medical_record(client_id, condition_name, condition_type, note):
    try:
        cursor.execute("SELECT id FROM catalogo_condicoes WHERE nome = %s", (condition_name,))
        result = cursor.fetchone()
        
        if result:
            condition_id = result[0]
            
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

def agendar_consulta(medico_id, cliente_id, data_consulta, hora_consulta):
    try:
        sql = "INSERT INTO consultas (medico_id, cliente_id, data_consulta, horario, status) VALUES (%s, %s, %s, %s, %s)"
        values = (medico_id, cliente_id, data_consulta, hora_consulta, 'Agendada')
        cursor.execute(sql, values)
        cnx.commit()
        print("Consulta agendada com sucesso.")
    except Error as e:
        print(f"Erro ao agendar consulta: {e}")

def verificar_disponibilidade_para_agendamento(medico_id, data_consulta, hora_consulta):
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
    english_day = data_consulta.strftime('%A')
    weekday = days_translation.get(english_day) # Busca em Português

    # Verifica se existe horário cadastrado
    time_query = """
        SELECT id FROM horarios_atendimento 
        WHERE medico_id = %s 
        AND dia_semana = %s
        AND horario_inicio <= %s 
        AND horario_fim > %s
    """
    cursor.execute(time_query, (medico_id, weekday, hora_consulta, hora_consulta))
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
    cursor.execute(conflict_query, (medico_id, data_consulta, hora_consulta))
    if cursor.fetchone():
        return False # Já tem alguém marcado

    return True # Livre!

# --- EXECUÇÃO PRINCIPAL ---

cnx = connect_db()
if cnx is None:
    sys.exit(1)

cursor = cnx.cursor()

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
            medico_id = int(input("ID do Médico: "))
        except ValueError:
            print("ID inválido. Tente novamente.")
            continue
        data_input = input("Data da Consulta (YYYY-MM-DD): ")
        hora_input = input("Hora da Consulta (HH:MM:SS): ")
        
        try:
            data_consulta = datetime.strptime(data_input, '%Y-%m-%d').date()
            hora_consulta = datetime.strptime(hora_input, '%H:%M:%S').time()
            
            disponivel = verificar_disponibilidade_para_agendamento(medico_id, data_consulta, hora_consulta)
            if disponivel:
                print("O horário está disponível para agendamento.")
            else:
                print("O horário não está disponível para agendamento.")
        except ValueError:
            print("Formato de data ou hora inválido.")
        except Error as e:
            print(f"Erro ao verificar disponibilidade: {e}")

    elif choice == 2:
        try:
            medico_id = int(input("ID do Médico: "))
            cliente_id = int(input("ID do Cliente: "))
        except ValueError:
            print("ID inválido. Tente novamente.")
            continue
        data_input = input("Data da Consulta (YYYY-MM-DD): ")
        hora_input = input("Hora da Consulta (HH:MM:SS): ")
        
        try:
            data_consulta = datetime.strptime(data_input, '%Y-%m-%d').date()
            hora_consulta = datetime.strptime(hora_input, '%H:%M:%S').time()
            
            disponivel = verificar_disponibilidade_para_agendamento(medico_id, data_consulta, hora_consulta)
            if disponivel:
                agendar_consulta(medico_id, cliente_id, data_consulta, hora_consulta)
            else:
                print("O horário não está disponível para agendamento.")
        except ValueError:
             print("Formato de data ou hora inválido.")

    elif choice == 3:
        name = input("Nome: ")
        age = input("Idade: ")
        email = input("Email: ")
        phone = input("Telefone: ")
        blood_type = input("Tipo Sanguíneo (A+, O-, etc): ").upper()
        register_client(name, age, email, phone, blood_type)

    elif choice == 4:
        name = input("Nome: ")
        specialty = input("Especialidade: ")
        phone = input("Telefone: ")
        email = input("Email: ")
        register_doctor(name, specialty, phone, email)

    elif choice == 0:
        print("Saindo do programa.")
        break