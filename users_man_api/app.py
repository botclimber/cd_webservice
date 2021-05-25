from flask import Flask, jsonify, request

app = Flask(__name__)

admin = {
	'email': 'admin@admin.pt',
	'password': '12qwaszx,.'
	}


users = []
groups = []
channels = []

status = False 


@app.route('/')
def index():
	return 'delusional'

@app.route('/users/api/v1/users', methods=['GET'])
def get_users():

	data = []
	for x in range(len(users)):
		data.append({'id':x,'name':users[x]['name'], 'email':users[x]['email']})	

	return jsonify(data)	


@app.route('/users/api/v1/groups', methods=['GET'])
def get_groups():
	
	data = []
	for x in range(len(groups)):
		data.append({'id':x,'group_name':groups[x]['group_name'], 'emails':groups[x]['emails']})	

	
	return jsonify(data)	


@app.route('/users/api/v1/channels', methods=['GET'])
def get_channels():
	
	
	data = []
	for x in range(len(channels)):
		data.append({'id':x,'channel_name':channels[x]['channel_name'], 'emails':channels[x]['emails'], 'msgs':channels[x]['msgs']})	

	
	return jsonify(data)	


@app.route('/users/api/v1/add_user', methods=['POST'])
def add_user():
	
	# name, email, password	
	content = request.json
	users.append(content)
	
	return jsonify(True)	



@app.route('/users/api/v1/add_group', methods=['POST'])
def add_group():

	# group_name, emails (string with emails divided by comma)
		
	content = request.json
	groups.append(content)	

	return jsonify(True)	


@app.route('/users/api/v1/add_channel', methods=['POST'])
def add_channel():
		
	# channel_name 

	content = request.json
	content['emails'] = [] 	
	content['msgs'] = [] 	
	channels.append(content)

	return jsonify(True)


@app.route('/users/api/v1/chg_password/<email>', methods=['PUT'])
def chg_password(email):
	# old_pass, new_pass		

	content = request.json

	for x in range(len(users)):
		if email == users[x]['email']:
			if content['old_pass'] == users[x]['password']:
				users[x]['password'] = content['new_pass']
				status = True
	

	return jsonify(status)	


@app.route('/users/api/v1/remove_user/<email>', methods=['DELETE'])
def rm_user(email):
	# remove user from data struct		

	for x in range(len(users)):
		if email == users[x]['email']: 
			users.pop(x)	
			status = True
			break			

	return jsonify(status)	



if __name__ == '__main__':
	app.run(debug = True, port = 5001)

