from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

url = "http://127.0.0.1:8001"
VALIDATE = "http://127.0.0.1:8003/validate-session/"
TRANSACTIONS = "http://127.0.0.1:8005/"
headers = {"Content-Type": "application/json"}

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

@app.route('/login-1', methods=['POST'])
def login():
    data = request.get_json()
    print(data)
    response = requests.post(f'{url}/verify-user', json=data, headers=headers)
    json = response.json()
    print(json)
    
    if "user_id" in json:
        response = requests.post(f"{url}/ask-for-combination", json=json, headers=headers)
        response = response.json()
        print(response)
        return response

    return jsonify({'message': "there's an error during verification process"})

@app.route('/login-2', methods=['POST'])
def login_2():
    data = request.get_json()
    login = data["login"]
    password = data["password"]
    response = requests.post(f'{url}/verify-password', json={"login": login, "password": password}, headers=headers)
    json = response.json()
    print(json)
    return json

@app.route('/verify-session', methods=['POST']) 
def verify_session():
    data = request.get_json()
    print(data)
    response = requests.get(f"{VALIDATE}{data['session_id']}/{data['login']}")
    print(response.json())
    return response.json()

@app.route('/get-user-data', methods=['POST'])
def get_user_data():
    data = request.get_json()
    print(data)
    response = requests.post(f'{TRANSACTIONS}get-user-data', json=data, headers=headers).json()
    return response

@app.route('/get-transactions', methods=['POST'])
def get_transactions():
    data = request.get_json()
    print(data)
    response = requests.post(f'{TRANSACTIONS}check-transactions', json=data, headers=headers).json()
    return response

@app.route('/make-transaction', methods=['POST'])
def make_transaction():
    data = request.get_json()
    print(data)
    response = requests.post(f'{TRANSACTIONS}make-transaction', json=data, headers=headers).json()
    return response

if __name__ == "__main__":
    app.run(port=8000)