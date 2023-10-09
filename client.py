import tkinter as tk
from tkinter import messagebox
import socket
import threading
import pickle

MY_HOST = ""
MY_PORT = 0
SERVER_HOST = ""
SERVER_PORT = 0
USERS = None
MY_USERNAME = None
OTHER_HOST = ""
OTHER_PORT = 0
chat_socket = None
CHAT_WINDOW = None
OTHER_USER = None
CHAT_TEXT = None

def socket_client(other_host, other_port):
    print(f"Connecting to host {other_host}\n")
    global chat_socket
    chat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(other_host, other_port)
    chat_socket.connect((other_host, other_port))
    # print("Ingresa el mensaje que deseas enviar (o 'exit' para salir), envía 'archivo' si deseas enviar un archivo\n")
    # while True:
    #     message = send_message(entry)
    #     if message == "archivo":
    #         client_socket.send(b'Enviando un archivo...')
    #         path = input("Ingresa el path del archivo: ")
    #         filename = path.split('\\')[-1]
    #         client_socket.send(filename.encode())
    #         with open(path, 'rb') as file:
    #             file_data = file.read(1024)
    #             while file_data:
    #                 client_socket.send(file_data)
    #                 file_data = file.read(1024)
    #             # Envia el marcador de final de archivo
    #             client_socket.send(b'EOF')
    #         print(f"Archivo enviado: {filename}")
    #     elif message.lower() == 'exit':
    #         client_socket.close()
    #     else:
    #         message = message + "\n"
    #         client_socket.send(message.encode())

def send_message(message):
    global chat_socket
    chat_socket.send(message.encode())
    CHAT_TEXT.insert(tk.END, MY_USERNAME + ': ' + message + '\n')



def socket_server(host, port):
    print(f"Server running on port {port}\n")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1000)
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}\n")
    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break
        if data == "Enviando un archivo...":
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
            CHAT_TEXT.insert(tk.END, OTHER_USER + ': ' + data + '\n')


# Function to handle login button click
def login_server(entry_username, entry_password, entry_server_host, entry_server_port):
    global SERVER_HOST
    global SERVER_PORT
    global MY_USERNAME
    username = entry_username.get()
    MY_USERNAME = username
    password = entry_password.get()
    server_host = entry_server_host.get()
    SERVER_HOST = server_host
    server_port = int(entry_server_port.get())
    SERVER_PORT = server_port
    login_data = username + ' ' + password + ' ' + str(MY_PORT)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))
    client_socket.send(login_data.encode())
    client_socket.settimeout(4)
    data = client_socket.recv(1024)
    if data.decode() == "Autorizao":
        messagebox.showinfo("Login Successful", "Welcome, " + username + "!")
        open_main_window()
        root.withdraw()  # Hide the login window after successful login
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")


# Function to open the main application window
def open_main_window():
    main_window = tk.Toplevel(root)
    main_window.title("Main Application")

    # Add widgets to the main window
    label_main = tk.Label(main_window, text="Welcome to the main application!")
    label_main.pack()
    load_button = tk.Button(main_window, text="Load Users...", command=lambda: load_users(main_window))
    load_button.pack()


def load_users(window):
    global USERS
    for child in window.winfo_children():
        child.destroy()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(SERVER_HOST)
    print(SERVER_PORT)
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    client_socket.send(b"Users")
    data_users = client_socket.recv(1024)
    USERS = pickle.loads(data_users)
    for user in USERS:
        if user[0] == MY_USERNAME:
            continue
        user_name = tk.Label(window, text=user[0])
        user_name.pack()
        user_addr = tk.Label(window, text=user[2])
        user_addr.pack()
        user_port = tk.Label(window, text=user[3])
        user_port.pack()
        user_button = tk.Button(window, text="Connect to user", command=lambda u=user: open_chat_window(u, window))
        user_button.pack()
    load_button = tk.Button(window, text="Load Users...", command=lambda: load_users(window))
    load_button.pack()


def open_chat_window(user, window):
    global OTHER_HOST
    global OTHER_PORT
    global CHAT_WINDOW
    global OTHER_USER
    global CHAT_TEXT
    OTHER_HOST = user[2]
    OTHER_PORT = int(user[3])
    OTHER_USER = user[0]
    CHAT_WINDOW = tk.Toplevel(window)
    CHAT_WINDOW.title(f"Chat with {OTHER_USER}")
    user_label = tk.Label(master=CHAT_WINDOW, text=user[0])
    user_label.pack()
    message_entry = tk.Entry(master=CHAT_WINDOW)
    message_entry.pack()
    message_button = tk.Button(master=CHAT_WINDOW, text="Send message", command=lambda: send_message(message_entry.get()))
    message_button.pack()
    CHAT_TEXT = tk.Text(master=CHAT_WINDOW)
    CHAT_TEXT.pack()
    hilo_cliente = threading.Thread(target=socket_client, args=(OTHER_HOST, OTHER_PORT))  # Hilo para enviar datos
    hilo_cliente.start()



def open_login_window():
    # Create and pack the username label and entry field
    label_username = tk.Label(root, text="Username:")
    label_username.pack()
    entry_username = tk.Entry(root)
    entry_username.pack()

    # Create and pack the password label and entry field
    label_password = tk.Label(root, text="Password:")
    label_password.pack()
    entry_password = tk.Entry(root, show="*")  # Show '*' for password input
    entry_password.pack()

    # Create and pack the server host label and entry field
    label_server_host = tk.Label(root, text="Server host:")
    label_server_host.pack()
    entry_server_host = tk.Entry(root)
    entry_server_host.pack()

    # Create and pack the server port label and entry field
    label_server_port = tk.Label(root, text="Server port:")
    label_server_port.pack()
    entry_server_port = tk.Entry(root)
    entry_server_port.pack()

    # Create and pack the login button
    login_button = tk.Button(root, text="Login",
                             command=lambda: login_server(entry_username, entry_password, entry_server_host,
                                                          entry_server_port))
    login_button.pack()


def save_data():
    global MY_HOST
    global MY_PORT
    MY_HOST = entry_my_host.get()
    MY_PORT = int(entry_my_port.get())
    hilo_server = threading.Thread(target=socket_server, args=(MY_HOST, MY_PORT))  # Hilo para recibir información
    hilo_server.start()
    label_my_host.destroy()
    label_my_port.destroy()
    entry_my_port.destroy()
    entry_my_host.destroy()
    save_button.destroy()
    open_login_window()


# Create the main window
root = tk.Tk()
root.config(pady=10, padx=10)
root.title("Your Data")

label_my_host = tk.Label(root, text="My host:")
label_my_host.pack()
entry_my_host = tk.Entry(root)
entry_my_host.pack()
# Create and pack my port label and entry
label_my_port = tk.Label(root, text="My port:")
label_my_port.pack()
entry_my_port = tk.Entry(root)
entry_my_port.pack()
# Create and pack the save button
save_button = tk.Button(root, text="Save", command=save_data)
save_button.pack()

# Start the Tkinter main loop
root.mainloop()
