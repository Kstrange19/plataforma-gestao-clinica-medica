-- =============================================
-- Projeto: Plataforma de Gestão para Clínica Médica
-- Descrição: Criação de banco de dados para gerenciar pacientes, consultas e disponibilidade.
-- Autores: Kauã Amado (Kstrange19) e Moisés Henrique (moises-h7)
-- Data: 02/12/2025
-- =============================================
CREATE DATABASE IF NOT EXISTS clinica_medica CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE clinica_medica;
SET NAMES utf8mb4; -- Garante que os inserts do arquivo sejam lidos corretamente (ç, ã, etc).

CREATE TABLE IF NOT EXISTS medicos (
        id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(255) NOT NULL,
        especialidade VARCHAR(50) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        telefone VARCHAR(11) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS clientes (
        id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(255) NOT NULL,
        idade INT NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        telefone VARCHAR(11),
        tipo_sanguineo ENUM('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-') NOT NULL
);

CREATE TABLE IF NOT EXISTS consultas (
        id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        cliente_id INT UNSIGNED,
        medico_id INT UNSIGNED,
        data_consulta DATE,
        horario TIME,
        motivo VARCHAR(255),
        status VARCHAR(50),
        FOREIGN KEY (cliente_id) REFERENCES clientes(id),
        FOREIGN KEY (medico_id) REFERENCES medicos(id)
);

CREATE TABLE horarios_atendimento (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    medico_id INT UNSIGNED,
    dia_semana VARCHAR(20), 
    horario_inicio TIME,
    horario_fim TIME,
    FOREIGN KEY (medico_id) REFERENCES medicos(id)
);

-- Catálogo de Condições (Doenças, Alergias, Comorbidades)
CREATE TABLE IF NOT EXISTS catalogo_condicoes (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE,
    tipo ENUM('Fumante', 'Alergia', 'Doença Crônica', 'Cirurgia', 'Medicamento regular', 'Outros') NOT NULL
);

-- Liga o Paciente à Condição e permite adicionar uma observação
CREATE TABLE IF NOT EXISTS ficha_paciente (
    cliente_id INT UNSIGNED,
    condicao_id INT UNSIGNED,
    data_registro DATE DEFAULT (CURRENT_DATE),
    observacoes VARCHAR(255), -- Ex: 'Teve crise em 2020', 'Grau leve'
    -- A chave primária é a dupla (Cliente + Condição), permitindo várias doenças por paciente sem duplicatas
    PRIMARY KEY (cliente_id, condicao_id),
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (condicao_id) REFERENCES catalogo_condicoes(id)
);


INSERT INTO medicos (nome, especialidade, email, telefone) VALUES
('Paulo Roberto', 'Pneumologia', 'prmnasc@clinica.com','21965386364'),
('Ewerton Madruga', 'Dermatologia', 'elmadruga@clinica.com', '21994485533'),
('Wladimir Chapetta', 'Endocrinologia', 'wcchapetta@clinica.com', '21999999999'),
('Roberto Amaral', 'Cardiologia',  'rlamaral@clinica.com', '21992668215'),
('Mariana Carla', 'Ginecologia', 'marianacarla@clinica.com', '21979681241'),
('Antônio Lacerda', 'Psiquiatria', 'aljunior@clinica.com', '24981543287');

INSERT INTO clientes (nome, idade, email, telefone, tipo_sanguineo) VALUES
('Kauã Amado', 17, 'kauaamado5@gmail.com', '21974392787', 'A+'),
('Moises Campos', 18, 'moiseshoc27@gmail.com', '21972701348', 'O-'),
('Estevão Martins', 17, 'estevaomartins@gmail.com', '21972963756', 'B+'),
('Matheus Marques', 18, 'marquesaraujomatheus7@gmail.com', '21979513613', 'AB+'),
('Raphael Furtado', 16, 'raphaelfurtado120@gmail.com', '21980979950', 'O+'),
('Dominique Gomes', 17, 'niquegbarbosa@gmail.com', '21970763935', 'A-');

INSERT INTO consultas (cliente_id, medico_id, data_consulta, horario, motivo, status) VALUES
(1, 1, '2024-12-2', '10:00:00', 'Tosse com sangue', 'Agendada'),
(1, 2, '2024-12-11', '14:30:00', 'Mancha na pele', 'Agendada'),
(3, 3, '2024-12-12', '09:00:00', 'Check-up anual', 'Agendada'),
(2, 6, '2024-12-15', '11:00:00', 'Ansiedade e insônia', 'Agendada'),
(4, 4, '2024-12-18', '13:30:00', 'Dor no peito', 'Agendada'),
(6, 5, '2024-12-20', '15:00:00', 'Check-up trimestral', 'Agendada');

INSERT INTO horarios_atendimento (medico_id, dia_semana, horario_inicio, horario_fim) VALUES
(1, 'Segunda', '07:30:00', '11:00:00'),
(1, 'Segunda', '13:00:00', '16:30:00'),
(2, 'Terca', '07:30:00', '11:00:00'),
(2, 'Terca', '13:00:00', '18:00:00'),
(3, 'Quarta', '07:30:00', '11:00:00'),
(3, 'Quarta', '13:00:00', '16:00:00'),
(4, 'Quinta', '07:30:00', '11:00:00'),
(4, 'Quinta', '13:00:00', '16:30:00'),
(5, 'Sexta', '8:00:00', '11:00:00'),
(5, 'Sexta', '13:30:00', '16:20:00'),
(6, 'Segunda', '08:00:00', '12:00:00'),
(6, 'Segunda', '13:00:00', '17:00:00'),
(6, 'Quarta', '08:00:00', '12:00:00'),
(6, 'Quarta', '13:00:00', '17:00:00'),
(6, 'Quinta', '08:00:00', '12:00:00'),
(6, 'Quinta', '13:00:00', '17:00:00');

INSERT INTO catalogo_condicoes (nome, tipo) VALUES 
('Penicilina', 'Alergia'),      -- Para a pergunta "Tem alergia a algum medicamento?"
('Dipirona', 'Alergia'),
('Hipertensão', 'Doença Crônica'),      -- Para a pergunta "Possui alguma doença crônica?"
('Diabetes Tipo 2', 'Doença Crônica'),
('Tabagismo', 'Fumante'),       -- Para a pergunta "É fumante?"
('Sedentarismo', 'Outros'),     -- Para a pergunta "Exercícios regulares? ( ) Não"
('Consumo de Álcool', 'Outros'),        -- Para a pergunta "Consome bebida alcoólica?"
('Frutos do Mar', 'Alergia'), -- Exemplo para "Alimento que não possa consumir"
('Intolerância a Lactose', 'Alergia'),
('Insulina', 'Medicamento regular'),
('Apendicectomia', 'Cirurgia'); -- Exemplo para "Já passou por alguma cirurgia?"

INSERT INTO ficha_paciente (cliente_id, condicao_id, observacoes) VALUES 
(1, 2, 'Teve reação na infância'),
(1, 3, 'Controlada com remédios');

-- VIEWS DO SISTEMA
-- View: consultas com nome do cliente e do médico
CREATE OR REPLACE VIEW vw_consultas_completas AS
SELECT 
    c.id AS consulta_id,
    cli.nome AS cliente,
    m.nome AS medico,
    m.especialidade,
    c.data_consulta,
    c.horario,
    c.motivo,
    c.status
FROM consultas c
JOIN clientes cli ON c.cliente_id = cli.id
JOIN medicos m ON c.medico_id = m.id;

-- View: consultas futuras
CREATE OR REPLACE VIEW vw_consultas_futuras AS
SELECT *
FROM vw_consultas_completas
WHERE data_consulta >= CURRENT_DATE;

-- View: pacientes com condições cadastradas
CREATE OR REPLACE VIEW vw_pacientes_com_condicoes AS
SELECT 
    cli.id AS cliente_id,
    cli.nome,
    cli.idade,
    cli.email,
    cli.telefone,
    cli.tipo_sanguineo,
    cc.nome AS condicao,
    cc.tipo AS tipo_condicao,
    fp.observacoes,
    fp.data_registro
FROM clientes cli
LEFT JOIN ficha_paciente fp ON cli.id = fp.cliente_id
LEFT JOIN catalogo_condicoes cc ON fp.condicao_id = cc.id;

-- View: agenda completa dos médicos
CREATE OR REPLACE VIEW vw_agenda_medicos AS
SELECT
    m.id AS medico_id,
    m.nome AS medico,
    m.especialidade,
    ha.dia_semana,
    ha.horario_inicio,
    ha.horario_fim,
    c.data_consulta,
    c.horario AS horario_consulta,
    c.cliente_id
FROM medicos m
LEFT JOIN horarios_atendimento ha ON ha.medico_id = m.id
LEFT JOIN consultas c 
    ON c.medico_id = m.id 
    AND c.horario BETWEEN ha.horario_inicio AND ha.horario_fim;

-- View: ficha resumida de pacientes
CREATE OR REPLACE VIEW vw_pacientes_resumo AS
SELECT 
    cli.id,
    cli.nome,
    cli.idade,
    cli.email,
    cli.telefone,
    cli.tipo_sanguineo,
    COUNT(fp.condicao_id) AS total_condicoes
FROM clientes cli
LEFT JOIN ficha_paciente fp ON cli.id = fp.cliente_id
GROUP BY cli.id;
