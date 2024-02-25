from flask import Flask, request, jsonify, send_from_directory
import pymysql
import yaml
import os
import time

# Delay the application startup by 10 seconds to let MySQL start up
time.sleep(10)

# Load database configuration from db.yaml
db_config = yaml.load(open('backend/db.yaml'), Loader=yaml.FullLoader)

# Define the paths to the 'frontend' folder relative to this
static_folder_path = os.path.join(os.getcwd(), 'frontend')
print("Static folder path:", static_folder_path)

app = Flask(__name__, static_folder=static_folder_path, static_url_path='')

# Database connection function
def get_db_connection():
    return pymysql.connect(host=db_config['mysql_host'],
                           user=db_config['mysql_user'],
                           password=db_config['mysql_password'],
                           db=db_config['mysql_db'],
                           cursorclass=pymysql.cursors.DictCursor)

# Function to ensure the database is connected
def connect_to_database(max_attempts=25):
    attempt_num = 0
    while attempt_num < max_attempts:
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
            conn.close()
            print(f"Successfully connected to the database on attempt {attempt_num}.")
            return
        except Exception as e:
            attempt_num += 1
            print(f"Attempt {attempt_num} failed with error: {e}")
            time.sleep(5)  # Wait for 5 seconds before retrying

connect_to_database()

@app.route('/')
def home():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/todos', methods=['GET'])
def get_todos():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM todos")
        rv = cursor.fetchall()
    conn.close()
    return jsonify(rv)

@app.route('/todo', methods=['POST'])
def add_todo():
    details = request.json
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO todos(task) VALUES (%s)", (details['task'],))
        conn.commit()
    conn.close()
    return jsonify({'message': 'Todo added successfully!'})

@app.route('/todo/<id>', methods=['PUT'])
def update_todo(id):
    details = request.json
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("UPDATE todos SET completed = %s WHERE id = %s", (details['completed'], id))
        conn.commit()
    conn.close()
    return jsonify({'message': 'Todo updated successfully!'})

@app.route('/todo/<id>', methods=['DELETE'])
def delete_todo(id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM todos WHERE id = %s", (id,))
        conn.commit()
    conn.close()
    return jsonify({'message': 'Todo deleted successfully!'})

if __name__ == '__main__':
    app.run(debug=True)
