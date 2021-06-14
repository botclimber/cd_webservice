import os
from flask import Flask, render_template, request, jsonify, make_response, send_from_directory
from flask_socketio import *

from functools import wraps
import jwt
import datetime

from email_api.lib import *
from file_man_api.lib import *


app = Flask(__name__)
app.config['SECRET_KEY'] = '21savage'
socketio = SocketIO(app, cors_allowed_origins='*')


users = [{'name':'admin','email':'admin@admin.pt','password':'12qwaszx,.','user_type':0}]
groups = []
channels = []

status = False


@app.route('/')
def index():
	return render_template('index.html')

# LOGIN
@app.route('/api/v1/login/')
def login():
    
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'wwww-Authenticate':'Basic realm="Login required!"'})

    user = False
    for x in range(len(users)):
        if auth.username == users[x]['email']:
            user = users[x]

    if not user:
        return make_response('could not verify', 401, {'wwww-Authenticate':'Basic realm="Login required!"'})
        
    if auth.password == user['password']:
        token = jwt.encode({'email_key': user['email'], 'exp': datetime.datetime.utcnow()+datetime.timedelta(minutes=30) }, app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({'token': token, 'email': user['email'], 'user_type': user['user_type']})

    return make_response('could not verify', 401, {'wwww-Authenticate':'Basic realm="Login required!"'})


# SESSION VERIFICATION
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            for x in range(len(users)):
                if data['email_key'] == users[x]['email']: current_user = users[x]
        
        except:
            return jsonify({'message': 'Token is invalid', 'status': 401}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated


# *************** USERS Managment ***************
@app.route('/users/api/v1/users', methods=['GET'])
@token_required
def get_users(current_user):

	data = []
	for x in range(len(users)):
		data.append({'id':x,'name':users[x]['name'], 'email':users[x]['email']})	

	return jsonify(data)	


@app.route('/users/api/v1/groups', methods=['GET'])
@token_required
def get_groups(current_user):
	
	data = []
	for x in range(len(groups)):
		data.append({'id':x,'group_name':groups[x]['group_name'], 'emails':groups[x]['emails']})	

	
	return jsonify(data)	


@app.route('/users/api/v1/channels', methods=['GET'])
@token_required
def get_channels(current_user):
	
	return jsonify(channels)	


@app.route('/users/api/v1/add_user', methods=['POST'])
@token_required
def add_user(current_user):
	
	# name, email, password, user_type [0 (admin) ,1 (other)]
	content = request.json
	users.append(content)
	
	return jsonify(True)	



@app.route('/users/api/v1/add_group', methods=['POST'])
@token_required
def add_group(current_user):

	# group_name, emails (string with emails divided by comma)
		
	content = request.json
	groups.append(content)	

	return jsonify(True)	


@app.route('/users/api/v1/add_channel', methods=['POST'])
@token_required
def add_channel(current_user):
		
	# channel_name 

	content = request.json
	if content not in channels: channels.append(content)

	return jsonify(True)


@app.route('/users/api/v1/chg_password', methods=['PUT'])
@token_required
def chg_password(current_user):
	# old_pass, new_pass		
	status = False
	content = request.json

	for x in range(len(users)):
		if current_user['email'] == users[x]['email']:
			if content['old_password'] == users[x]['password']:
				users[x]['password'] = content['new_password']
				status = True
	
	print(users)
	return jsonify(status)	


@app.route('/users/api/v1/remove_user/<user_email>', methods=['DELETE'])
@token_required
def rm_user(current_user, user_email):
	# remove user from data struct		

	for x in range(len(users)):
		if user_email == users[x]['email']:
			
			users.pop(x)	    
			status = True
			break			

	return jsonify(status)	
# ************************************


# *************** CHAT ***************

@socketio.on('send_message')
def handle_send_message_event(data):
    app.logger.info("{} has sent message to the room {}:{}".format(data['name'], data['room'], data['message']))
    socketio.emit('receive_message', data, room=data['room'])


@socketio.on('join_room')
def handle_join_room_event(data):
    app.logger.info("{} has joined the room {}".format(data['name'], data['room']))
    join_room(data['room'])
    socketio.emit('join_room_announcement', data, room=data['room'])


@socketio.on('leave_room')
def handle_leave_room_event(data):
    app.logger.info("{} has left the room {}".format(data['name'], data['room']))
    leave_room(data['room'])
    socketio.emit('leave_room_announcement', data, room=data['room'])
# ************************************


# *************** Email system ***************
@app.route('/box/api/v1/', methods=['GET'])
@token_required
def get_emails(current_user):
    
    response = get_all_emails(current_user['email'])
    
    return jsonify(response)


@app.route('/box/api/v1/<int:email_id>', methods=['GET'])
@token_required
def get_email(current_user, email_id):
    
    response = get_one_email(current_user['email'], email_id)
    return jsonify(response)


@app.route('/box/api/v1/delete/<int:email_id>', methods=['DELETE'])
@token_required
def del_email(current_user, email_id):
    
    response = del_sng_email(current_user['email'], email_id)
    data = get_all_emails(current_user['email'])
 
    return jsonify(data)


@app.route('/box/api/v1/write', methods=['POST'])
@token_required
def write_email(current_user):
    
    '''
        [to, subject, msg]
        - to: string (email, emails by comma)
        - sub: string
        - msg: string
        '''
    
    content = request.json
    response = w_email(current_user['email'], content)
    
    return jsonify(response)

# ************************************

# *************** File managment system ***************

@app.route('/files/api/v1/', methods=['GET'])
@token_required
def get_files(current_user):
    
    response = get_all_files(current_user['email'])
    return jsonify(response)


@app.route('/files/api/v1/rm_file/<filename>', methods=['DELETE'])
@token_required
def rm_file(current_user, filename):
    
    response = delete_file(current_user['email'], filename)
    return jsonify(response)


@app.route('/files/api/v1/upload/<email>', methods=['GET', 'POST'])
def upload_file(email):
    #set expire time
    
    f = request.files['file']
 
    if os.path.exists('file_man_api/'+email) == False: os.mkdir('file_man_api/'+email)
    response = f.save('file_man_api/'+email+'/'+f.filename)
    
    return jsonify(response)


@app.route('/files/api/v1/download/<path:filename>', methods=['GET'])
@token_required
def download_file(current_user, filename):
    print(os.getcwd())
    # send it
    
    return send_from_directory('file_man_api/'+current_user['email'], filename, as_attachment=True)

# ************************************


if __name__ == '__main__':
	socketio.run(app, debug = True)

