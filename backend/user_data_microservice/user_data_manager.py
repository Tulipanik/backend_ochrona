from flask import Flask, request, jsonify
import sqlite3
from Crypto.Cipher import AES
import requests
from dotenv import load_dotenv
import os
from jsonschema import validate, ValidationError

app = Flask(__name__)

load_dotenv()
VALIDATE = "http://session:8003/validate-session/"

def get_data_from_db(user_id):
    conn = sqlite3.connect('fragile_data.db')
    conn.row_factory = sqlite3.Row
    data = conn.execute('SELECT * FROM fragile_data WHERE user_id = ?', (user_id,)).fetchone()
    conn.close()
    if (data is None):
        return None
    return dict(data)

def decode_data (toDecode, tag):
    nonce = os.getenv('NONCE').encode('utf-8')
    key = os.getenv('KEY').encode('utf-8')
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(toDecode, tag)
    return plaintext.decode('utf-8')

@app.route("/get-fragile-data", methods=["POST"])
def get_fragile_data ():
    data = request.get_json()

    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
        "session_id": {
            "type": "string","pattern": "^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
        }
        },
        "required": [ "session_id"],
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

    fragile_data = get_data_from_db(response["user_id"])
    if (fragile_data is None):
        return jsonify({"message": "Are you trying to do malicious staff?"})

    id_card = decode_data(fragile_data["id_card"],fragile_data["id_card_tag"])
    card_number = decode_data(fragile_data["card_number"],fragile_data["card_number_tag"])

    return jsonify({"card_id": id_card, "card_number": card_number})
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8004")
