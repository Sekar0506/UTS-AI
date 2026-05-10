import tkinter as tk
from tkinter import scrolledtext
import json
import random
import pyttsx3
import speech_recognition as sr
from PIL import Image, ImageTk
import threading

# ================== LOAD DATA ==================
with open('faq.json') as file:
    data = json.load(file)

responses = {
    "sapaan": [
        "Halo juga!",
        "Hai! Senang bertemu denganmu"
    ],

    "nama": [
        "Aku adalah AI Chatbot"
    ],

    "ai": [
        "AI adalah kecerdasan buatan yang meniru cara berpikir manusia"
    ],

    "kabar": [
        "Aku baik! Semoga harimu menyenangkan"
    ],

    "kampus": [
        "Kampus adalah tempat untuk belajar dan mengembangkan ilmu"
    ],

    "terima": [
        "Sama-sama",
        "Dengan senang hati!"
    ]
}

# ================== NLP ==================
def get_response(user_input):
    user_input = user_input.lower()

    for key, keywords in data.items():
        for word in keywords:
            if word in user_input:
                return random.choice(responses[key])

    return "Maaf, aku belum memahami pertanyaanmu"

# ================== TEXT TO SPEECH ==================
def speak(text):
    engine = pyttsx3.init()

    voices = engine.getProperty('voices')

    if len(voices) > 1:
        engine.setProperty('voice', voices[1].id)

    engine.setProperty('rate', 170)

    engine.say(text)
    engine.runAndWait()

    engine.stop()

# ================== TYPING ANIMATION ==================
def typing_animation():
    chat.insert(tk.END, "Bot sedang mengetik")
    window.update()

    for _ in range(3):
        chat.insert(tk.END, ".")
        window.update()
        window.after(300)

    chat.insert(tk.END, "\n")

# ================== RESPOND ==================
def respond(user_text):
    typing_animation()

    bot = get_response(user_text)

    chat.insert(tk.END, "🤖 Bot : " + bot + "\n\n")
    chat.yview(tk.END)

    speak(bot)

# ================== SEND TEXT ==================
def send_text():
    user = entry.get()

    if user.strip() == "":
        return

    chat.insert(tk.END, "🧑 Kamu : " + user + "\n")
    chat.yview(tk.END)

    entry.delete(0, tk.END)

    respond(user)

# ================== SPEECH TO TEXT ==================
def listen():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        chat.insert(tk.END, "🎤 Mendengarkan suara...\n")
        chat.yview(tk.END)
        window.update()

        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio, language='id-ID')

        chat.insert(tk.END, "🧑 Kamu : " + text + "\n")
        chat.yview(tk.END)

        respond(text)

    except:
        chat.insert(tk.END, "❌ Suara tidak dikenali\n\n")

# ================== GUI ==================
window = tk.Tk()
window.title("AI Chatbot 🤖")
window.geometry("500x650")
window.configure(bg="#1e1e1e")

# ================== BOT IMAGE ==================
img = Image.open("bot.png")
img = img.resize((120, 120))
bot_img = ImageTk.PhotoImage(img)

img_label = tk.Label(window, image=bot_img, bg="#1e1e1e")
img_label.pack(pady=10)

# ================== TITLE ==================
title = tk.Label(
    window,
    text="AI Chatbot with Voice Interaction",
    font=("Arial", 16, "bold"),
    bg="#1e1e1e",
    fg="white"
)

title.pack()

# ================== CHAT AREA ==================
chat = scrolledtext.ScrolledText(
    window,
    wrap=tk.WORD,
    font=("Arial", 11),
    bg="#2b2b2b",
    fg="white",
    insertbackground="white"
)

chat.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# ================== INPUT ==================
entry = tk.Entry(
    window,
    font=("Arial", 12),
    bg="#3b3b3b",
    fg="white",
    insertbackground="white"
)

entry.pack(padx=10, pady=5, fill=tk.X)

# ================== BUTTON FRAME ==================
btn_frame = tk.Frame(window, bg="#1e1e1e")
btn_frame.pack(pady=10)

# ================== SEND BUTTON ==================
send_btn = tk.Button(
    btn_frame,
    text="Kirim",
    command=send_text,
    font=("Arial", 11, "bold"),
    width=10,
    bg="#4CAF50",
    fg="white"
)

send_btn.pack(side=tk.LEFT, padx=10)

# ================== MIC BUTTON ==================
mic_btn = tk.Button(
    btn_frame,
    text="🎤 Mic",
    command=listen,
    font=("Arial", 11, "bold"),
    width=10,
    bg="#2196F3",
    fg="white"
)

mic_btn.pack(side=tk.LEFT, padx=10)

# ================== RUN ==================
window.mainloop()