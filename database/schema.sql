# =============================================
# Projeto: Plataforma de Gestão para Clínica Médica
# Descrição: Banco de dados para gerenciar pacientes, consultas, médicos e condições
# Autores: Kauã Amado e Moisés Henrique
# Data: 02/12/2025
# =============================================

-- Comando de segurança para limpar o banco de dados antes de recriar
DROP DATABASE IF EXISTS clinica_medica;

-- Criacao, Conectividade, acessibilidade do banco de dados 
CREATE DATABASE IF NOT EXISTS clinica_medica CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE clinica_medica;
SET NAMES utf8mb4; 

-- Tabela: Medicos
CREATE TABLE IF NOT EXISTS medicos (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    especialidade VARCHAR(50) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    telefone VARCHAR(11) UNIQUE NOT NULL,
    senha_hash VARCHAR(255)
);
-- Segurança: 'senha_hash' nao deve salvar texto puro. Em producao, usar Bcrypt ou Argon2 (hashing lento) na aplicacao.

-- Indice: Medicos
CREATE INDEX idx_medicos_nome ON medicos(nome);

-- Tabela: Pacientes
CREATE TABLE IF NOT EXISTS pacientes (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    idade INT NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefone VARCHAR(11),
    tipo_sanguineo ENUM('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-') NOT NULL,
    cpf VARCHAR(11) UNIQUE,
    senha_hash VARCHAR(255)
);
-- Segurança: 'senha_hash' nao salva em texto puro. Em producao, usar Bcrypt ou Argon2 (hashing lento) na aplicacao.

-- Indice: pacientes
CREATE INDEX idx_pacientes_nome ON pacientes(nome);

-- Tabela: Consultas
CREATE TABLE IF NOT EXISTS consultas (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    paciente_id INT UNSIGNED,
    medico_id INT UNSIGNED,
    data_consulta DATE,
    hora_consulta TIME,
    motivo VARCHAR(255),
    status VARCHAR(50),
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id),
    FOREIGN KEY (medico_id) REFERENCES medicos(id)
);

-- Criacao dos indices dos pacientes
CREATE INDEX idx_consultas_paciente ON consultas(paciente_id);
CREATE INDEX idx_consultas_medico ON consultas(medico_id);
CREATE INDEX idx_consultas_data_hora ON consultas(data_consulta, hora_consulta);

-- Tabela: horarios de atendimento
CREATE TABLE IF NOT EXISTS horarios_atendimento (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    medico_id INT UNSIGNED,
    dia_semana VARCHAR(20),
    horario_inicio TIME,
    horario_fim TIME,
    FOREIGN KEY (medico_id) REFERENCES medicos(id)
);

-- Indice: disponibilidade dos medicos
CREATE INDEX idx_horarios_medico_dia ON horarios_atendimento(medico_id, dia_semana);

-- Tabela: catalogo de condicoes
CREATE TABLE IF NOT EXISTS catalogo_condicoes (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE,
    tipo ENUM('Fumante', 'Alergia', 'Doença Crônica', 'Cirurgia', 'Medicamento regular', 'Outros') NOT NULL
);

-- Tabela: Ficha_Paciente (N:M)
CREATE TABLE IF NOT EXISTS ficha_paciente (
    paciente_id INT UNSIGNED,
    condicao_id INT UNSIGNED,
    data_registro DATE DEFAULT (CURRENT_DATE),
    observacoes VARCHAR(255), # Observações
    PRIMARY KEY (paciente_id, condicao_id),
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id),
    FOREIGN KEY (condicao_id) REFERENCES catalogo_condicoes(id)
);

-- Paciente cadastrado
CREATE INDEX idx_ficha_paciente ON ficha_paciente(paciente_id);

-- Inserções de Exemplo
-- Seguranca: 'dummyhash' e um valor de teste. Em producao, aqui seria inserido o hash gerado pela aplicacao (Ex: Bcrypt,SHA-256).
INSERT INTO medicos (nome, especialidade, email, telefone, senha_hash) VALUES
('Paulo Roberto', 'Pneumologia', 'prmnasc@clinica.com','21965386364', 'dummyhash'),
('Ewerton Madruga', 'Dermatologia', 'elmadruga@clinica.com', '21994485533', 'dummyhash'),
('Wladimir Chapetta', 'Endocrinologia', 'wcchapetta@clinica.com', '21999999999', 'dummyhash'),
('Roberto Amaral', 'Cardiologia',  'rlamaral@clinica.com', '21992668215', 'dummyhash'),
('Mariana Carla', 'Ginecologia', 'marianacarla@clinica.com', '21979681241', 'dummyhash'),
('Antônio Lacerda', 'Psiquiatria', 'aljunior@clinica.com', '24981543287', 'dummyhash');

-- Seguranca: 'dummyhash': valor de teste. Em producao, aqui seria inserido o hash gerado pela aplicacao (Ex: Bcrypt,SHA-256).
INSERT INTO pacientes (nome, idade, email, telefone, tipo_sanguineo, cpf, senha_hash) VALUES
('Kauã Amado', 17, 'kauaamado5@gmail.com', '21974392787', 'A+', '00000000000', 'dummyhash'),
('Moises Campos', 18, 'moiseshoc27@gmail.com', '21972701348', 'O-', '00000000001', 'dummyhash'),
('Estevão Martins', 17, 'estevaomartins@gmail.com', '21972963756', 'B+', '00000000002', 'dummyhash'),
('Matheus Maques', 18, 'marquesaraujomatheus7@gmail.com', '2199513613', 'AB+', '00000000003', 'dummyhash'),
('Raphael Furtado', 16, 'raphaelfurtado120@gmail.com', '219979950', 'O+', '00000000004', 'dummyhash'),
('Dominique Gomes', 17, 'niquegbarbosa@gmail.com', '21970763935', 'A-', '00000000005', 'dummyhash');

