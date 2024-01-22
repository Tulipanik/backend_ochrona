from flask import Flask, request, jsonify
import requests
import sqlite3
import random
import time
from jsonschema import validate, ValidationError

app = Flask(__name__)

password_manager_url = "http://127.0.0.1:8002/verify-password"
password_manager_url_count = "http://127.0.0.1:8002/ask-for-password-count"
password_manager_password_change = "http://127.0.0.1:8002/change-password"
verify_session = "http://127.0.0.1:8003/validate-session/"

def get_db_connection():
	conn = sqlite3.connect('user_database.db')
	conn.row_factory = sqlite3.Row
	return conn

def verify_password(user_id, password):
	response = requests.post(password_manager_url, json={'user_id': user_id, 'password': password})
	return response.json()

def ask_for_password_count (data):
	response = requests.post(password_manager_url_count, json=data)
	return response.json()

def random_delay():
    delay = random.uniform(1, 5)
    time.sleep(delay)

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
	
	random_delay()
	username = data["login"]
	conn = get_db_connection()
	user_from_db = conn.execute('SELECT user_id FROM users WHERE username = ?', (username,)).fetchall()
	conn.close()
	if (len(user_from_db) != 0):
		user_from_db = dict(user_from_db[0])["user_id"]
		return jsonify({'user_id': user_from_db})
	return jsonify({'message': 'User not verified'})

@app.route("/ask-for-combination", methods=["POST"])
def ask_for_combination ():
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
	user_from_db = conn.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,)).fetchone()
	conn.close()
	if (not(user_from_db is None)):
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
		"login": {
		"type": "string",
		"pattern": "^[a-zA-Z0-9]+$"
		},
		"password": {
		"type": "string",
		}
	},
	"required": ["login", "password"],
	"additionalProperties": False
	}

	try:
		validate(data, schema)
	except ValidationError as e:
		return jsonify({'message': 'Are you trying to do malicious staff?'})
	
	random_delay()
	login = data["login"]
	conn = get_db_connection()
	user_from_db = conn.execute('SELECT user_id FROM users WHERE username = ?', (login,)).fetchall()

	if (len(user_from_db) != 0):
		user_id = dict(user_from_db[0])['user_id']
		response = verify_password(user_id, data["password"])
		return response
	return jsonify({'message': "You shouldn't be here"})

@app.route("/change-password", methods=["POST"])
def change_password ():
	data = request.get_json()
	
	schema = {
          "$schema": "http://json-schema.org/draft-07/schema#",
          "type": "object",
          "properties": {
          "session_id": {
               "type": "string",
               "pattern": "^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$"
          },
          "password": {
               "type": "string",
			   "maxLenght": 20,
			   "minLenght": 8
          },
          "password_change_1": {
               "type": "string",
			   "maxLenght": 20,
			   "minLenght": 8
          },
          "password_change_2": {
               "type": "string",
               "maxLenght": 20,
			   "minLenght": 8
          }
          },
          "required": ["session_id", "password", "password_change_1", "password_change_2"],
          "additionalProperties": False
     }
	
	try:
		validate(data, schema)
	except ValidationError as e:
		return jsonify({'message': 'Are you trying to do malicious staff?'})

	response = requests.get(f"{verify_session}{data['session_id']}").json()

	if(not(response["valid"])):
		return jsonify({'message': 'You not have right premissions'})

	response = requests.post(f"{password_manager_password_change}", json=data).json()
	return response

@app.route("/get-user-id/<username>", methods=['GET'])
def get_user_id(username):
	conn = get_db_connection()
	id = conn.execute('SELECT user_id FROM users WHERE username = ?', (username,)).fetchone()

	if (id is None):
		return jsonify({'message': 'Are you trying to do malicious staff?'})
	
	conn.close()
	return jsonify({"user_id": dict(id)["user_id"]})


if __name__ == "__main__":
    app.run(port=8001)