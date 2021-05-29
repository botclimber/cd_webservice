from flask import Flask, request, redirect, url_for 
from flask.templating import render_template
import requests
import json

app = Flask(__name__)


url_api_users = 'http://127.0.0.1:5000/users/api/v1/'
url_api_chat = 'http://127.0.0.1:5000/chat/api/v1/'
url_api_email = 'http://127.0.0.1:5000/box/api/v1/'
url_api_files = 'http://127.0.0.1:5000/files/api/v1/'

global token
token = None


def _r(url, method, auth_tk = None, body = None ):
	header = {"Content-Type": "application/json","x-access-token": auth_tk }
	
	if method.upper() == 'POST':
		r = requests.post(url, json = body, headers = header)

	elif method.upper() == 'GET':
		r = requests.get(url, headers = header)

	elif method.upper() == 'DELETE':
		r = requests.delete(url, headers = header)
	
	elif method.upper() == 'PUT':
		r = requests.put(url, json=body, headers = header)
	
	try:
		response = json.loads(r.text)
	except:
		response = None

	return response

def imauser(_token):
	
	global token
	url = url_api_email 	
	status = False


	if token != None:
		r = _r(url, 'get', _token['token'])

		try: 
			if r['status'] == 401: token = None 
		except: status = True
	

	return status



@app.route('/')
def index():
	
	if token is None: 	
		return render_template('index.html')
	
	return render_template('home.html', user_type=token['user_type'])

@app.route('/login', methods=['POST'])
def login():
	global token	

	data = request.form

	url = 'http://127.0.0.1:5000/api/v1/login'
	r = requests.get(url, auth=(data['email'], data['password']))	

	if r.text != 'could not verify':
		token = json.loads(r.text)
		return render_template('home.html', user_type=token['user_type'])
	
	return redirect('/')



@app.route('/users')
def users():
	if not imauser(token): return redirect('/')	

	url = url_api_users+'users'
	
	r = requests.get(url, headers={"Content-Type": "application/json", "x-access-token": token['token']})

	return render_template('users.html', users = json.loads(r.text))




@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
	if not imauser(token): return redirect('/')	
	
	if request.method != 'POST': return render_template('add_user.html')	

	data = {'name':request.form['name'], 'email': request.form['email'], 'password':request.form['password'], 'user_type': request.form['user_type']}

	url = url_api_users+'add_user'
	
	r = requests.post(url, json=data ,headers={"Content-Type": "application/json", "x-access-token": token['token']})
	
	return redirect('/users')




@app.route('/delete_user/<action>')
def delete_user(action):

	if not imauser(token): return redirect('/')	

	if action == 'view': return render_template('del_user.html')
	elif action == 'delete':
		
		user_email = request.args.get('email')		

		url = url_api_users+'remove_user/'+user_email
		r = requests.delete(url, headers={"Content-Type": "application/json", "x-access-token": token['token']})
		
	return redirect('/users')




@app.route('/add_group', methods=['GET', 'POST'])
def add_group():
	if not imauser(token): return redirect('/')	

	if request.method != 'POST': 
		# return also all groups
		
		url = url_api_users+'groups'
		groups = _r(url, 'get', token['token'])

		return render_template('add_group.html', groups=groups)	

	data = {'group_name':request.form['group_name'], 'emails': request.form['emails']}
	url = url_api_users+'add_group'
	_r(url, 'post', token['token'], data)
	
	return redirect('/add_group')



@app.route('/add_channel', methods=['GET', 'POST'])
def add_channel():
	if not imauser(token): return redirect('/')	

	if request.method != 'POST': 
		# return also all groups
		
		url = url_api_users+'channels'
		channels = _r(url, 'get', token['token'])

		return render_template('add_channel.html', channels=channels)	

	data = request.form['channel_name'] 
	url = url_api_users+'add_channel'
	_r(url, 'post', token['token'], data)
	
	return redirect('/add_channel')



# ********** CHAT ***********
@app.route('/chat_index')
def chat_index():
	
	if not imauser(token): return redirect('/')	
	
	url = url_api_users+'channels'
	channels = _r(url, 'get', token['token'])



	return render_template("chat_index.html", channels=channels)



@app.route('/room', methods=['GET'])
def room():
	
	if not imauser(token): return redirect('/')	
	
	room = request.args.get('room')	
    
	if room:
		return render_template('room.html', name=token['token'] ,room=room)
	else:
		return redirect('/chat_index')




@app.route('/chg_password', methods=['GET', 'POST'])
def chg_password():
	
	if not imauser(token): return redirect('/')	
	if request.method != 'POST': 
		return render_template('chg_password.html')	

	data = {'old_password': request.form['old_password'] ,'new_password': request.form['new_password']}
	url = url_api_users+'chg_password'
	r = _r(url, 'put', token['token'], data)
	
	if r['status'] == 401: redirect('/')	
	
	return render_template('chg_password.html', r=r)





# EMAIL SYSTEM
@app.route('/email/<action>' , methods=['GET','POST'])
def email(action):	
	if not imauser(token): return redirect('/')	

	
	if request.method == 'POST': 
		email_type = int(request.form['email_type'])
		
		url = url_api_email+'write'
		method = 'post'
		
		data = {'msg': request.form['message'], 'sub':request.form['sub']}
		data['to'] = request.form['group'] if email_type else request.form['email'] 
		print(data)	
		_r(url, method, token['token'], data)

		return redirect('/email/all')


	if action == 'all':
		url = url_api_email	
		method = 'get'	

	elif action == 'details':
		url = url_api_email+'/'+request.args.get('email_id')
		method = 'get'	

	elif action == 'delete':
		url = url_api_email+'delete/'+request.args.get('email_id')
		method = 'delete'
	
	elif action == 'new_message':
		url = url_api_users+'groups'
		method = 'get'

	else: return redirect('/')

	data = _r(url, method, token['token'])

	
	return render_template('emails.html', data = data, action=action)



# FILE SYSTEM
@app.route('/files/<action>', methods=['GET', 'POST'])
def files(action):
	
	if not imauser(token): return redirect('/')	

	if request.method == 'POST':
		if action == 'upload':
			filename = request.form['file']
			url = url_api_files+'upload/'+token['email']
			method = 'post'
		
			data = {'file':(filename, open( filename ,'rb')) }			
			
			requests.post(url, files = data)
			
			return redirect('/files/view')			

	
	if action == 'view':
		url = url_api_files
		method = 'get'

	elif action == 'delete':
		url = url_api_files+'rm_file/'+request.args.get('file_name')	
		method = 'delete'
		_r(url, method, token['token'])		
		
		return redirect('/files/view')

	elif action == 'download':
		url = url_api_files+'download/'+request.args.get('file_name')	
		r = requests.get(url, allow_redirects=True)
		open(request.args.get('file_name'), 'wb').write(r.content)
	
		return redirect('/files/view')

	else:
		return redirect('/')

	data = _r(url, method, token['token'])	

	return render_template('files.html', data = data)



@app.route('/logout')
def logout():
	global token
	token = None
	
	return redirect('/')	


if __name__ == '__main__':
        app.run(debug = True, port=5001)





