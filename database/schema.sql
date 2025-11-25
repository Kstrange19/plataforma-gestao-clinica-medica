-- =============================================
-- Projeto: Plataforma de Gestão para Clínica Médica
-- Descrição: Criação de banco de dados para gerenciar pacientes, consultas e disponibilidade.
-- Autores: Kauã Amado (Kstrange19) e Moisés Henrique (moises-h7)
-- Data: 02/12/2025
-- =============================================
CREATE DATABASE IF NOT EXISTS clinica_medica;
USE clinica_medica;

CREATE TABLE IF NOT EXISTS medicos (
        id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(255) NOT NULL,
        especialidade VARCHAR(50) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL
        telefone VARCHAR(11) UNIQUE NOT NULL,
    );

CREATE TABLE IF NOT EXISTS clientes (
        id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(255) NOT NULL,
        idade INT NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        telefone VARCHAR(11)
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

CREATE TABLE disponibilidade_medicos (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    medico_id INT UNSIGNED,
    dia_semana VARCHAR(20), 
    horario_inicio TIME,
    horario_fim TIME,
    FOREIGN KEY (medico_id) REFERENCES medicos(id)
);

INSERT INTO medicos (nome, especialidade, email, telefone) VALUES
('Paulo Roberto', 'Pneumologia', 'prmnasc@clinica.com','21965386364',),
('Ewerton Madruga', 'Dermatologia', 'elmadruga@clinica.com', '21994485533'),
('Wladimir Chapetta', 'Endocrinologia', 'wcchapetta@clinica.com', '21999999999'),
('Roberto Amaral', 'Cardiologia',  'rlamaral@clinica.com', '21992668215'),
('Mariana Carla', 'Ginecologia', 'marianacarla@clinica.com', '21979681241'),
('Antônio Lacerda', 'Psiquiatria', 'aljunior@clinica.com', '24981543287');

INSERT INTO clientes (nome, idade, email, telefone) VALUES
('Kauã Amado', 17, 'kauaamado5@gmail.com', '21974392787'),
('Moises Campos', 18, 'moiseshoc27@gmail.com', '21972701348'),
('Estevão Martins', 17, 'estevaomartins@gmail.com', '21972963756'),
('Matheus Marques', 18, 'marquesaraujomatheus7@gmail.com', '21979513613'),
('Raphael Furtado', 16, 'raphaelfurtado120@gmail.com', '21980979950'),
('Dominique Gomes', 17, 'niquegbarbosa@gmail.com', '21970763935');

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
(2, 'Terça', '07:30:00', '11:00:00'),
(2, 'Terça', '13:00:00', '18:00:00'),
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