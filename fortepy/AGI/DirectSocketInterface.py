import ssl
import socket
import six

class DirectSocketInterface(object):
	AGI_PASSWORD = None
	MERCHANT_ID = None

	def __init__(self, hostname='www.paymentsgateway.net', port=6050):
		self.hostname = hostname
		self.port = port
	
	def connect(self):
		self.socket = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
		return self.socket.connect((self.hostname, self.port))
		
	def write_header(self):
		self.write("pg_merchant_id", DirectSocketInterface.MERCHANT_ID)
		self.write("pg_password", DirectSocketInterface.AGI_PASSWORD)

	def write(self, key, value):
		if value is None:
			return False
		data = "%s=%s\n" % (key, str(value))
		return self.socket.sendall(six.b(data))

	def send(self):
		return self.socket.sendall(b"endofdata\n\n")

	def read(self):
		data = ""
		while data.rfind("endofdata") == -1:
			chunk = self.socket.recv(4096)
			if not six.PY3:
				data = data + str(chunk)
			else:
				data = data + str(chunk, 'UTF-8')
		dict = {}
		for line in data.split("\n"):
			if line.find('=') != -1:
				data = line.split('=')
				dict[data[0]] = data[1]
		return dict
		
	def close(self):
		return self.socket.close()

	def __enter__(self):
		self.connect() # this is fucking retarded.
		return self
		
	def __exit__(self, exception_type, exception_value, traceback):
		self.close()
		return exception_type == None
