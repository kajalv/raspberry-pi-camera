import cameraModule
import motionDetTop
import socket
import sys
import struct
from multiprocessing import Process

# Server must be running to enable the security system in remote Android control mode.
# Any commands received from the Android app will be logged to the console.

def recvall(sock, count) :

	buf = b''
	while count :
		newbuf = sock.recv(count)
		if not newbuf :
			return None
		buf += newbuf
		count -= len(newbuf)

	return buf

def serverStart() :

	host = socket.gethostbyname('127.0.0.1')
	port = 8008

	try :
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print "Socket created"
	except socket.error :
		print "Unable to create socket"
		sys.exit()

	try :
		sock.bind((host, port))
		print "Socket bounded to port 8008"
	except socket.error :
		print "Unable to bind to port 8008"
		sys.exit()

	sock.listen(5)

	while  True:

		(cliSock, addr) = sock.accept()

		length = int(recvall(cliSock, 2))
		#length, = struct.unpack('!I', lengthbuf)
		cmd = recvall(cliSock, length)

		print "Command from android: " + cmd

		cameraModule.do_command(cmd)

		cliSock.close()



if __name__ == "__main__" :

	serverStart()
