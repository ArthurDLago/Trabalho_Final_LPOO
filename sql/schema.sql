-- Script de criação das tabelas do Pet Shop (PostgreSQL)
-- Banco: Trabalho_Final_LPOO

CREATE TABLE IF NOT EXISTS cliente (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    telefone VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS pet (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    especie VARCHAR(50) NOT NULL,
    cliente_id INTEGER NOT NULL REFERENCES cliente(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS agendamento (
    id SERIAL PRIMARY KEY,
    data DATE NOT NULL,
    hora VARCHAR(5) NOT NULL,
    pet_id INTEGER NOT NULL REFERENCES pet(id) ON DELETE CASCADE,
    CONSTRAINT uq_agendamento_pet_data_hora UNIQUE (data, hora)
);

CREATE INDEX IF NOT EXISTS idx_pet_cliente ON pet(cliente_id);
CREATE INDEX IF NOT EXISTS idx_agendamento_pet ON agendamento(pet_id);
