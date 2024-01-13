from flask import Flask, request, jsonify
import sqlite3
import requests

app = Flask(__name__)

VALIDATE = "http://127.0.0.1:8003/validate-session/"

def get_db_connection():
        conn = sqlite3.connect('transactions.db')
        conn.row_factory = sqlite3.Row
        return conn

@app.route("/make-transaction", methods=["POST"])
def make_transaction ():
    data = request.get_json()

    session = data["session_id"]
    response = requests.get(f'{VALIDATE}{session}').json()
    if (not(response["valid"])):
         return jsonify({"message": "You do not have rigth premission."})
    
    user = data["user_id"]
    to = data["account_number"]
    amount = data["amount"]
    title = data["title"]
    receiver_data = data["receiver_data"]
    conn = get_db_connection()
    acc_amount = dict((conn.execute('SELECT money_state FROM users WHERE user_id = ?', (user,)).fetchall())[0])["money_state"]
    if acc_amount < amount:
         return jsonify({"message": "You do not own such amount of money"})

    if len(to) != 26 or not(int(to)):
         return jsonify({"message": "Provided account number is incorrect"})

    conn.execute('INSERT INTO transactions (to_account, amount, title, receiver_data, user_id) VALUES (?, ?, ?, ?, ?)', (to, amount, title, receiver_data, user))
    conn.commit()
    
    get_to_account = conn.execute('SELECT user_id FROM users WHERE account number = ?', (to,))

    if len(get_to_account) == 0:
         return jsonify({"message": "Transfer realised correctly"})

    get_to_account = dict(get_to_account[0])["user_id"]
    conn.execute('UPDATE users SET money_state = money_state - ? WHERE user_id = ?', (amount, get_to_account))
    conn.commit()
    conn.close()


@app.route("/check-transactions", methods=["POST"])
def check_transactions ():
     data = request.get_json()

     session = data["session_id"]
     response = requests.get(f'{VALIDATE}{session}').json()
     if (not(response["valid"])):
          return jsonify({"message": "You do not have rigth premission."})

     conn = get_db_connection()
     data = conn.execute('SELECT * FROM transactions WHERE user_id = ?', (data["user_id"]))

     if len(data) == 0:
        return jsonify({"message": "There's no transactions yet"})
     
     data = dict(data[0])
     return jsonify(data)


if __name__ == "__main__":
    app.run(port="8005")