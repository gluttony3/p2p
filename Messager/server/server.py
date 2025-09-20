# Імпортуємо сокет
import threading
from socket import*
# використовуємо сімейство ipv4 та протокол tcp 
server_socket = socket(AF_INET, SOCK_STREAM)
# звязуємо порти з хостомcalhost", 12345))
# Робимо сокет неблокуючим щоб пр
server_socket.bind(("127.0.0.1", 12345))
# Робимо сокет неблокуючим щоб програма не зависала на операціях очікування підключень
server_socket.setblocking(False)
# даємо можливість підключитися 5 клієнтам
server_socket.listen(5)
# сюди ми зберігаємо клієнтів які вже підключилися
clients = []
#Функція яка відправляє повідомлення всім користувачам на сервері
def snd_mwssage():
        while True: #цикл
            global clients
            give_message = input() #відправляємо повідомлення на сервер
            for i in clients:
                i.send(give_message.encode()) #отправляєм в байтах
threading.Thread(target=snd_mwssage).start() #поток

def priem():
    global clients
    while True:
            for f in clients:
                try:
                    print(f.recv(1024).decode()) #получаєм(преобразовиваєм в текст)
                except:
                    pass
threading.Thread(target=priem).start()
#приймає нові підключення
while 1:
        try:
               connection, address = server_socket.accept() #чекаємо нових клієнтів
               print("Підключився клієнт", address) 
               connection.setblocking(False) #сокет не блокувався
               clients.append(connection) #додаємо до списку clients
        except:
                pass