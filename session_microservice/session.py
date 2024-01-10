from flask import Flask, session, request, jsonify, session
from flask_session import Session
import requests

app = Flask(__name__)
app.config["SESSION_PERMAMENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/create-session', methods=['POST'])
def create_session():
	data = request.get_json()
	
	user_id = request["user_id"]
	session["name"] = user_id

@app.route('/delete-session', methods=['POST'])
def delete_session():
	data = request.get_json()
	
	user_id = request["user_id"]
	session["name"] = None 	

if __name__=="__main__":
	app.run(port=8003)
