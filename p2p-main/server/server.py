import socket
import threading
import json


# Файл для сохранения сообщений
json_file = "file.json"

# Загружаем данние
try:
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
except:
    data = {"messages": []} # створює змінну data з ключем messages и пустим словник за для уникнення помилок

# Функция для сохранения сообщений
def save_data():
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Создаем серверный сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 12345))  # локальный хост и порт
server_socket.listen(5)  # максимум 5 подключений

# Список и словник для хранения клиентов и их ников
clients = []
nicknames = {}

# Функция для обработки одного клиента
def handle_client(client):
    try:
        # Получаем ник клиента
        nickname = client.recv(1024).decode() # отримуємо данні від клієнта
        nicknames[client] = nickname # додає к ключу client значение которое введет пользователь в словник
        clients.append(client) # додає client в кінець списку
        print(nickname + " подключился") # введений пользователем никнейм + подключился

        while True:
            try:
                # Получаем сообщение от клиента
                message = client.recv(1024).decode() # получаем введенное пользователем сообщение
                if not message: # если клиент отключился виходим из цикла
                    break
                full_message = nickname + ": " + message # додаємо до повідомлення 
                data["messages"].append(full_message) # додаємо нове повідомлення к переменной data
                save_data() # викликає функцію save data

                # Отправляем сообщение всем клиентам кроме отправителя
                for c in clients:
                    if c != client: # исключаем отправителя сообщения
                        c.send(full_message.encode()) # отсилает рядок клиенту байтами

            except:
                # Если клиент отключился
                break

    finally: 
        # Убираем клиента из списков и закрываем соединение
        if client in clients: # перевіряємо чи є клієнт у списку clients
            clients.remove(client) # якщо є - видаляємо
        if client in nicknames: # перевіряємо чи є клієнт у списку nicknames
            del nicknames[client] # якщо є - видаляємо
        client.close() # закриваємо з'єднання з клієнтом
        print("Клиент отключился") # для дійсності виводимо фразу в термінал

# Функция для приняття нових подключень
def accept_connections(): 
    while True:
        client, addr = server_socket.accept() # после принятия возвращает данние о клиенте
        print("Подключился новий клиент:", addr) # з'являється повідомлення + адреса клієнта в терміналі 
        threading.Thread(target=handle_client, args=(client,), daemon=True).start() # поток для обробки клиента

print("Сервер запущен")
accept_connections() # запуск функції для прийняття підключень
