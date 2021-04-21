import socket
import re, uuid

print(socket.gethostname())
print(socket.gethostbyname(socket.gethostname()))
print(':'.join(re.findall('..', '%012x' % uuid.getnode())))

hostName = "www.htw-berlin.de"

fqdn = socket.getfqdn(hostName)
#socket.get

print("Fully qualified domain name of %s is:", hostName)

ipAddress = socket.gethostbyname_ex(hostName)
print(fqdn)
print(ipAddress)