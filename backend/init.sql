-- Create the database (if it does not already exist)
CREATE DATABASE IF NOT EXISTS todo_db;

-- Select the database to use
USE todo_db;

-- Create the 'todos' table to store todo items
CREATE TABLE IF NOT EXISTS todos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    task VARCHAR(255) NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert some sample data (Optional)
INSERT INTO todos (task, completed) VALUES ('Sample todo item #1', FALSE);
INSERT INTO todos (task, completed) VALUES ('Sample todo item #2', TRUE);
