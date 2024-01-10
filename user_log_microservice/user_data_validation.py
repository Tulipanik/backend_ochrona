from flask import Flask, request, jsonify
import requests
import sqlite3

app = Flask(__name__)

password_manager_url = "http://127.0.0.1:8002/verify-password"
password_manager_url_count = "http://127.0.0.1:8002/ask-for-password-count"

def get_db_connection():
	conn = sqlite3.connect('user_database.db')
	conn.row_factory = sqlite3.Row
	return conn

def verify_password(data):
	response = requests.post(password_manager_url, json=data)
	return response.json().get("message")

def ask_for_password_count (data):
	response = requests.post(password_manager_url_count, json=data)
	print(response)
	return response.json()

@app.route("/verify-user", methods=['POST'])
def verify_user():
	data = request.get_json()
	username = data['username']
	conn = get_db_connection()
	user_from_db = conn.execute('SELECT user_id FROM users WHERE username = ?', (username,)).fetchall()
	conn.close()
	if (len(user_from_db) != 0):
		print(dict(user_from_db[0]))
		return jsonify({'message': 'User verified'})
	return jsonify({'message': 'User not verified'})

@app.route("/ask-for-combination", methods=["POST"])
def ask_foo_combination ():
	data = request.get_json()
	user_id = data['user_id']
	conn = get_db_connection()
	user_from_db = conn.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,)).fetchall()
	conn.close()
	print(user_from_db)
	if (len(user_from_db) != 0):
		response = ask_for_password_count(data)
		return jsonify(response)
	return jsonify({'message': "You shouldn't be here"})


@app.route("/verify-password", methods=['POST'])
def password_verify():
	data = request.get_json()
	user_id = data["user_id"]
	conn = get_db_connection()
	user_from_db = conn.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchall()
	print(user_from_db)
	if (len(user_from_db) != 0):
		response = verify_password(data)
		print(response)
		return jsonify(response)
	return jsonify({'message': "You shouldn't be here"})

if __name__ == "__main__":
    app.run(port=8001)

