# Echo client program
import socket
import sys
import json

HOST = 'localhost'    # The remote host
PORT = 50007              # The same port as used by the server
val = ['boy', 'girl', 'mother', 'father']
s = None
for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        s = None
        continue
    try:
        s.connect(sa)
    except socket.error as msg:
        s.close()
        s = None
        continue
    break
if s is None:
    print 'could not open socket'
    sys.exit(1)
count = 0
while count < 20:
    count += 1
    s.sendall(json.dumps(val))
    data = s.recv(1024)
    if data is None: continue
    print 'Received', repr(json.loads(data))
s.close()
#print 'Received', repr(data)