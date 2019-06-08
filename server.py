import socket
import sys
import sqlite3
from _thread import *


def menu(conn, data):
	if data == 'p1':
		msg = 'You have ' + str(len(p1_messages)) + ' total messages \n'
		conn.send(bytes(msg, "utf8"))
	elif data == 'p2':
		msg = 'You have ' + str(len(p2_messages)) + ' total messages \n'
		conn.send(bytes(msg, "utf8"))
	msg = 'Enter 1 to Logout\n'
	conn.send(bytes(msg, "utf8"))
	msg = 'Enter 2 to Broadcast a message\n'
	conn.send(bytes(msg, "utf8"))
	msg = 'Enter 3 to Send a Message to a User\n'
	conn.send(bytes(msg, "utf8"))
	msg = 'Enter 4 to check your messages\n'
	conn.send(bytes(msg, "utf8"))
	msg = 'Enter 5 to change your password'
	conn.send(bytes(msg, "utf8"))


HOST = ''
PORT = 33000
conn_list = []
login_list = [('p1', '123'), ('p2', '111'), ('p3', '100')]
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print ('Socket created')

try:
	s.bind((HOST, PORT))
except socket.error as msg:
	print("Bind failed. Error Code: {} Message: {}".format(str(msg[0]), msg[1]))
	sys.exit()

print ('Socket bind complete')

s.listen(10)
print ('Socket now listening')

pwdflag = '~'

p1_messages = []
p2_messages = []


def clientthread(conn):
	success = False

	conn_list.append(conn)
	while True:
		while success == False:
			msg = 'Enter Username'

			conn.send(bytes(msg, "utf8"))
			data = conn.recv(4096).decode("utf8")

			msg = 'Enter Password: ' + str(pwdflag)

			conn.send(bytes(msg, "utf8"))
			data1 = conn.recv(4096).decode("utf8")

			with sqlite3.connect("Login.db") as db:
				cursor = db.cursor()

			find_user = ('SELECT * FROM user WHERE username = ? AND password = ?')
			cursor.execute(find_user, [(data),(data1)])
			results = cursor.fetchall()
			print(results)
			if results:
				for i in results:
					msg = 'Welcome ' + i[0]
					conn.send(bytes(msg, "utf8"))
					success = True
					break

			else:
				msg = "Invalid username or password"
				conn.send(bytes(msg, "utf8"))
				success = False

		while success == True:
			menu(conn, data)
			menu_data = conn.recv(4096).decode("utf8")
			if menu_data == "":
				menu(conn, data)

			elif menu_data == '1':
				msg = 'Logging out'
				conn.send(bytes(msg, "utf8"))
				success = False
				break
		
			elif menu_data == '2':
				msg = 'Send a message to broadcast: '
				conn.send(bytes(msg, "utf8"))
				data1 = conn.recv(4096).decode()
				for conns in conn_list:
					if conns == conn:
						continue
					else:
						msg = 'Message from ' + data + '\n'
						conns.send(bytes(msg, "utf8"))
						conns.send(bytes(data1, "utf8"))

			elif menu_data == '3':
				msg = 'Who are you sending to?'

				conn.send(bytes(msg, "utf8"))

				user_send = conn.recv(4096).decode()
				msg = 'Enter the message to send'
				conn.send(bytes(msg, "utf8"))
				mess = conn.recv(4096).decode()
				if user_send == 'p1':
					p1_messages.append('Message from ' + data + ': ' + mess + '\n')
				elif user_send == 'p2':
					p2_messages.append('Message from ' + data + ': ' + mess + '\n')

			elif menu_data == '4':
				if data == 'p1':
					if len(p1_messages) == 0:
						msg = 'No new messages\n'
						conn.send(bytes(msg, "utf8"))
					else:
						for msg in p1_messages:
							conn.send(bytes(msg, "utf8"))

				elif data == 'p2':
					if len(p2_messages) == 0:
						msg = 'No new messages\n'
						conn.send(bytes(msg, "utf8"))
					else:
						for msg in p2_messages:
							conn.send(bytes(msg, "utf8"))

			elif menu_data == '5':
				with sqlite3.connect("Login.db") as db:
					cursor = db.cursor()

				msg = 'Input old password: '
				conn.send(bytes(msg, "utf8"))
				data1 = conn.recv(4096).decode("utf8")

				find_user = ('SELECT * FROM user WHERE username = ? AND password = ?')
				cursor.execute(find_user, [(data), (data1)])
				results = cursor.fetchall()
				msg = 'Input new password: '
				conn.send(bytes(msg, "utf8"))
				data2 = conn.recv(4096).decode("utf8")
				if results:
					for i in results:
						cursor.execute('''UPDATE user SET password = ? WHERE username = ?''', (data2, data))
						db.commit()
						break

				else:
					msg = "Invalid old password"
					conn.send(bytes(msg, "utf8"))
				print (cursor.fetchall())

			else:
				continue


	conn_list.remove(conn)
	conn.close()


while 1:
	conn, addr = s.accept()
	
	print ('Connected with ' + addr[0] + ':' + str(addr[1]))

	start_new_thread(clientthread, (conn,))


s.close()
