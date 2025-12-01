-- ============================
-- CRIAÇÃO DO BANCO DE DADOS
-- ============================
CREATE DATABASE IF NOT EXISTS clinica;
USE clinica;

-- ============================
-- TABELA: especialidades
-- ============================
CREATE TABLE especialidades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
);

-- ============================
-- TABELA: medicos
-- ============================
CREATE TABLE medicos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    crm VARCHAR(20) NOT NULL UNIQUE,
    especialidade_id INT NOT NULL,
    telefone VARCHAR(20),
    cidade VARCHAR(100),

    -- Em produção, senha deve ser armazenada como HASH
    -- Exemplo recomendável: SHA2('senha', 256) ou bcrypt
    senha_hash CHAR(64) NOT NULL,

    FOREIGN KEY (especialidade_id) REFERENCES especialidades(id)
);

-- Índice para melhorar buscas por especialidade
CREATE INDEX idx_medicos_especialidade ON medicos (especialidade_id);

-- ============================
-- TABELA: pacientes
-- ============================
CREATE TABLE pacientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    cpf CHAR(11) NOT NULL UNIQUE,
    telefone VARCHAR(20),
    data_nascimento DATE,

    -- Em produção: usar SHA2/bcrypt
    senha_hash CHAR(64) NOT NULL
);

-- ============================
-- TABELA: consultas
-- ============================
CREATE TABLE consultas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    paciente_id INT NOT NULL,
    medico_id INT NOT NULL,
    data_consulta DATE NOT NULL,
    hora_consulta TIME NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'agendado'
        CHECK (status IN ('agendado', 'cancelado', 'concluido')),

    FOREIGN KEY (paciente_id) REFERENCES pacientes(id),
    FOREIGN KEY (medico_id) REFERENCES medicos(id)
);

-- Índices úteis
CREATE INDEX idx_consultas_medico_data ON consultas (medico_id, data_consulta);
CREATE INDEX idx_consultas_paciente ON consultas (paciente_id);

-- ============================
-- VIEW: view_consultas_completas
-- Usando JOIN + filtros → diferente das queries simples
-- ============================
CREATE OR REPLACE VIEW view_consultas_completas AS
SELECT 
    c.id AS consulta_id,
    p.nome AS paciente_nome,
    m.nome AS medico_nome,
    e.nome AS especialidade,
    c.data_consulta,
    c.hora_consulta,
    c.status
FROM consultas c
JOIN pacientes p ON c.paciente_id = p.id
JOIN medicos m ON c.medico_id = m.id
JOIN especialidades e ON m.especialidade_id = e.id
WHERE c.status <> 'cancelado'
ORDER BY c.data_consulta DESC;

-- ============================
-- Comentário sobre segurança:
-- SENHAS NÃO DEVEM SER ARMAZENADAS EM TEXTO PURO
-- Armazenar sempre HASH da senha:
-- INSERT INTO pacientes (nome, cpf, senha_hash) VALUES ('Joao', '123...', SHA2('senha123', 256));
-- ============================

