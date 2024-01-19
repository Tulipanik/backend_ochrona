from flask import Flask, request, jsonify
import sqlite3
from Crypto.Cipher import AES
import requests
from dotenv import load_dotenv
import os
from jsonschema import validate, ValidationError

app = Flask(__name__)

load_dotenv()
VALIDATE = "http://127.0.0.1:8003/validate-session/"

def get_data_from_db(user_id):
    conn = sqlite3.connect('fragile_data.db')
    conn.row_factory = sqlite3.Row
    data = conn.execute('SELECT * FROM fragile_data WHERE user_id = ?', (user_id,))
    if (len(data) == 0):
        return {}
    conn.close()
    return dict(data[0])

def decode_data (toDecode, tag):
    nonce = os.getenv('NONCE')
    key = os.getenv('KEY')
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(toDecode, tag)
    return plaintext

@app.route("/get-fragile-data", methods=["POST"])
def get_fragile_data ():
    data = request.get_json()

    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
        "user_id": {
            "type": "string",
            "pattern": "^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
        },
        "session_id": {
            "type": "string",
            "pattern": "^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
        }
        },
        "required": ["user_id", "session_id"],
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

    session = data["session_id"]
    response = requests.get(f'{VALIDATE}{session}').json()
    if (not(response["valid"])):
        return jsonify({"message": "You do not have rigth premission."})

    fragile_data = get_data_from_db(data["user_id"])
    if (len(fragile_data) == 0):
        return {"message": "Are you trying to do malicious staff?"}

    id_card = decode_data(fragile_data["id_card"],fragile_data["id_card_tag"])
    card_number = decode_data(fragile_data["card_number"],fragile_data["card_number_tag"])
    return jsonify({"cardId": id_card, "cardNumber": card_number})
    
if __name__ == "__main__":
    app.run(port="8004")
