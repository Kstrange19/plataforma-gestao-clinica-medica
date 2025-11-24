-- =============================================
-- Projeto: Plataforma de Gestão para Clínica Médica
-- Descrição: Criação de banco de dados para gerenciar pacientes, consultas e disponibilidade.
-- Autores: Kauã Amado (Kstrange19) e Moisés Henrique (moises.h7)
-- Data: 02/12/2025
-- =============================================
CREATE DATABASE IF NOT EXISTS clinica_medica;
USE clinica_medica;

CREATE TABLE IF NOT EXISTS medicos (
        id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(255) NOT NULL,
        especialidade VARCHAR(50),
        telefone VARCHAR(11),
        email VARCHAR(255)
    );

CREATE TABLE IF NOT EXISTS clientes (
        id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(255) NOT NULL,
        idade INT NOT NULL,
        email VARCHAR(100),
        telefone VARCHAR(11)
    );

CREATE TABLE IF NOT EXISTS consultas (
        id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        cliente_id INT UNSIGNED,
        medico_id INT UNSIGNED,
        data_consulta DATETIME,
        horario TIME,
        motivo VARCHAR(255),
        status VARCHAR(50),
        FOREIGN KEY (cliente_id) REFERENCES clientes(id),
        FOREIGN KEY (medico_id) REFERENCES medicos(id)
    );

CREATE TABLE IF NOT EXISTS disponibilidade_medicos (
        id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        medico_id INT UNSIGNED,
        dia_semana VARCHAR(20),
        horario_inicio TIME,
        horario_fim TIME,
        FOREIGN KEY (medico_id) REFERENCES medicos(id)
    );