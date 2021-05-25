from flask import Flask, jsonify, request
from lib import *

import requests

app = Flask(__name__)

def load_groups():
	try:
		x = requests.get('http://127.0.0.1/users/api/v1/groups')
	except: x = []
	
	return x

groups = load_groups()

@app.route('/')
def index():
	return "root"

@app.route('/box/api/v1/<email>', methods=['GET'])
def get_emails(email):
	
	response = get_emails(email)

	return jsonify(response)
	

@app.route('/box/api/v1/<email>/<int:email_id>', methods=['GET'])
def get_email(email, email_id):
	
	response = get_email(email, email_id)

	return jsonify(response)


@app.route('/box/api/v1/delete/<email>/<int:email_id>', methods=['DELETE'])
def del_email(email, email_id):
	
	response = del_email(email, email_id)

	return jsonify(response)


@app.route('/box/api/v1/write/<email>', methods=['GET, POST'])
def write_email(email):
	
	'''
	[to, subject, msg]
	- to: string (email or group id)
	- sub: string
	- msg: string
	'''

	content = request.json
	response = write_email(email, content)	

	return jsonify(response)


if __name__ == '__main__':
	app.run(debug=True)
