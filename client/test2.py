from customtkinter import *
from socket import *
import threading
import json
from PIL import Image
json_file = "file.json" 

font_size = 16  # Початковий розмір шрифту

def load_data():
    with open(json_file, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data():
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


client = socket(AF_INET, SOCK_STREAM)
client.connect(("127.0.0.1", 8080))
client.setblocking(False)


def update_chat(message):
    chat_box.configure(state="normal") 
    chat_box.insert(END, message + "\n")
    chat_box.configure(state="disabled")

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode()
            if message:
                data["messages"].append(message)
                window.after(0, lambda: update_chat(message))
        except:
            pass

def send_message(event=None):
    message = entry.get()
    if message:
        client.send(message.encode())
        data["messages"].append(f"Ви: {message}")
        update_chat(f"Ви: {message}")
        entry.delete(0, END)


def increase_font():
    font_size += 2
    chat_box.configure(font=("Arial", font_size))

def decrease_font():
    if font_size > 8:
        font_size -= 2
        chat_box.configure(font=("Arial", font_size))


def create_chat_window():
    window = CTk()
    window.geometry("400x500")
    window.title("ЧАТ")
    background= CTkImage(Image.open("image.jpeg"), size=(400, 500))  
    background_label = CTkLabel(window, image=background, text="")  
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    window.configure(fg_color="#1A1A1A")

    chat_box = CTkTextbox(window, height=320, width=360,
                          fg_color="#2F2F2F", text_color="#FFD700", corner_radius=10,
                          font=("Arial", font_size))
    chat_box.place(y=10, x=20)
    chat_box.configure(state="disabled")

    for msg in data["messages"]:
        update_chat(msg)

    entry = CTkEntry(window, placeholder_text="Введіть повідомлення...",
                     width=220, fg_color="#3A3A3A", text_color="#FFFFFF", corner_radius=10)
    entry.place(y=360, x=20)
    entry.bind("<Return>", send_message)

    send_button = CTkButton(window, text="Надіслати", command=send_message,
                            fg_color="#DC3545", hover_color="#B02A37", corner_radius=10)
    send_button.place(y=360, x=260)

    CTkButton(window, text="A+", width=40, command=increase_font,
              fg_color="#DC3545", hover_color="#B02A37").place(x=260, y=320)

    CTkButton(window, text="A−", width=40, command=decrease_font,
              fg_color="#DC3545", hover_color="#B02A37").place(x=310, y=320)

    threading.Thread(target=receive_messages, daemon=True).start()

    def on_close():
        save_data()
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_close)
    window.mainloop()


def submit_nickname(event=None):
    nickname = nickname_entry.get().strip()
    if nickname:
        data["nickname"] = nickname
        client.send(nickname.encode())
        save_data()
        nickname_window.destroy()
        create_chat_window()
    else:
        label.configure(text="Введіть нікнейм!")


# --- СТАРТ ---
data = load_data()

if data["nickname"]:
    client.send(data["nickname"].encode())
    create_chat_window()
else:
    nickname_window = CTk()
    nickname_window.geometry("300x150")
    nickname_window.title("Вибір ніку")
    nickname_window.configure(fg_color="#1E1E1E")

    label = CTkLabel(nickname_window, text="Введіть ваш нікнейм:",
                     font=("Helvetica", 16, "bold"), text_color="#FFD700")
    label.place(x=70, y=20)

    nickname_entry = CTkEntry(nickname_window, width=220,
                              fg_color="#2F2F2F", text_color="#FFFFFF", corner_radius=15)
    nickname_entry.place(x=40, y=50)
    nickname_entry.bind("<Return>", submit_nickname)

    start_button = CTkButton(nickname_window, text="Почати", command=submit_nickname,
                             fg_color="#8A2BE2", hover_color="#6A1B9A", corner_radius=15)
    start_button.place(x=110, y=100)

    nickname_window.mainloop()
