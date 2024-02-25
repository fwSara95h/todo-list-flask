from flask import Flask, request, jsonify, send_from_directory
from flask_mysqldb import MySQL
import yaml
import os
import time

# Delay the application startup by 10 seconds to let mysql start up
time.sleep(10)


# Define the paths to the 'frontend' folder relative to this
# parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
# static_folder_path = os.path.join(parent_dir, 'frontend')
static_folder_path = os.path.join(os.getcwd(), 'frontend')
print("Static folder path:", static_folder_path)

app = Flask(__name__, static_folder=static_folder_path, static_url_path='')

# Load database configuration from db.yaml
db_config = yaml.load(open('backend/db.yaml'), Loader=yaml.FullLoader)
app.config['MYSQL_HOST'] = db_config['mysql_host']
app.config['MYSQL_PORT'] = db_config['mysql_port'] 
app.config['MYSQL_USER'] = db_config['mysql_user']
app.config['MYSQL_PASSWORD'] = db_config['mysql_password']
app.config['MYSQL_DB'] = db_config['mysql_db']

mysql = MySQL(app)

# Multiple attempts to connect
def connect_to_database(max_attempts=25):
    attempt_num = 0
    while attempt_num < max_attempts:
        attempt_num += 1
        try:
            # Try to get a cursor to test the connection
            with app.app_context():
                mysql.connection.cursor()
            print(f"Successfully connected to the database on attempt {attempt_num}.")
            return
        except Exception as e:
            print(f"Attempt {attempt_num} failed with error: {e}")
            time.sleep(5)  # Wait for 5 seconds before retrying


connect_to_database()
#################


@app.route('/')
def home():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/todos', methods=['GET'])
def get_todos(): 
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM todos")
    # rv = cur.fetchall()
    fields = [field_md[0] for field_md in cur.description]
    rv = [dict(zip(fields, row)) for row in cur.fetchall()]
    return jsonify(rv)


@app.route('/todo', methods=['POST'])
def add_todo():
    details = request.json
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO todos(task) VALUES (%s)", [details['task']])
    mysql.connection.commit()
    return jsonify({'message': 'Todo added successfully!'})


@app.route('/todo/<id>', methods=['PUT'])
def update_todo(id):
    details = request.json
    print(type(details), details)
    cur = mysql.connection.cursor()
    cur.execute("UPDATE todos SET completed = %s WHERE id = %s", (details['completed'], id))
    mysql.connection.commit()
    return jsonify({'message': 'Todo updated successfully!'})


@app.route('/todo/<id>', methods=['DELETE'])
def delete_todo(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM todos WHERE id = %s", [id])
    mysql.connection.commit()
    return jsonify({'message': 'Todo deleted successfully!'})


if __name__ == '__main__':
    app.run(debug=True)
