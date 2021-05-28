import requests

site = 'http://127.0.0.1:4999/files/api/v1/upload/teste@teste.pt'

filename = 'mg.jpg'
up = {'file':(filename, open(filename, 'rb'), "multipart/form-data")}

request = requests.post(site, files=up)

print(request.text)
