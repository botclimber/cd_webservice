import requests


url = 'http://127.0.0.1:5000/users/api/v1/add_user'

for x in range(5):

	name = 'teste'+str(x)
	email = name+'@teste.pt'
	password = 'password'+str(x)

	obj = {'name': name, 'email': email, 'password': password}	

	i = requests.post(url, json = obj)
	

url = 'http://127.0.0.1:5000/users/api/v1/add_group'


group_name = 'grupo do wasapp'
emails = 'teste0@teste.pt, teste1@teste.pt, teste2@teste.pt'

obj = {'group_name': group_name, 'emails': emails }	

i = requests.post(url, json = obj)
	

	
url = 'http://127.0.0.1:5000/users/api/v1/add_channel'

for x in range(2):

	channel_name = 'teste'+str(x)

	obj = {'channel_name': channel_name }	

	i = requests.post(url, json = obj)
	


	
