import socket
import threading
import sys
class Peer:
    def __init__(self, my_host, my_port):
        self.my_host = my_host
        self.my_port = my_port

    def login(self, username, password, server_host, server_port):
        try:
            # Datos para inicio de sesión
            # username = input("Ingresa tu username: ")
            # password = input("Ingresa tu contraseña: ")
            # server_host = input("Ingresa la dirreción del server")
            # server_port = input("Ingresa el puerto del server")
            login_data = username + ' ' + password
            # Conexión a servidor
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((server_host, server_port))
            client_socket.send(login_data.encode())
            client_socket.settimeout(4)
            print("Checking auth...")
            data = client_socket.recv(1024)
            if data == "Autorizado":
                print("Logged in!")
                return "Valid"
            elif data == "No autorizado":
                print("Credentials invalid")
                return
        except:
            print("No autorizado...")
            sys.exit()

    def start_connection(self, other_host, other_port):
        # Conectando al server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((other_host, other_port))
        while True:
            message = input("")
            if message == "archivo":
                client_socket.send(b'Enviando un archivo...')
                path = input("Ingresa el path del archivo: ")
                filename = path.split('\\')[-1]
                client_socket.send(filename.encode())
                with open(path, 'rb') as file:
                    file_data = file.read(1024)
                    while file_data:
                        client_socket.send(file_data)
                        file_data = file.read(1024)
                    # Envia el marcador de final de archivo
                    client_socket.send(b'EOF')
                print(f"Archivo enviado: {filename}")
            elif message.lower() == 'exit':
                client_socket.close()
            else:
                message = message + "\n"
                client_socket.send(message.encode())
    def start_listening(self):
        print(f"Server running on port {self.my_port}\n")
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.my_host, self.my_port))
        server_socket.listen(1000)
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}\n")
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            if data.decode() == "Enviando un archivo...":
                print("Archivo FUNC")
                filename = client_socket.recv(1024).decode()
                with open(filename, 'wb') as file:

                    while True:
                        try:
                            client_socket.settimeout(5)
                            file_data = client_socket.recv(1024)
                            file.write(file_data)
                        except:
                            client_socket.settimeout(10000)
                            break
                print(f"Archivo recibido: {filename}")
            else:
                print(f"{client_address[0]}: {data.decode()}")

        print("Connection closed.")
        client_socket.close()