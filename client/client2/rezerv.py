from customtkinter import *
from PIL import Image
import threading
from socket import *

# Підключення до сервера
client = socket(AF_INET, SOCK_STREAM)
client.connect(("127.0.0.1", 8080))

# Створення вікна
window = CTk()
window.geometry("400x500")
window.title("ЧАТ")
window.configure(fg_color="#000000")

# Фонова картинка
img = Image.open("image.jpeg")
background = CTkImage(light_image=img, size=(400, 500))
label = CTkLabel(window, image=background, text="")
label.place(y=0, x=0)

# Фрейм для чату
chat_frame = CTkFrame(window, height=300, width=350)
chat_frame.pack_propagate(False)
chat_frame.place(y=0, x=25)
chat_ready = CTkTextbox(chat_frame, height=290, width=340, fg_color="#2F2F2F", text_color="#FF8C00")
chat_ready.configure(state="disabled")
chat_ready.place(y=5, x=5)

font_size = 12

# Функція відправки повідомлення
def send_message():
    message = entry.get()
    if message:
        client.send(message.encode())
        chat_ready.configure(state="normal")
        chat_ready.insert(END, f"Ви: {message}\n")
        chat_ready.configure(state="disabled")
        entry.delete(0, END)

# Функція збільшення шрифту
def increase_font():
    global font_size
    font_size += 2
    chat_ready.configure(font=("Arial", font_size))

# Функція зменшення шрифту
def decrease_font():
    global font_size
    if font_size > 8:
        font_size -= 2
        chat_ready.configure(font=("Arial", font_size))

# Функція отримання повідомлень
def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode()
            chat_ready.configure(state="normal")
            chat_ready.insert(END, message + "\n")  # Відображаємо всі повідомлення
            chat_ready.configure(state="disabled")
        except:
            pass

# Запускаємо потік для отримання повідомлень
threading.Thread(target=receive_messages).start()

# Фрейм для введення
input_frame = CTkFrame(window, height=50, width=350, fg_color="#2F2F2F")
input_frame.place(y=310, x=0)

# Поле введення
entry = CTkEntry(input_frame, placeholder_text="Введіть повідомлення...", width=200, fg_color="#2F2F2F", text_color="#FF8C00", corner_radius=20)
entry.place(y=10, x=0)
entry.bind("<Return>", lambda event: send_message())

# Кнопка відправки
button = CTkButton(input_frame, text="Відповісти", command=send_message)
button.place(y=10, x=205)

# Кнопки зміни шрифту
CTkButton(window, text="A+", width=40, command=increase_font).place(x=280, y=280)
CTkButton(window, text="A−", width=40, command=decrease_font).place(x=330, y=280)

window.mainloop()