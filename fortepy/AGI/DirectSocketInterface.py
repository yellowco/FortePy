import ssl
import socket

class DirectSocketInterface(object):
    AGI_PASSWORD = None
    MERCHANT_ID = None

    def __init__(self, hostname='www.paymentsgateway.net', port=6050):
        self.socket = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        self.socket.connect((hostname, port))
        
    def write_header(self):
        self.socket.write("pg_merchant_id", DirectSocketInterface.MERCHANT_ID)
        self.socket.write("pg_password", DirectSocketInterface.AGI_PASSWORD)

    def write(self, key, value):
        if value is None:
            return False
        data = "%s=%s\n" % (key, str(value))
        return self.socket.sendall(bytes(data, 'UTF-8'))

    def send(self):
        return self.socket.sendall(b"endofdata\n\n")

    def read(self):
        data = ""
        while data.rfind("endofdata") == -1:
            chunk = self.socket.recv(4096)
            data = data + str(chunk, 'UTF-8')
        dict = {}
        for line in data.split("\n"):
            if line.find('=') != -1:
                data = line.split('=')
                dict[data[0]] = data[1]
        return dict

    def close(self):
        return self.socket.close()