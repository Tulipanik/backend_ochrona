from flask import Flask, session, request, jsonify
import sqlite3
import uuid
import re
from datetime import datetime, timedelta

app = Flask(__name__)

DB_FILE = "session.db"
SESSION_EXPIRATION_TIME = timedelta(minutes=5)

@app.route('/create-session/<user_id>', methods=['GET'])
def create_session(user_id):

    regex_pattern = r"^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$"
    
    if not(re.match(regex_pattern, user_id)): 
        return jsonify({"message": "Are you trying to do malicious staff?"})
    
    session_id = str(uuid.uuid4())
	
    with sqlite3.connect(DB_FILE) as conn:
        created_time = datetime.now().isoformat()
        conn.execute('INSERT OR REPLACE INTO sessions (session_id, user_id, creation) VALUES (?, ?, ?)', (session_id, user_id, created_time))
    
    return jsonify({'session_id': session_id})

@app.route('/validate-session/<session_id>', methods=['GET'])
def validate_session(session_id):

    regex_pattern = r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"

    if not(re.match(regex_pattern, session_id)): 
        return jsonify({"message": "Are you trying to do malicious staff?"})

    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.execute('SELECT user_id, creation FROM sessions WHERE session_id = ?', (session_id,))
        row = cursor.fetchone()

    if row:
        created_at = datetime.fromisoformat(row[1])
        username = row[0]
        current_time = datetime.now()
        if current_time - created_at <= SESSION_EXPIRATION_TIME:
            created_time = datetime.now().isoformat()
            with sqlite3.connect(DB_FILE) as conn:
                conn.execute('UPDATE sessions SET creation = ? WHERE session_id = ?', (created_time, session_id))
                conn.commit()

            return jsonify({'valid': True, 'user_id': username})
    
    return jsonify({'valid': False})

@app.route('/delete-session/<session_id>', methods=['DELETE'])
def delete_session(session_id):

    regex_pattern = r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"

    if not(re.match(regex_pattern, session_id)): 
        return jsonify({"message": "Are you trying to do malicious staff?"})
    
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('DELETE FROM sessions WHERE session_id = ?', (session_id,))
    
    return jsonify({'message': 'Session deleted'})

if __name__=="__main__":
	app.run(host="0.0.0.0", port=8003)
