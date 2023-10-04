import socket
import threading
import os
import sys

# Función para limpiar la consola ( No sirve :( )
def clear_console():
    if os.name == 'posix':
        # En sistemas POSIX (Linux, macOS)
        os.system('clear')
    elif os.name == 'nt':
        # En sistemas Windows
        os.system('cls')

# Abre un socket para enviar datos
def socket_client(other_host, other_port):
    print(f"Connecting to host {other_host}\n")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((other_host, other_port))
    clear_console()
    print("Ingresa el mensaje que deseas enviar (o 'exit' para salir), envía 'archivo' si deseas enviar un archivo\n")
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

# Abre un socket para recibir datos
def socket_server(host, port):
    while True:
        print(f"Server running on port {port}\n")
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(1000)
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}\n")
        clear_console()
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
                            client_socket.settimeout(10)
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

def login(server_host, server_port):
    try:
        username = input("Ingresa tu username: ")
        password = input("Ingresa tu contraseña: ")
        login_data = username + ' ' + password
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


# Inicia el programa
def startup():
    auth_check = login("127.0.0.1", 5002)
    if auth_check != "Valid":
        print("Autorizado!")
    my_host = input("Ingresa tu dirección: ") # Dirección para recibir datos
    my_port = int(input("Ingresa tu puerto: ")) # Puerto para recibir datos
    hilo_server = threading.Thread(target=socket_server, args=(my_host, my_port)) # Hilo para recibir información
    hilo_server.start() # Inicio del hilo
    other_host = input("Ingresa la dirección del server: ") # Dirección al que enviar datos
    other_port = int(input("Ingresa el puerto del server: ")) # Puerto al que enviar datos
    clear_console() # Limpiar consola
    hilo_cliente = threading.Thread(target=socket_client, args=(other_host, other_port)) # Hilo para enviar datos
    hilo_cliente.start() # Inicio de hilo

    # Espera a que los hilos se completen antes de salir del programa
    hilo_server.join()
    hilo_cliente.join()



startup()
