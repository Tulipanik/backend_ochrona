from flask import Flask, request, jsonify
from passlib.hash import argon2
import sqlite3
import requests
import string
import random
import math
from collections import Counter
from jsonschema import validate, ValidationError

app = Flask(__name__)

SESSION_URL = "http://session:8003"
headers = {"Content-Type": "application/json"}

def calculate_entropy(text):
    leng = 0
    stat = {}
    for symb in text:
        leng += 1
        if symb in stat:
                stat[symb] += 1
        else:
                stat[symb] = 1

    H = 0.0
    for znak in stat:
        p_i = stat[znak]/leng
        H -= p_i * math.log2(p_i)

    return H

def get_db_connection():
        conn = sqlite3.connect('password.db')
        conn.row_factory = sqlite3.Row
        return conn

def get_password_from_db(user_id):
	conn = get_db_connection()
	combination = conn.execute('SELECT last_elem FROM passwords WHERE user_id = ?', (user_id,)).fetchone()
	combination = dict(combination)['last_elem']

	if combination is None:
		return (False, "")

	hash_from_db = conn.execute('SELECT combination, hash FROM hash WHERE user_id = ? AND combination = ?', (user_id, combination)).fetchone()
	if (hash_from_db is None):
		return (False, "")
	
	hash_from_db = dict(hash_from_db)
	return (True, hash_from_db["hash"])


def check_try_count(user_id):
	conn = get_db_connection()
	conn.execute('UPDATE passwords SET try = try + 1 WHERE user_id = ?', (user_id,))
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
		"maxLength": 20,
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
	hash_from_db = conn.execute('SELECT last_elem, try FROM passwords WHERE user_id = ?', (user_to_retrive_password_count, )).fetchone()

	if (hash_from_db is None):
		conn.close()
		return jsonify({"message": "you shouldn't be here"})
	
	hash_from_db = dict(hash_from_db)
	if (hash_from_db['last_elem'] is None):
		elements = conn.execute('SELECT combination FROM hash WHERE user_id = ?', (user_to_retrive_password_count, )).fetchall()

		if (len(elements) == 0):
			conn.close()
			return jsonify({'message': 'Are you trying to do malicious staff?'})
		
		random_element = dict(random.choice(elements))["combination"]
		conn.execute('UPDATE passwords SET last_elem = ? WHERE user_id = ?', (random_element, user_to_retrive_password_count))
		conn.commit()
	else:
		random_element = hash_from_db['last_elem']

		if (hash_from_db["try"] == 3):
			return jsonify({"message": "You're account is locked, you cannot log in, contact with bank to resolve this issue"})
	
	conn.close()
	random_element = random_element.split("_")
	return jsonify({"elements": random_element})

@app.route('/change-password', methods=['POST'])
def change_password():
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

	response = requests.get(f"{SESSION_URL}/validate-session/{data['session_id']}").json()

	if (not(response["valid"])):
		return jsonify({'message': 'Are you trying to do malicious staff?'})
	
	password = data["password"]

	if (data["password_change_1"] != data["password_change_2"] or len(data["password_change_1"]) > 20 or len(data["password_change_1"]) < 8):
		return jsonify({'message': "Password not changed"})
	
	conn = get_db_connection()
	hash = conn.execute("SELECT hash FROM passwords WHERE user_id = ?", (response["user_id"], )).fetchone()
	conn.close()

	if(hash is None):
		return jsonify({'message': 'Are you trying to do malicious staff?'})
	
	hash = dict(hash)["hash"]
	is_valid = argon2.verify(password , hash)

	if (not(is_valid)):
		return jsonify({'message': 'Incorrect password'})
	
	enthropy = calculate_entropy(data["password_change_1"])

	if(enthropy < 3 ):
		return jsonify({'message': "Your password is too weak"})
	
	conn = get_db_connection()
	conn.execute('DELETE FROM hash WHERE user_id = ?', (response["user_id"], ))
	conn.commit()

	conn.execute('DELETE FROM passwords WHERE user_id = ?', (response["user_id"], ))
	conn.commit()

	password = data["password_change_1"]

	table_names_joined = set()
	min_length = 4
	max_length = len(password) - 1
	min_value = 0
	max_value = len(password) - 1

	while len(table_names_joined) < 20:
		list_length = random.randint(min_length, max_length)
		current_list = set()
		while len(current_list) != list_length:
			current_list.add(str(random.randint(min_value, max_value)))
		
		current_list = list(sorted(current_list))
		table_name = "_".join(current_list)
		table_names_joined.add(table_name)

		toHash = [password[int(j)] for j in current_list]
		toHash = "".join(toHash)
		toHash = argon2.using(rounds=5, salt = (''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))).encode('utf-8')).hash(toHash)


		conn.execute("INSERT OR REPLACE INTO hash (user_id, hash, combination) VALUES (?,?,?)", (response["user_id"], toHash, table_name ))
		conn.commit()


	hashed_password = argon2.hash(password)
	conn.execute('INSERT INTO passwords (user_id, hash, try) VALUES (?, ?, ?)', (response["user_id"], hashed_password, 0 ))

	conn.commit()

	return jsonify({'message': 'Password changed'})




if __name__ == "__main__":
	app.run(host="0.0.0.0", port="8002")
