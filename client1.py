import socket
from threading import Thread
import sys
import getpass
import tkinter

pflag = 0


def receive():
	while True:
		try:
			msg = s.recv(4096).decode("utf8")
			"""
			if msg[-1] == '1':
				print(msg[:-1])
				pflag = 1

			else:
				print(msg)
			"""
			msg_list.insert(tkinter.END, msg)

		except OSError:# Possibly client has left the chat.
			break


def send(event = None):
	if pflag == 1:
		msg = getpass.getpass(' ')
	else:
		msg = my_msg.get()

	my_msg.set("")  # Clears input field.
	try:
		s.sendall(bytes(msg, "utf8"))
	except socket.error:
		print('Send failed')
		sys.exit()


def on_closing(event=None):
	my_msg.set("{quit}")
	send()


top = tkinter.Tk()
top.title("Chatter")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)


try:

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

except socket.error as msg:
	print('Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message: ' + msg[1])
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

s.connect((remote_ip, port))

print ('Socket Connected to ' + host + ' on ip ' + remote_ip)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()

