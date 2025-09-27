from customtkinter import *
from socket import *
import threading
import json
from PIL import Image

json_file = "file.json"
font_size = 16

def load_data():
    with open(json_file, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data():
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

data = load_data()

client = socket(AF_INET, SOCK_STREAM)
client.connect(("localhost", 8080))
client.setblocking(False)

def update_chat(message):
    global chat_box
    chat_box.configure(state="normal")
    chat_box.insert(END, message + "\n")
    chat_box.configure(state="disabled")

def receive_messages():
    global window
    while True:
        try:
            message = client.recv(1024).decode()
            if message:
                data["messages"].append(message)
                window.after(0, lambda: update_chat(message))
        except:
            pass  

def send_message(event=None):
    global entry, chat_box
    message = entry.get()
    if message:
        client.send(message.encode())
        data["messages"].append(f"Ви: {message}")
        update_chat(f"Ви: {message}")
        entry.delete(0, END)

def increase_font():
    global font_size, chat_box
    font_size += 2
    chat_box.configure(font=("Arial", font_size))

def decrease_font():
    global font_size, chat_box
    if font_size > 8:
        font_size -= 2
        chat_box.configure(font=("Arial", font_size))

def create_chat_window():
    global window, entry, chat_box

    window = CTk()
    window.geometry("400x500")
    window.title("ЧАТ")

    background = CTkImage(Image.open("image.jpeg"), size=(400, 500))
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

create_chat_window()
