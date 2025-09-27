import threading
from socket import *

# Налаштування сервера
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(("127.0.0.1", 8081))
server_socket.listen(5)  # Дозволяє 5 клієнтів

clients = []  # Список підключених клієнтів

# Функція відправки повідомлень
def send_message():
    while True:
        message = input()  # Введення повідомлення на сервері
        for client in clients:
            client.send(message.encode())

# Функція прийому повідомлень
def receive():
    while True:
        for client in clients:
            try:
                message = client.recv(1024).decode()
                print(message)  # Виводимо повідомлення в консоль
            except:
                pass

# Функція прийому нових підключень
def accept_connections():
    while True:
        try:
            connection, address = server_socket.accept()
            print("Підключився клієнт", address)
            clients.append(connection)
        except:
            pass

# Запускаємо потоки
threading.Thread(target=send_message).start()
threading.Thread(target=receive).start()
threading.Thread(target=accept_connections).start()