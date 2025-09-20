from customtkinter import*
from PIL import Image
from socket import*
import threading
client = socket(AF_INET,SOCK_STREAM)
client.connect(("127.0.0.1", 12345))





window = CTk()
window.geometry("400x500") 
window.title("ЧАТ")
window.configure(fg_color="#000000")
font = CTkFrame(window, height=800, width=600)
font.place(y=0,x=0)
font = Image.open("")
font_ready = CTkImage(light_image=font, size=(800, 600))
font = CTkLabel(window, image=font_ready, text="")
font.place(y=0,x=0)

def on_enter(event):
    send_message()


def on_ctrl(event):
    increase_font()

cht = CTkFrame(window, height=300, width=300)
cht.pack_propagate(False)
cht.place(y=0,x=50)
chat_ready = CTkTextbox(cht, height=800, width=700,fg_color="#2F2F2F", text_color="#FF8C00")
chat_ready.configure(state="disabled")
chat_ready.place(y=0,x=0)

font_size = 12

def send_message():
    message = entry.get()
    client.send(message.encode()) 
    entry.delete(0, END)
    chat_ready.configure(state="normal")
    chat_ready.insert(END, message + "\n")
    chat_ready.configure(state="disabled")

def increase_font():
    global font_size
    font_size += 2
    chat_ready.configure(font=("Arial", font_size)) 

def decrease_font():
    global font_size
    if font_size > 8:
        font_size -= 2
        chat_ready.configure(font=("Arial", font_size))
polyhaem = []
def polyhenie():
    while True:
        for f in polyhaem:
            try:
                print(f.recv(1024).decode())
            except:
                pass
threading.Thread(target=polyhenie).start()


inputframe = CTkFrame(window, height=50, width=350,fg_color="#2F2F2F")
inputframe.place(y=310,x=0)




entry = CTkEntry(inputframe, placeholder_text="Введіть повідомлення...",  width=200,fg_color="#2F2F2F",text_color="#FF8C00", corner_radius=20)
entry.place(y=10,x=0)
entry.bind("<Return>", on_enter)


button = CTkButton(inputframe, text="Відповісти",  command=send_message )
button.place(y=10,x=205)

CTkButton(window, text="A+", width=40, command=increase_font).place(x=280, y=280)
CTkButton(window, text="A−", width=40, command=decrease_font).place(x=330, y=280)
window.mainloop()