import os
import glob

def get_files(email):
	data = {'nr_files': 0, 'files':[]}

	if os.path.exists(email):
		f = os.listdir(email)			
		
		for x in f:
			data['files'].append(x)

		data['nr_files'] = len(f)	

	return data

def delete_file(email, filename):	
	status = None

	if os.path.exists(email):
		status = os.remove(email+'/'+filename)

	return status


