from flask import Flask, session, request, jsonify
import sqlite3
import uuid
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

DB_FILE = "session.db"
SESSION_EXPIRATION_TIME = timedelta(minutes=5)
USER_LOG = "http://127.0.0.1:8001/get-user-id"

@app.route('/create-session/<user_id>', methods=['GET'])
def create_session(user_id):

	session_id = str(uuid.uuid4())
	
	with sqlite3.connect(DB_FILE) as conn:
		created_time = datetime.now().isoformat()
		conn.execute('INSERT OR REPLACE INTO sessions (session_id, user_id, creation) VALUES (?, ?, ?)', (session_id, user_id, created_time))
	return jsonify({'session_id': session_id})

@app.route('/validate-session/<session_id>/<username>', methods=['GET'])
def validate_session(session_id, username):
    username = requests.get(f"{USER_LOG}/{username}").json()
    if 'message' in username:
         return jsonify({'valid': False})

    print(username)
    
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.execute('SELECT creation FROM sessions WHERE session_id = ? AND user_id = ?', (session_id, username["user_id"]))
        row = cursor.fetchone()

    if row:
        created_at = datetime.fromisoformat(row[0])
        current_time = datetime.now()
        if current_time - created_at <= SESSION_EXPIRATION_TIME:
            return jsonify({'valid': True, 'user_id': username["user_id"]})
    
    return jsonify({'valid': False})

@app.route('/delete-session/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('DELETE FROM sessions WHERE session_id = ?', (session_id,))
    
    return jsonify({'message': 'Session deleted'})

if __name__=="__main__":
	app.run(port=8003)
