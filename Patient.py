import time
import socket
import ssl
import random
import threading

class Patient:
    def __init__(self, port, certfile, keyfile, name):
        self.name = name
        self.port = port
        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.context.load_cert_chain(certfile=certfile, keyfile=keyfile)
        self.secret = random.randint(1, 100)
        self.secret_parts = [0, 0, 0]
        self.split_shares()
        self.initialize_secret()
        print(f"{self.name} secret: {self.secret}")
        print(f"{self.name} secret parts: {self.secret_parts}")
        self.shares_received_count = 0

    def start_server(self):
        self.server_socket = socket.socket()
        self.server_socket.bind(('localhost', self.port))
        self.server_socket.listen(5)
        
        print(f"[+] Server {self.name} started, waiting for connection on port {self.port}...")
        while True:
            new_socket, address = self.server_socket.accept()
            with self.context.wrap_socket(new_socket, server_side=True) as ssl_socket:
                data = ssl_socket.recv(1024)
                if data:
                    received_share = int(data.decode())
                    print(f"{self.name} received {received_share}")
                    self.received_secret_shares += received_share
                    self.shares_received_count += 1
                    print(f"{self.name} total received secret shares: {self.received_secret_shares}")

                    if self.shares_received == 2:
                        self.send_to_hospital()

    def send_message(self, host, port, share):
        with socket.create_connection((host, port)) as sock:
            with self.context.wrap_socket(sock, server_hostname='localhost') as ssock:
                ssock.send(str(share).encode())

    def split_shares(self):
        self.secret_parts[0] = random.randint(1, self.secret - 4)
        self.secret_parts[1] = random.randint(1, self.secret - self.secret_parts[0] - 1)
        self.secret_parts[2] = self.secret - (self.secret_parts[0] + self.secret_parts[1])

    
    def distribute_shares(self, host_bob, port_bob, host_charlie, port_charlie):
        #Send shares to peers
        if self.name == "Alice":
            self.send_message(host_bob, port_bob, self.secret_parts[1])
            self.send_message(host_charlie, port_charlie, self.secret_parts[2])
        elif self.name == "Bob":
            self.send_message(host_charlie, port_charlie, self.secret_parts[2])
            self.send_message('localhost', 5001, self.secret_parts[0])
        elif self.name == "Charlie":
            self.send_message('localhost', 5001, self.secret_parts[0])
            self.send_message('localhost', 5002, self.secret_parts[1])

    def send_to_hospital(self):
        #Send to hospital
        print(f"{self.name} sending total secret shares to Hospital: {self.received_secret_shares}")
        self.send_message('localhost', 5004, self.received_secret_shares)

    def run(self):
        server_thread = threading.Thread(target=self.start_server, daemon=True)
        server_thread.start()
        return server_thread
    
    def initialize_secret(self):
        #Initialize received_secret shares based on the kept part
        if self.name == "Alice":
            self.received_secret_shares = self.secret_parts[0]
        elif self.name == "Bob":
            self.received_secret_shares = self.secret_parts[1]
        elif self.name == "Charlie":
            self.received_secret_shares = self.secret_parts[2]