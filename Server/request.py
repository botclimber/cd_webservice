import requests

site = 'http://127.0.0.1:5000/files/api/v1/upload'

filename = 'IPCA-Logo_rgb_v2.png'
up = {'file':(filename, open(filename, 'rb'), "multipart/form-data")}

print(up)

request = requests.post(site, files=up, headers={"Content-Type": "application/json","x-access-token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbF9rZXkiOiJhZG1pbkBhZG1pbi5wdCIsImV4cCI6MTYyMjMwNTM1Nn0.gV63sYjgLSSJdR726yLCVSL8dPc39ny6knPNLhPlP3w"})

print(request.text)
