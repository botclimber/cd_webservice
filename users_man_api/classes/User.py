

class User:

	def __init__(self, name, email, password = None):
		self.name = name	
		self.email = email
		self.password = password

class Users:

	users = []
	status = True
	
	def __init__(self):
		pass

	def newUser(user):		

		if user.name != "" and user.email != "" and user.password != None:
			Users.users.append(user)
		
		else: status = 'all fields required' 			

		return status		

	def changePassword(new_password):
		pass

	def deleteUser(email):
		pass


class MsgBox:
	
	def __init__(self, email):
		self.box_id = 'box_'+email 
		self.readen = []
		
		self.msgs = self.__msgs()		

	def __msgs(self):
		# upload messages by self.box_id
		pass


	def createDir(self):
		pass


	def getLength(self):
		pass


	def getAll(self):
		# send diff between read and unread
		pass


	def getOne(self, msg_id):
		pass

		
	def delete(self, msg_id):
		pass

	def __read(self):
		pass



class Msg(MsgBox):

	def __init__(self, sub, msg):
		self.sub = sub
		self.msg = msg

	def send(self, to):
		pass


		
	


class UsersGroupPerm:
	
	def __init__(self, group):
		self.group = [group]	



class UsersChannelChat:
	
	def __init__(self, channel)	

	


class FileManagment:
	
	def __init__(self, email):
		self.drive_id = 'drive_'+email
		self.files = self.__files()


	def __files(self):
		pass


	def upload(self, _file):	
		# set expire time
		pass
	

	def download(self, file_id):
		pass


	def getAll(self):
		pass
	

	def delete(self, file_id):
		pass


	def __setExpTime(self):
		pass




user = User("teste@teste.pt", '12qwaszx,.')
print(user.email)

users = Users
users.newUser(user)

print(users.users)
print(users.users[0].password)
