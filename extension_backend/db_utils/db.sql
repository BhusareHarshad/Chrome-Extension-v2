-- Create a new database
CREATE DATABASE SUMMARIZER;

CREATE TABLE request_response (
    id SERIAL PRIMARY KEY,
    request TEXT,
    response TEXT,
	feedback VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);