import socket
import sys
import getpass
try:

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

except socket.error as msg:
	print ('Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message: ' + msg[1])
	sys.exit()

print ('Socket Created')


host = ''
port = 33000

try:
	remote_ip = '192.168.1.20'

except socket.gaierror:
	print ('Hostname could not be resolved. Exiting')
	sys.exit()

print ('Ip addresss of ' + host + ' is ' + remote_ip)

s.connect((remote_ip , port))

print ('Socket Connected to ' + host + ' on ip ' + remote_ip)


while 1:
	reply = s.recv(4096).decode("utf8")
	if reply[-1] == '~':
		print(reply[:-1])
		
	else:
		print(reply)

	if reply[-1] == '~':
		message = getpass.getpass(' ')
	else:
		message = input()
	
	try :
		s.sendall(bytes(message, "utf8"))
	except socket.error:
		print('Send failed')
		sys.exit()

s.close()
