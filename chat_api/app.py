from lib import *
import requests

def load_channels():
	try:
		x = requests.get('http://127.0.0.1:5001/users/api/v1/channels')
	except: x = []

	return x	

channels = load_channels()