INSERT INTO consultas (paciente_id, medico_id, data_consulta, hora_consulta, motivo, status) VALUES
(1, 1, '2025-12-02', '10:00:00', 'Tosse com sangue', 'Agendada'),
(1, 2, '2025-12-11', '14:30:00', 'Mancha na pele', 'Agendada'),
(3, 3, '2025-12-12', '09:00:00', 'Check-up anual', 'Agendada'),
(2, 6, '2025-12-15', '11:00:00', 'Ansiedade e insônia', 'Agendada'),
(4, 4, '2025-12-18', '13:30:00', 'Dor no peito', 'Agendada'),
(6, 5, '2025-12-20', '15:00:00', 'Check-up trimestral', 'Agendada');

INSERT INTO horarios_atendimento (medico_id, dia_semana, horario_inicio, horario_fim) VALUES
(1, 'Segunda', '07:30:00', '11:00:00'),
(1, 'Segunda', '13:00:00', '16:30:00'),
(2, 'Terca', '07:30:00', '11:00:00'),
(2, 'Terca', '13:00:00', '18:00:00'),
(3, 'Quarta', '07:30:00', '11:00:00'),
(3, 'Quarta', '13:00:00', '16:00:00'),
(4, 'Quinta', '07:30:00', '11:00:00'),
(4, 'Quinta', '13:00:00', '16:30:00'),
(5, 'Sexta', '08:00:00', '11:00:00'),
(5, 'Sexta', '13:30:00', '16:20:00'),
(6, 'Segunda', '08:00:00', '12:00:00'),
(6, 'Segunda', '13:00:00', '17:00:00'),
(6, 'Quarta', '08:00:00', '12:00:00'),
(6, 'Quarta', '13:00:00', '17:00:00'),
(6, 'Quinta', '08:00:00', '12:00:00'),
(6, 'Quinta', '13:00:00', '17:00:00');

INSERT INTO catalogo_condicoes (nome, tipo) VALUES  
('Penicilina', 'Alergia'),
('Dipirona', 'Alergia'),
('Hipertensão', 'Doença Crônica'),
('Diabetes Tipo 2', 'Doença Crônica'),
('Tabagismo', 'Fumante'),
('Sedentarismo', 'Outros'),
('Consumo de Álcool', 'Outros'),
('Frutos do Mar', 'Alergia'),
('Intolerância a Lactose', 'Alergia'),
('Insulina', 'Medicamento regular'),
('Apendicectomia', 'Cirurgia');

INSERT INTO ficha_paciente (paciente_id, condicao_id, observacoes) VALUES  
(1, 2, 'Teve reação na infância'),
(1, 3, 'Controlada com remédios'),
(2, 4, 'Recém-diagnosticado, uso de metformina'), 
(3, 5, 'Fumante de longa data, buscando cessação'),
(4, 8, 'Alergia severa, evita consumo'),
(6, 11, 'Cirurgia realizada há 5 anos, sem complicações');

-- Views do sistema
-- View: consultas marcadas
CREATE OR REPLACE VIEW view_consultas_completas AS
SELECT  
    c.id AS consulta_id,
    p.nome AS paciente,
    m.nome AS medico,
    m.especialidade,
    c.data_consulta,
    c.hora_consulta,
    c.motivo,
    c.status
FROM consultas c
JOIN pacientes p ON c.paciente_id = p.id
JOIN medicos m ON c.medico_id = m.id;

-- View: consultas futuras
CREATE OR REPLACE VIEW vw_consultas_futuras AS
SELECT *
FROM view_consultas_completas
WHERE data_consulta >= CURRENT_DATE();

-- View: resumo de pacientes com certas condicoes
CREATE OR REPLACE VIEW vw_pacientes_com_condicoes AS
SELECT  
    p.id AS paciente_id,
    p.nome,
    p.idade,
    p.email,
    p.telefone,
    p.tipo_sanguineo,
    cc.nome AS condicao,
    cc.tipo AS tipo_condicao,
    fp.observacoes,
    fp.data_registro
FROM pacientes p
LEFT JOIN ficha_paciente fp ON p.id = fp.paciente_id
LEFT JOIN catalogo_condicoes cc ON fp.condicao_id = cc.id;

-- View: resumo da agenda dos medicos
CREATE OR REPLACE VIEW vw_agenda_medicos AS
SELECT
    m.id AS medico_id,
    m.nome AS medico,
    m.especialidade,
    ha.dia_semana,
    ha.horario_inicio,
    ha.horario_fim,
    c.data_consulta,
    c.hora_consulta AS horario_consulta,
    c.paciente_id
FROM medicos m
LEFT JOIN horarios_atendimento ha ON ha.medico_id = m.id
LEFT JOIN consultas c 
    ON c.medico_id = m.id 
    AND c.hora_consulta BETWEEN ha.horario_inicio AND ha.horario_fim;

-- View: resumo geral dos pacientes
CREATE OR REPLACE VIEW vw_pacientes_resumo AS
SELECT  
    p.id,
    p.nome,
    p.idade,
    p.email,
    p.telefone,
    p.tipo_sanguineo,
    COUNT(fp.condicao_id) AS total_condicoes
FROM pacientes p
LEFT JOIN ficha_paciente fp ON p.id = fp.paciente_id
GROUP BY p.id;
