import glob
import os
import random

_path = 'email_api/'

def get_all_emails(email):

	if os.path.exists(_path+email) == False:

		content = {'to': email, 'sub': '[ADMIN] new dir', 'msg': 'New dir has been created' }
		createDir(email)
		w_email('admin@admin.pt', content)
			

	os.chdir(_path+email)
	myFiles = glob.glob('*.txt')
	
	data = {'total': len(myFiles), 'emails': []}
	for x in myFiles:
		_id = x.split('.')

		f = open(x, 'r')
		read = True if int(f.readline()) else False
		f_email = f.readline()
		sub = f.readline()		

		data['emails'].append({'id': _id[0],'from':f_email, 'sub': sub, 'read': read })
		
	os.chdir('../../')
	return data


def get_one_email(email, email_id):

	if os.path.exists(_path+email+'/'+str(email_id)+'.txt') == False: status = False
	else:
		
		f = open(_path+email+'/'+str(email_id)+'.txt', 'r')
		status = f.read()
		status = '1\n'+status[2:]
		f.close()
		
		fi = open(_path+email+'/'+str(email_id)+'.txt', 'w')
		fi.write(status)
		fi.close()
		
		f = open(_path+email+'/'+str(email_id)+'.txt', 'r')
		status = f.readlines()[3:][0]
	
	return status




def del_sng_email(email, email_id):
		
	if os.path.exists(_path+email+'/'+str(email_id)+'.txt') == False: status = False
	else:
		status = os.remove(_path+email+'/'+str(email_id)+'.txt')
	
	return status



def w_email(email, content):
	emails = content['to'].split(',')	

	for x in emails:
		x = x.strip()		

		if os.path.exists(_path+x) == False: createDir(x)
			
		rand_id = random.randint(1000, 99999)
		f = open(_path+x+'/'+str(rand_id)+'.txt', 'w')
		
		w = '0\n'+email+'\n'+content['sub']+'\n'+content['msg']	
			
		f.write(w)



def createDir(email):
	os.mkdir(_path+email)


