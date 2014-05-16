import socket

def ipv6():
	return [(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)]][0][1]
