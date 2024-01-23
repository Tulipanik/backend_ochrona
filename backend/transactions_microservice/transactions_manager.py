from flask import Flask, request, jsonify
import sqlite3
import requests
from jsonschema import validate, ValidationError

app = Flask(__name__)

VALIDATE = "http://session:8003/validate-session/"

def get_db_connection():
        conn = sqlite3.connect('transactions.db')
        conn.row_factory = sqlite3.Row
        return conn

@app.route("/make-transaction", methods=["POST"])
def make_transaction ():
    data = request.get_json()

    schema = {
          "$schema": "http://json-schema.org/draft-07/schema#",
          "type": "object",
          "properties": {
          "session_id": {
               "type": "string",
               "pattern": "^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$"
          },
          "amount": {
               "type": "string",
               "pattern": "^(10000(\.00?)?|\d{0,4}(\.\d{1,2})?)$"
          },
          "title": {
               "type": "string",
               "maxLength": 35,
               "pattern": "^[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ0-9, -]+$"
          },
          "address": {
               "type": "string",
               "maxLength": 105,
               "pattern": "^[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ0-9, -]+$"
          },
          "account": {
               "type": "string",
               "pattern": "^\\d{26}$"
          }
          },
          "required": ["amount", "title", "address", "account", "session_id"],
          "additionalProperties": False
     }
    
    try:
         validate(data, schema)
    except ValidationError as e:
         return jsonify({'message': 'Are you trying to do malicious staff?'})
         
    session = data["session_id"]
    response = requests.get(f'{VALIDATE}{session}').json()
    if (not(response["valid"])):
         return jsonify({"message": "You do not have rigth premission."})
    
    user = response["user_id"]
    to = data["account"]
    amount = data["amount"]
    title = data["title"]
    receiver_data = data["address"]

    conn = get_db_connection()
    acc_amount = dict((conn.execute('SELECT money_state FROM users WHERE user_id = ?', (user,)).fetchone()))["money_state"]
    if acc_amount < float(amount):
         return jsonify({"message": "You do not own such amount of money"})

    conn.execute('INSERT INTO transactions (to_account, amount, title, receiver_data, user_id) VALUES (?, ?, ?, ?, ?)', (to, amount, title, receiver_data, user))
    conn.commit()
    
    conn.execute('UPDATE users SET money_state = money_state - ? WHERE user_id = ?', (amount, user))
    conn.commit()

    get_to_account = conn.execute('SELECT user_id FROM users WHERE account_number = ?', (to,)).fetchone()

    if get_to_account is None:
         return jsonify({"message": "Transfer realised correctly"})


    get_to_account = dict(get_to_account)["user_id"]

    conn.execute('UPDATE users SET money_state = money_state - ? WHERE user_id = ?', (amount, get_to_account))
    conn.commit()
    conn.close()

    return jsonify({"message": "Transfer realised correctly"})


@app.route("/check-transactions", methods=["POST"])
def check_transactions ():
     data = request.get_json()

     schema = {
          "$schema": "http://json-schema.org/draft-07/schema#",
          "type": "object",
          "properties": {
               "session_id": {
                    "type": "string",
                    "pattern": "^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
               }
          },
          "required": ["session_id"],
          "additionalProperties": False
     }

     try:
          validate(data, schema)
     except ValidationError as e:
          return jsonify({'message': 'Are you trying to do malicious staff?'})
     
     session = data["session_id"]
     response = requests.get(f'{VALIDATE}{session}').json()
     if (not(response["valid"])):
          return jsonify({"message": "You do not have rigth premission."})

     conn = get_db_connection()
     data = conn.execute('SELECT * FROM transactions WHERE user_id = ?', (response["user_id"], )).fetchall()
     conn.close()

     if len(data) == 0:
          return jsonify({"message": "There's no transactions yet"})

     for i in range(0, len(data)):
          data[i] = dict(data[i])
     
     return jsonify({'list': data})

@app.route('/get-user-data', methods=['POST'])
def get_user_data ():
     data = request.get_json()

     schema = {
          "$schema": "http://json-schema.org/draft-07/schema#",
          "type": "object",
          "properties": {
               "session_id": {
                    "type": "string",
                    "pattern": "^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
               }
          },
          "required": ["session_id"],
          "additionalProperties": False
     }

     try:
          validate(data, schema)
     except ValidationError as e:
          return jsonify({'message': 'Are you trying to do malicious staff?'})
     
     session = data["session_id"]
     response = requests.get(f'{VALIDATE}{session}').json()
     if (not(response["valid"])):
          return jsonify({"message": "You do not have rigth premission."})
     
     conn = get_db_connection()
     data = conn.execute('SELECT * FROM users WHERE user_id = ?', (response["user_id"], )).fetchone()
     conn.close()

     data = dict(data)
     return jsonify({"money": data["money_state"], "account": data["account_number"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8005")