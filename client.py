import socket

OTHER_HOST = '127.0.0.1'
MY_HOST = '127.0.0.1'
OTHER_PORT = int(input("Whats the other port?"))  # Port of the remote server
MY_PORT = int(input("Whats my port?"))  # Port for your server
def peer_server():
    peer_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Socket server de mi peer
    peer_server_socket.bind((MY_HOST, MY_PORT))  # Mi socket server establece su dirección y puerto
    peer_server_socket.listen(1)  # Mi socket server escucha una conexión
    server_connection, server_address = peer_server_socket.accept()
    data = server_connection.recv(1024)
    print(f"Recieved ->: \n {data.decode()}")
    peer_server_socket.close()
    peer_client()

# Create the client socket and connect to the server
def peer_client():
    peer_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Socket cliente de mi peer
    peer_client_socket.connect((OTHER_HOST, OTHER_PORT))  # Conexión de mi peer cliente al server del otro peer
    message = input("Send a message: \n")
    peer_client_socket.send(message.encode())
    peer_client_socket.close()
    peer_server()

def ask_user():
    user_input = input("1 to be server first\n2 to be client first")
    if user_input == "1":
        peer_server()
    if user_input == "2":
        peer_client()
    else:
        ask_user()




# Create and bind the server socket


ask_user()
