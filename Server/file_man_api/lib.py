import os
import glob

_path = 'file_man_api/'

def get_all_files(email):
	data = {'nr_files': 0, 'files':[]}

	if os.path.exists(_path+email):
		f = os.listdir(_path+email)			
		
		for x in f:
			data['files'].append(x)

		data['nr_files'] = len(f)	

	return data

def delete_file(email, filename):	
	status = None

	if os.path.exists(_path+email):
		status = os.remove(_path+email+'/'+filename)

	return status


