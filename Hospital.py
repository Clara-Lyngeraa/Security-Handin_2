import socket
import ssl
import threading

class Hospital:
    def __init__(self, port, certfile, keyfile):
        self.port = port
        self.total_received_shares = 0
        self.received_from_peers = 0
        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.context.load_cert_chain(certfile=certfile, keyfile=keyfile)

    def start_server(self):
        server_socket = socket.socket()
        server_socket.bind(('localhost', self.port))
        server_socket.listen(5)

        print(f"[+] Hospital started, waiting for connection at port:{self.port}")

        while self.received_from_peers < 3:
            connection, address = server_socket.accept()
            with self.context.wrap_socket(connection, server_side=True) as client_socket:
                data = client_socket.recv(1024)
                if data:
                    received_share = int(data.decode())
                    self.total_received_shares += received_share
                    self.received_from_peers += 1
                    print(f"Hospital received share: {data}\n")
        print(f"Hospital received all shares: {self.total_received_shares}")
        server_socket.close()
    
    def run(self):
        server_thead = threading.Thread(target=self.start_server, daemon=True)
        server_thead.start()
        return server_thead

    