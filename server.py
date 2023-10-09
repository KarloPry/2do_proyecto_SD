import socket
import pickle
import time
USERS_CONECTED = []
def checkAuth(username, password):
    with open("login_credentials.txt", mode='r') as file:
        for line in file:
            stored_username, stored_password = line.strip().split()
            if username == stored_username and password == stored_password:
                return True
    return False

def getUsers():
    data = pickle.dumps(USERS_CONECTED)
    client_socket.send(data)

host = input("Ingresa tu host: ")
port = int(input("Ingresa tu port: "))
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(200)
print(f"Servidor escuchando en {host}:{port}")

while True:
    # Aceptar una conexión entrante
    client_socket, client_address = server_socket.accept()
    print(f"Conexión entrante desde {client_address}")

    # Recibir el nombre de usuario y la contraseña del cliente
    data_login = client_socket.recv(1024).decode()
    if data_login == "Users":
        getUsers()
    else:
        username = data_login.split(" ")[0]
        password = data_login.split(" ")[1]
        port = data_login.split(" ")[2]
        isAuth = checkAuth(username, password)
        print(isAuth)
        if isAuth:
            USERS_CONECTED.append((username, password, client_address[0], port))
            client_socket.send("Autorizao".encode())
        else:
            pass
