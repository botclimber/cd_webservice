import glob
import os
import random

def get_emails(email):

	if os.path.exists(email) == False:

		content = {'to': email, 'sub': '[ADMIN] new dir', 'msg': 'New dir has been created' }
		createDir(email)
		write_email('admin@admin.pt', content)
			

	os.chdir(email)
	myFiles = glob.glob('*.txt')
	
	data = {'total': len(myFiles), 'emails': []}
	for x in myFiles:
		_id = x.split('.')

		f = open(x, 'r')
		read = True if int(f.readline()) else False
		f_email = f.readline()
		sub = f.readline()		

		data['emails'].append({'id': _id[0],'from':f_email, 'sub': sub, 'read': read })
		

	return data


def get_email(email, email_id):

	if os.path.exists(email+'/'+str(email_id)+'.txt') == False: status = False
	else:
		f = open(email+'/'+str(email_id)+'.txt', 'r')
		status = f.readlines()[3:][0]
	
	return status


def del_email(email, email_id):
		
	if os.path.exists(email+'/'+str(email_id)+'.txt') == False: status = False
	else:
		status = os.remove(email+'/'+str(email_id)+'.txt')
	
	return status



def write_email(email, content):
	emails = content['to'].split(',')	

	for x in emails:
	
		if os.path.exists(x) == False: createDir(x)
			
		rand_id = random.randint(1000, 99999)
		f = open(x+'/'+str(rand_id)+'.txt', 'w')
		
		w = '0\n'+email+'\n'+content['sub']+'\n'+content['msg']	
			
		f.write(w)



def createDir(email):
	os.mkdir(email)


