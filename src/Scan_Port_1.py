import socket, sys

'''
Scan_Port_1.py @IP Port1 Port2
'''


if len(sys.argv) != 4:
	print("Mauvais usage")
	exit()

startPort = 0
endPort = 0

try:
	startPort = int(sys.argv[2])
	endPort = int(sys.argv[3])
except:
	print("There is error in Port Number !")
	exit()


while startPort <= endPort:
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((sys.argv[1], startPort))
		print("Port {} is opened !".format(startPort))
		startPort += 1
		sock.close()
	except:
		#print("Port {} is closed !".format(startPort))
		startPort += 1
