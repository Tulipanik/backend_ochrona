from flask import Flask, request, jsonify
from passlib.hash import argon2
import sqlite3
import requests
import ast
import random
import math
from collections import Counter
from jsonschema import validate, ValidationError

app = Flask(__name__)

SESSION_URL = "http://127.0.0.1:8003"
headers = {"Content-Type": "application/json"}

def calculate_entropy(data):
    data_size = len(data)
    char_count = Counter(data)

    probabilities = [char_count[char] / data_size for char in set(data)]

    entropy = -sum(p * math.log2(p) for p in probabilities)

    return entropy

def get_db_connection():
        conn = sqlite3.connect('password.db')
        conn.row_factory = sqlite3.Row
        return conn

def get_password_from_db(user_id):
	conn = get_db_connection()
	combination = conn.execute('SELECT last_elem FROM passwords WHERE user_id = ?', (user_id,)).fetchone()
	print(combination)
	combination = dict(combination[0])['last_elem']

	if combination is None:
		return (False, "")
	
	format = f'SELECT hash FROM {combination} WHERE user_id = ?'
	hash_from_db = conn.execute(format, (user_id,)).fetchall()
	if (len(hash_from_db) == 0):
		return (False, "")
	
	hash_from_db = dict(hash_from_db[0])
	print(hash_from_db)
	return (True, hash_from_db["hash"])


def check_try_count(user_id):
	conn = get_db_connection()
	conn.execute('UPDATE passwords SET try = try + 1 WHERE user_id = ?', (user_id,))
	print("updated")
	conn.commit()
	tries = conn.execute('SELECT try FROM passwords WHERE user_id = ?', (user_id, )).fetchone()
	conn.close()
	return dict(tries)["try"]

def clean_after_correct_verification(user_id):
	conn = get_db_connection()
	conn.execute('UPDATE passwords SET try = 0, last_elem = ? WHERE user_id = ?', (None, user_id,))
	conn.commit()
	conn.close()


@app.route("/verify-password", methods=['POST'])
def verify_password():
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

	hash_to_check_with = get_password_from_db(data["user_id"])

	tries = check_try_count(data["user_id"])
	if (tries > 3):
		return jsonify({"message": "You're account is locked, you cannot log in, contact with bank to resolve this issue"})

	if(hash_to_check_with[0]):	
		is_valid = argon2.verify(data["password"] , hash_to_check_with[1])
		if(is_valid):
			clean_after_correct_verification(data["user_id"])
			response = requests.get(f"{SESSION_URL}/create-session/{data['user_id']}", headers=headers).json()
			return response

		return jsonify({"message": "invalid password"})
	return jsonify({"message": "you shouldn't be here"})

@app.route('/ask-for-password-count', methods=['POST'])
def get_password_count():
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
	
	user_to_retrive_password_count = data["user_id"]
	conn = get_db_connection()
	hash_from_db = conn.execute('SELECT hash_list, last_elem, try FROM passwords WHERE user_id = ?', (user_to_retrive_password_count, )).fetchall()
	conn.close()

	if (len(hash_from_db) == 0):
		return jsonify({"message": "you shouldn't be here"})
	
	hash_from_db = dict(hash_from_db[0])
	if (hash_from_db['last_elem'] is None):
		hash_from_db = hash_from_db["hash_list"]
		list = ast.literal_eval(hash_from_db)
		random_element = random.choice(list).split("_")[1:]
		conn = get_db_connection()
		conn.execute('UPDATE passwords SET last_elem = ? WHERE user_id = ?', (str(random_element), user_to_retrive_password_count))
		conn.commit()
	else:
		random_element = ast.literal_eval(hash_from_db['last_elem'])
		print(hash_from_db)
		if (hash_from_db["try"] == 3):
			return jsonify({"message": "You're account is locked, you cannot log in, contact with bank to resolve this issue"})
	
	return jsonify({"elements": str(random_element)})

@app.route('/change-password', methods=['POST'])
def change_password():
	data = request.get_json()
	password = data["password"]

	calculate_entropy(password)




if __name__ == "__main__":
	app.run(port="8002")
