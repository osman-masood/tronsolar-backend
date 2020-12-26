import socket
import time

host = socket.gethostname()
port = 9999                   # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
print("Sending the data")
for index in range(10):
    s.sendall(b'Hello, world ')
    s.sendall(str.encode(str(index)))
    data = s.recv(1024)
    print('Received', repr(data))
    time.sleep(0.5)
s.close()
