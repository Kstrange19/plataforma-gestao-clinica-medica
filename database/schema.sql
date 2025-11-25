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
        telefone VARCHAR(11) UNIQUE NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL
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

CREATE TABLE IF NOT EXISTS disponibilidade_medicos (
    medico_id INT UNSIGNED, 
    dia_semana ENUM('Domingo', 'Segunda', 'Terca', 'Quarta', 'Quinta', 'Sexta', 'Sabado') NOT NULL,
    horario_inicio TIME NOT NULL,
    horario_fim TIME NOT NULL,
    FOREIGN KEY (medico_id) REFERENCES medicos(id),
    UNIQUE KEY unique_disponibilidade (medico_id, dia_semana, horario_inicio)
);