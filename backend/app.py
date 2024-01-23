from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
from jsonschema import validate, ValidationError

url = "http://user-log:8001"
VALIDATE = "http://session:8003/validate-session/"
TRANSACTIONS = "http://transactions:8005/"
FRAGILE = "http://user-data:8004/"
headers = {"Content-Type": "application/json"}

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000'])


@app.route('/login-1', methods=['POST'])
def login():
    data = request.get_json()

    schema = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "login": {
      "type": "string"
    }
  },
  "required": ["login"],
  "additionalProperties": False
}
    
    try:
        validate(data, schema)
    except ValidationError as e:
        return jsonify({'message': 'Are you trying to do malicious staff?'})

    response = requests.post(f'{url}/verify-user', json=data, headers=headers)
    json = response.json()
    
    if "user_id" in json:
        response = requests.post(f"{url}/ask-for-combination", json=json, headers=headers)
        response = response.json()
        return response

    return jsonify({'message': "there's an error during verification process"})

@app.route('/login-2', methods=['POST'])
def login_2():
    data = request.get_json()

    schema = {
	"$schema": "http://json-schema.org/draft-07/schema#",
	"type": "object",
    "properties": {
        "login": {
        "type": "string"
        },
        "password": {
        "type": "string"
        }
    },
	"required": ["login", "password"],
	"additionalProperties": False
	}

    try:
        validate(data, schema)
    except ValidationError as e:
        return jsonify({'message': 'Are you trying to do malicious staff?'})
	
    login = data["login"]
    password = data["password"]
    response = requests.post(f'{url}/verify-password', json={"login": login, "password": password}, headers=headers)
    json = response.json()
    return json

@app.route('/verify-session', methods=['POST']) 
def verify_session():
    data = request.get_json()

    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "session_id": {
                "type": "string",
                }
        },
        "required": [ "session_id"],
        "additionalProperties": False
    }

    try:
        validate(data, schema)
    except ValidationError as e:
        return jsonify({'message': 'Are you trying to do malicious staff?'})
    
    response = requests.get(f"{VALIDATE}{data['session_id']}")

    return response.json()

@app.route('/get-user-data', methods=['POST'])
def get_user_data():
    data = request.get_json()

    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "session_id": {
                "type": "string",
                }
        },
        "required": [ "session_id"],
        "additionalProperties": False
    }

    try:
        validate(data, schema)
    except ValidationError as e:
        return jsonify({'message': 'Are you trying to do malicious staff?'})
    
    response = requests.post(f'{TRANSACTIONS}get-user-data', json=data, headers=headers).json()
    return response

@app.route('/get-transactions', methods=['POST'])
def get_transactions():
    data = request.get_json()

    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "session_id": {
                "type": "string",
                }
        },
        "required": ["session_id"],
        "additionalProperties": False
    }

    try:
        validate(data, schema)
    except ValidationError as e:
        return jsonify({'message': 'Are you trying to do malicious staff?'})
    
    response = requests.post(f'{TRANSACTIONS}check-transactions', json=data, headers=headers).json()
    return response

@app.route('/make-transaction', methods=['POST'])
def make_transaction():
    data = request.get_json()

    schema = {
          "$schema": "http://json-schema.org/draft-07/schema#",
          "type": "object",
          "properties": {
          "session_id": {
               "type": "string",
          },
          "amount": {
               "type": "string",
          },
          "title": {
               "type": "string",
          },
          "address": {
               "type": "string",
          },
          "account": {
               "type": "string",
          }
          },
          "required": ["amount", "title", "address", "account", "session_id"],
          "additionalProperties": False
     }
    
    try:
         validate(data, schema)
    except ValidationError as e:
         return jsonify({'message': 'Are you trying to do malicious staff?'})
    
    response = requests.post(f'{TRANSACTIONS}make-transaction', json=data, headers=headers).json()
    return response

@app.route('/get-fragile-data', methods=['POST'])
def get_fragile_data ():
    data = request.get_json()

    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "session_id": {
                "type": "string",
                }
        },
        "required": [ "session_id"],
        "additionalProperties": False
    }

    try:
        validate(data, schema)
    except ValidationError as e:
        return jsonify({'message': 'Are you trying to do malicious staff?'})
    
    response = requests.post(f'{FRAGILE}get-fragile-data', json=data, headers=headers).json()
    return response

@app.route('/change-password', methods=["POST"])
def change_password ():
    data = request.get_json()

    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "session_id": {
                "type": "string",
            },
            "password": {
                "type": "string",
            },
            "password_change_1": {
                "type": "string",
            },
            "password_change_2": {
                "type": "string",
            }
        },
        "required": [ "session_id", "password", "password_change_1", "password_change_2"],
        "additionalProperties": False
    }

    try:
        validate(data, schema)
    except ValidationError as e:
        return jsonify({'message': 'Are you trying to do malicious staff?'})

    response = requests.post(f'{url}/change-password', json=data, headers=headers).json()
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)