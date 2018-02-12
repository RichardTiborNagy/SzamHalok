import socket
import struct
import select

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address=('localhost', 10000)
udp_server_address=('localhost', 10001)
server.bind(server_address)
server.listen(50)
# server.settimeout(1.0)
server.setblocking(0)

unpacker = struct.Struct('i c i')
packer = struct.Struct('i')

def calculate(first, operation, second):
    if operation == '+':
        return first + second
    elif operation == '-':
        return first - second
    elif operation == '*':
        return first * second
    elif operation == '/':
        return first / second

inputs = [server]

while True:
    timeout = 1
    readable, writeable, exceptional = select.select(inputs, [], [], timeout)

    if not (readable or writeable or exceptional):
		continue
    for s in readable:
        if s is server:
            try:
                client, address = server.accept()
                inputs.append(client)
            except:
                pass
        else:
            try:
                data = s.recv(unpacker.size)
                unpacked_data = unpacker.unpack(data)
                print 'Received data from client:', unpacked_data
                answer = calculate(unpacked_data[0], unpacked_data[1], unpacked_data[2])
                print 'Answer:', answer
                s.sendall(packer.pack(answer))
                print 'Answer sent to client.'
                print 'Sending answer to udp server.'
                udpclient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                try:
                    sent = udpclient.sendto(str(answer),udp_server_address)
                    print "%s bytes sent to udp server." % (sent)
                finally:
                    udpclient.close()
            finally:
                inputs.remove(s)
                s.close()
    # try:
    #     client, address = server.accept()
    #     try:
    #         data = client.recv(unpacker.size)
    #         unpacked_data = unpacker.unpack(data)
    #         print 'Received data:', unpacked_data
    #         answer = calculate(unpacked_data[0], unpacked_data[1], unpacked_data[2])
    #         print 'Answer:', answer
    #         client.sendall(packer.pack(answer))
    #         print 'Answer sent.'
    #     finally:
    #         client.close()
    # except:
    #     pass
server.close()
