import threading
import json
from socket import *

json_file = "file.json"

def load_data():
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"messages": []}

# збереження історії в JSON
def save_data():
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(("localhost", 8080))
server_socket.listen(5)

clients = []
nicknames = {}
data = load_data()

def receive():
    while True:
        for client in clients[:]:
            try:
                message = client.recv(1024).decode()
                if client not in nicknames:
                    nicknames[client] = message  # перше повідомлення — нік
                else:
                    full_message = nicknames[client] + ": " + message
                    data["messages"].append(full_message)
                    save_data()
                    for other_client in clients:
                        if other_client != client:
                            other_client.send(full_message.encode())
            except:
                clients.remove(client)
                if client in nicknames:
                    del nicknames[client]
                client.close()

def accept_connections():
    while True:
        connection, address = server_socket.accept()
        clients.append(connection)

threading.Thread(target=receive).start()
threading.Thread(target=accept_connections).start()

print("Сервер запущений")
