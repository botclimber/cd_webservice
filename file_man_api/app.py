from flask import Flask, jsonify, request, send_from_directory
from lib import *

import os

app = Flask(__name__)

@app.route('/')
def index():
	return "root, files managment"


@app.route('/files/api/v1/files/<email>', methods=['GET'])
def get_files(email):
	
	response = get_files(email)
	return jsonify(response)	


@app.route('/files/api/v1/rm_file/<email>/<filename>', methods=['DELETE'])
def rm_file(email, filename):
	
	response = delete_file(email, filename)
	return jsonify(response)	


@app.route('/files/api/v1/upload/<email>', methods=['POST'])
def upload_file(email):
	#set expire time
	
	f = request.files['file']
	
	if os.path.exists(email) == False: os.mkdir(email)	
	response = f.save(email+'/'+f.filename)

	return jsonify(response)	


@app.route('/files/api/v1/download/<email>/<filename>', methods=['GET'])
def download_file(email, filename):
	
	# send it
	return send_from_directory(email, filename, as_attachment=True)




if __name__ == '__main__':
	app.run(port=4999, debug=True)

