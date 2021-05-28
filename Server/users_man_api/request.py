import requests

def change_password():
	url = 'http://127.0.0.1:5000/users/api/v1/chg_password/teste1@teste.pt'

	obj = {'old_pass':'password1', 'new_pass':'12qwaszx,.'} 

	i = requests.put(url, json = obj)

	print(i.text)



def remove_user():

	url = 'http://127.0.0.1:5000/users/api/v1/remove_user/teste1@teste.pt'

	i = requests.delete(url)

	print(i.text)

# change_password()
remove_user()
