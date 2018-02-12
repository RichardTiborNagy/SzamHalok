import socket

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address=('localhost', 10001)

server.bind(server_address)
server.settimeout(1.0)

while True:
	try:
		# print "waiting..."
		data, client_address = server.recvfrom(4096)
		
		print "received %i byte from %s : %s" % (len(data),client_address,data)
		
		if data:
			print "%i data received" % (data)
	except:
		pass

server.close()