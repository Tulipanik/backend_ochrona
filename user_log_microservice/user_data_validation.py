from flask import Flask, request, jsonify
import requests
import sqlite3
from jsonschema import validate, ValidationError

app = Flask(__name__)

password_manager_url = "http://127.0.0.1:8002/verify-password"
password_manager_url_count = "http://127.0.0.1:8002/ask-for-password-count"


def get_db_connection():
	conn = sqlite3.connect('user_database.db')
	conn.row_factory = sqlite3.Row
	return conn

def verify_password(data):
	response = requests.post(password_manager_url, json=data)
	return response.json()

def ask_for_password_count (data):
	response = requests.post(password_manager_url_count, json=data)
	print(response)
	return response.json()

@app.route("/verify-user", methods=['POST'])
def verify_user():
	data = request.get_json()
	schema = {
	"$schema": "http://json-schema.org/draft-07/schema#",
	"type": "object",
	"properties": {
		"login": {
		"type": "string",
		"pattern": "^[a-zA-Z0-9]+$"
		}
	},
	"required": ["login"],
	"additionalProperties": False
	}

	try:
		validate(data, schema)
	except ValidationError as e:
		return jsonify({'message': 'Incorrect payload'})
	
	username = data["login"]
	conn = get_db_connection()
	user_from_db = conn.execute('SELECT user_id FROM users WHERE username = ?', (username,)).fetchall()
	conn.close()
	if (len(user_from_db) != 0):
		user_from_db = dict(user_from_db[0])["user_id"]
		return jsonify({'user_id': user_from_db})
	return jsonify({'message': 'User not verified'})

@app.route("/ask-for-combination", methods=["POST"])
def ask_foo_combination ():
	data = request.get_json()
	schema = {
		"$schema": "http://json-schema.org/draft-07/schema#",
		"type": "object",
		"properties": {
			"user_id": {
				"type": "string",
				"pattern": "^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$"
			}
		},
		"required": ["user_id"],
		"additionalProperties": False
	}

	try:
		validate(data, schema)
	except ValidationError as e:
		return jsonify({'message': 'Are you trying to do malicious staff?'})
	
	user_id = data['user_id']
	conn = get_db_connection()
	user_from_db = conn.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,)).fetchall()
	conn.close()
	if (len(user_from_db) != 0):
		response = ask_for_password_count(data)
		return jsonify(response)
	return jsonify({'message': "You shouldn't be here"})


@app.route("/verify-password", methods=['POST'])
def password_verify():
	data = request.get_json()
	schema = {
	"$schema": "http://json-schema.org/draft-07/schema#",
	"type": "object",
	"properties": {
		"user_id": {
		"type": "string",
		"pattern": "^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$"
		},
		"password": {
		"type": "string",
		"pattern": "^[a-zA-Z0-9]+$"
		}
	},
	"required": ["user_id", "password"]
	}

	try:
		validate(data, schema)
	except ValidationError as e:
		return jsonify({'message': 'Are you trying to do malicious staff?'})
	
	user_id = data["user_id"]
	conn = get_db_connection()
	user_from_db = conn.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchall()

	if (len(user_from_db) != 0):
		response = verify_password(data)
		print(response)
		return response
	return jsonify({'message': "You shouldn't be here"})

if __name__ == "__main__":
    app.run(port=8001)