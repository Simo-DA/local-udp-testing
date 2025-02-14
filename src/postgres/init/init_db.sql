-- init-dagster.sql
CREATE DATABASE dagster;
CREATE DATABASE mydatabase;
-- Connect to the database
\c mydatabase;

-- Create the table only if it does not exist
CREATE TABLE IF NOT EXISTS iot_messages (
    id SERIAL PRIMARY KEY,
    message TEXT NOT NULL,
    received_at TIMESTAMP DEFAULT NOW()
);