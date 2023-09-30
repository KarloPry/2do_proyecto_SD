import socket
import time
other_host = '127.0.0.1'
my_host = '127.0.0.1'
other_port = 12345  # Port of the remote server
my_port = 5001  # Port for your server

# Create and bind the server socket
peer_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Socket server de mi peer
peer_server_socket.bind((my_host, my_port))  # Mi socket server establece su dirección y puerto
peer_server_socket.listen(1)  # Mi socket server escucha una conexión
print("Waiting...")
while True:
    print("...")
    time.sleep(2)
    server_connection, server_address = peer_server_socket.accept()
    if server_connection:
        break
print(server_address)
# Create the client socket and connect to the server
peer_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Socket cliente de mi peer
peer_client_socket.connect((other_host, other_port))  # Conexión de mi peer cliente al server del otro peer

# Now that both sockets are set up, you can send data from the client to the server

# You should also have code to accept the incoming connection on the server side if needed
# For example:
server_connection, server_address = peer_server_socket.accept()
data = server_connection.recv(1024)

peer_client_socket.send(b"HEY, stfu")
