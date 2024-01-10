from flask import Flask
import sqlite3

app = Flask(__name__)

@app.route("/get-fragile-data", methods="POST")
def get_fragile_data():
	data=request.get_json();
	

if __name__=="__main__":
	app.run(port=8005)
