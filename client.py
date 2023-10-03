import socket
import threading
import os

# Función para limpiar la consola (No sirve :( )
def clear_console():
    if os.name == 'posix':
        # En sistemas POSIX (Linux, macOS)
        os.system('clear')
    elif os.name == 'nt':
        # En sistemas Windows
        os.system('cls')

# Proceso del servidor
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
                        file_data = client_socket.recv(1024)
                        print(file_data)
                        if not file_data:
                            print("Done!")
                            break
                        file.write(file_data)
                print(f"Archivo recibido: {filename}")
            else:
                print(f"{client_address[0]}: {data.decode()}")

        print("Connection closed.")
        client_socket.close()

# Proceso del cliente
def socket_client(other_host, other_port):
    print(f"Connecting to host {other_host}\n")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((other_host, other_port))
    clear_console()
    print("Ingresa el mensaje que deseas enviar (o 'exit' para salir), envia 'archivo' si deseas enviar un archivo\n")
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
                client_socket.shutdown(socket.SHUT_WR)
            print(f"Archivo enviado: {filename}")
        elif message.lower() == 'exit':
            client_socket.close()
        else:
            message = message + "\n"
            client_socket.send(message.encode())


def startup():
    my_host = input("Ingresa tu dirección: ")
    my_port = int(input("Ingresa tu puerto: "))
    hilo_server = threading.Thread(target=socket_server, args=(my_host, my_port))
    hilo_server.start()
    other_host = input("Ingresa la dirección del server: ")
    other_port = int(input("Ingresa el puerto del server: "))
    clear_console()
    hilo_cliente = threading.Thread(target=socket_client, args=(other_host, other_port))
    hilo_cliente.start()

    # Espera a que los hilos se completen antes de salir del programa
    hilo_server.join()
    hilo_cliente.join()

startup()
