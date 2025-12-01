# Plataforma de gestão de clínica médica

## Descrição

Projeto de desenvolvimento de uma plataforma de gestão de clínica médica com interface em Python para gerenciar cadastros ou consultar disponibilidade de horários.

## Autores

- Kauã Amado
- Moisés Campos

## Tecnologias Utilizadas

- Docker 29.0.4
- MySQL Workbench 8.0
- Python 3.12.3

## Modelo de Dados

- Modelo relacional (MySQL 8.0)

### Entidades Principais

- **medicos**: Cadastro dos profissionais, incluindo especialidade e contato.
- **clientes**: Dados pessoais dos pacientes, incluindo tipo sanguíneo (Fator RH).
- **consultas**: Tabela central que registra os agendamentos, vinculando médico e paciente.
- **horarios_atendimento**: Grade de horários disponíveis de cada médico (Dias da semana e turnos).
- **catalogo_condicoes**: Tabela de domínio (lookup) contendo tipos padronizados de doenças, alergias e hábitos.
- **ficha_paciente**: Prontuário médico que registra o histórico de saúde (Relacionamento N:M entre Clientes e Condições).

### Relacionamentos

- **[medicos] 1 → N [consultas]**: Um médico pode realizar diversas consultas, mas uma consulta pertence a apenas um médico.
- **[clientes] 1 → N [consultas]**: Um paciente pode agendar várias consultas ao longo do tempo.
- **[medicos] 1 → N [horarios_atendimento]**: Um médico possui vários horários de disponibilidade cadastrados na semana.
- **[clientes] N ↔ M [catalogo_condicoes]**: Relacionamento Muitos-para-Muitos implementado através da tabela associativa **`ficha_paciente`**.
  - *Explicação:* Um paciente pode ter várias condições de saúde (ex: ser fumante e ter alergia), e uma condição (ex: Diabetes) pode afetar vários pacientes.

## Decisões de Design

1. **Normalização e Tabela Associativa (Ficha Médica)**:
   - Para evitar redundância e inconsistência nos dados de saúde (como grafias diferentes para a mesma doença), optamos por criar uma tabela separada `catalogo_condicoes`.
   - A tabela `ficha_paciente` atua como uma entidade associativa, permitindo criar um prontuário rico onde um paciente pode ter múltiplas comorbidades registradas de forma organizada.

2. **Uso de ENUM para Integridade de Dados**:
   - Utilizamos o tipo de dado `ENUM` para campos com valores fixos e previsíveis, como `tipo_sanguineo` (A+, B-, etc.) e `tipo` da condição (Alergia, Cirurgia, etc.).
   - Isso impede a inserção de dados inválidos no sistema e otimiza o armazenamento.

3. **Infraestrutura com Docker**:
   - O projeto foi containerizado para garantir que o ambiente de desenvolvimento seja reproduzível. Utilizamos um volume persistente (`mysql_data`) e um script de inicialização (`schema.sql`) para automatizar a criação da estrutura do banco.

4. **Tratamento de Datas e Horários**:
   - Separamos `data` e `horario` em colunas distintas na tabela de consultas para facilitar filtros por dia ou por faixa de horário, simplificando a lógica de verificação de disponibilidade no backend.

## 🚀 Como Executar

### 1. Preparar o Ambiente Python

Recomendamos o uso de um ambiente virtual para isolar as dependências do projeto.

```bash
# 1. Crie o ambiente virtual (chamado .venv)
python3 -m venv .venv

# 2. Ative o ambiente
# No Linux/Mac:
source .venv/bin/activate
# No Windows (PowerShell):
.venv\Scripts\Activate

# 3. Instale a biblioteca de conexão com o MySQL
pip install mysql-connector-python
```

### 2. Subir o Banco de Dados

```bash
sudo docker compose up -d # Aguarde alguns segundos na primeira execução para que o container carregue tudo.
```

### Executar o sistema

```bash
python main.py
```

### ⚠️ Observação sobre a Persistência de Dados (mysql_data)

O projeto utiliza um volume Docker (`./mysql_data`) para garantir que os dados não sejam perdidos quando o container é desligado.

- **Para resetar o banco de dados:** Se você alterar o arquivo `schema.sql` e precisar recriar o banco do zero, execute os seguintes comandos:

  ```bash
  docker compose down
  # No Linux/Mac:
  sudo rm -rf mysql_data
  # No Windows (PowerShell):
  # Remove-Item -Recurse -Force mysql_data
  docker compose up -d
