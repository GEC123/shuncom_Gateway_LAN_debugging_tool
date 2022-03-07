import socket

myname = socket.getfqdn(socket.gethostname())
ip = socket.gethostbyname(myname)
print(ip)