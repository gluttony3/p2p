from socket import *
import threading
from customtkinter import *
import json
from PIL import Image

# Подключение к серверу
client = socket(AF_INET, SOCK_STREAM)
client.connect(("localhost", 12345))

nickname = None
chat_ready = None 
entry = None
json_file = "file.json"
font_size = 12
data = {"nickname": "", "messages": []} # создається переменная data

# Функция для сохранения информации в файл json
def save_data():
    with open(json_file, "w", encoding="utf-8") as f: # записуем інформацію з data у файл json
        json.dump(data, f, ensure_ascii=False, indent=2)

# Пробуем загрузить старый json файл
try:
    with open("file.json", "r", encoding="utf-8") as f: # завантажуємо вміст json файлу в data
        data = json.load(f)
except:
    pass

# --- Вікно ---
window = CTk()
window.geometry("400x500")
window.title("ЧАТ")

# --- Заставка для ника ---
start_frame = CTkFrame(window, width=400, height=500, fg_color="#1F1F1F")  # створюємо об'єкт для заставки введення псевдоніма
start_frame.place(x=0, y=0)

label = CTkLabel(start_frame, text="Введите ник", text_color="#FFFFFF", font=("Arial", 20)) # создаем метку где просим пользователя ввести псевдоним
label.place(relx=0.5, rely=0.3, anchor="center") # создаем метку в центре фрейма по горизонтали и вертикали

nick_frame = CTkFrame(start_frame, width=320, height=60, fg_color="#2E2E2E", corner_radius=15) # заставка для введення псевдоніму
nick_frame.place(relx=0.5, rely=0.5, anchor="center") #  создаем фрейм в центре фрейма по горизонтали и вертикали

# Поле для введення псевдоніма
nick_entry = CTkEntry(
    nick_frame,
    width=250,
    fg_color="#2E2E2E",
    text_color="#FFFFFF",
    placeholder_text="Введите ник...",
    placeholder_text_color="#AAAAAA",
    corner_radius=10
)
nick_entry.place(relx=0.5, rely=0.5, anchor="center")

# --- Функция создания чата ---
def show_chat():
    global chat_ready, entry

    # Фон (если есть картинка)
    try:
        img = Image.open("font/wallaper.jpg") # відкриваємо картинку для фону
        background = CTkImage(light_image=img, size=(400, 500)) # робимо її CTk картинкою
        label = CTkLabel(window, image=background, text="") # вставляємо картинку як фон
        label.place(y=0, x=0)
    except:
        pass

    # Чатовое окно
    chat_frame = CTkFrame(window, height=300, width=350) # создаём фрейм для сообщений
    chat_frame.pack_propagate(False) # автоматично не змінює розмір фрейму під вкладені віджети
    chat_frame.place(y=5, x=25)

    chat_ready = CTkTextbox(chat_frame, height=290, width=340, # віджет для майбутнього відображення тексту
                            fg_color="#2F2F2F", text_color="#FF8C00")
    chat_ready.configure(state="disabled") # забороняємо редагування вручну
    chat_ready.place(y=5, x=5)

    # Поле ввода
    input_frame = CTkFrame(window, height=50, width=350, fg_color="#2F2F2F") # фрейм для поля введення
    input_frame.place(y=320, x=0)

    entry = CTkEntry(input_frame, placeholder_text="Введіть повідомлення...", # поле введення
                     width=200, fg_color="#2F2F2F", text_color="#FF8C00", corner_radius=20)
    entry.place(y=10, x=0)
    entry.bind("<Return>", lambda event: send_message()) # Enter = отправка

    # Кнопка отправки
    button = CTkButton(input_frame, text="Відповісти", text_color="#D3D7CF", 
                       fg_color="#3C3B37", hover_color="#4F4E49", command=send_message) # кнопка для отправки
    button.place(y=10, x=205)

    # Кнопки изменения шрифта
    CTkButton(window, text="A+", width=40, text_color="#D3D7CF", fg_color="#4A4843",
              hover_color="#4A4843", command=increase_font).place(x=280, y=280) # увеличить шрифт
    CTkButton(window, text="A−", width=40, text_color="#D3D7CF", fg_color="#4A4843",
              hover_color="#4A4843", command=decrease_font).place(x=330, y=280) # уменьшить шрифт

    # запускаем получение сообщений в отдельном потоке
    threading.Thread(target=receive_messages, daemon=True).start()

# --- Установка ника ---
def set_nickname(event=None):
    global nickname

    nickname = nick_entry.get() # отримання никнейму из поля ввода

    if nickname != "": # исключает пустую строку
        client.send(nickname.encode()) # отправляем серверу ник
        start_frame.destroy() # прибираємо заставку
        show_chat() # запускаем чат

# Привязываем Enter к функции set_nickname
nick_entry.bind("<Return>", set_nickname)

# --- Отправка сообщений ---
def send_message():
    message = entry.get() # получаем текст из поля
    if message != "": # исключает пустую строку
        client.send(message.encode()) # отправляет сообщение на сервер
        chat_ready.configure(state="normal") # делаем чат редактируемым
        chat_ready.insert("end", nickname + ": " + message + "\n") # вставляем текст в чат
        chat_ready.configure(state="disabled") # снова запрещаем редактирование
        entry.delete(0, "end") # очищаем поле ввода

# --- Изменение шрифта ---
def increase_font():
    global font_size
    font_size += 2 # увеличиваем размер шрифта
    chat_ready.configure(font=("Arial", font_size))

def decrease_font():
    global font_size
    if font_size > 8: # ограничиваем минимальный размер
        font_size -= 2
        chat_ready.configure(font=("Arial", font_size))

# --- Получение сообщений ---
def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode() # принимаем данные от сервера
            chat_ready.configure(state="normal")
            chat_ready.insert("end", message + "\n") # выводим в чат
            chat_ready.configure(state="disabled")
        except:
            break # если ошибка → прерываем цикл

# --- Сохранение и выход ---
def save_and_close():
    if nickname and chat_ready:
        data["nickname"] = nickname # сохраняем ник
        chat_ready.configure(state="normal")
        data["messages"] = chat_ready.get("1.0", "end").split("\n") # сохраняем весь текст чата
        chat_ready.configure(state="disabled")
        save_data() # записываем в json
    window.destroy() # закрываем окно

window.protocol("WM_DELETE_WINDOW", save_and_close) # перехватываем закрытие окна
window.mainloop() # запускаем главный цикл
