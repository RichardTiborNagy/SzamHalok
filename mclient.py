import socket
import struct

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10000)

client.connect(server_address)

values = (20000000,'+',3)
packer = struct.Struct('i c i')
unpacker = struct.Struct('i')
packed_data = packer.pack(*values)

raw_input("Connected to server, press something to continue...")

try:
    client.sendall(packed_data)
    print "Data sent to server:", values
    answer = unpacker.unpack(client.recv(unpacker.size))
    print 'Received answer:', answer[0]
finally:
    client.close()
