import tkinter as tk
from tkinter import scrolledtext
import json
import random
import re
import pyttsx3
import speech_recognition as sr
from PIL import Image, ImageTk
import threading
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# ================== LOAD DATA ==================
with open(BASE_DIR / 'faq.json') as file:
    data = json.load(file)

responses = {
    "sapaan": [
        "Halo juga!",
        "Hai! Senang bertemu denganmu"
    ],

    "nama": [
        "Aku adalah AI Chatbot yang dibuat untuk project UTS Artificial Intelligence."
    ],

    "ai": [
        "AI adalah kecerdasan buatan yang membuat komputer dapat meniru kemampuan manusia seperti belajar, mengenali pola, memahami bahasa, dan mengambil keputusan."
    ],

    "aiml": [
        "AIML adalah Artificial Intelligence Markup Language, yaitu bahasa berbasis tag XML untuk membuat pola pertanyaan dan jawaban pada chatbot."
    ],

    "bab4": [
        "Modul Bab 4 membahas pembuatan chatbot menggunakan AIML dan Espeak, termasuk penggunaan jawaban random untuk merespons pertanyaan user."
    ],

    "bab5": [
        "Modul Bab 5 membahas percakapan chatbot yang dapat menyimpan nama user dan menjawab pertanyaan lanjutan seperti Do you know me."
    ],

    "srai": [
        "Tag srai pada AIML digunakan untuk mengarahkan satu pola pertanyaan ke pola lain, sehingga beberapa pertanyaan dapat memakai jawaban yang sama."
    ],

    "tts": [
        "Text to speech adalah teknologi untuk mengubah teks menjadi suara. Pada project ini, jawabannya dibacakan memakai library pyttsx3."
    ],

    "stt": [
        "Speech to text adalah teknologi untuk mengubah suara menjadi teks. Pada project ini, suara user dikenali memakai library SpeechRecognition."
    ],

    "project_a": [
        "Project A meminta chatbot dibuat dengan AIML dan Espeak sesuai langkah pada modul Bab 4 dan Bab 5."
    ],

    "project_b": [
        "Project B membebaskan mahasiswa membuat sistem AI NLP selain AIML, termasuk chatbot dengan suara menggunakan Python atau library lain."
    ],

    "penyanyi_favorit": [
        "Penyanyi favoritmu adalah Ariel, vokalis dari band NOAH."
    ],

    "dokumentasi": [
        "Hasil project UTS perlu didokumentasikan dalam bentuk video yang menampilkan proses pembuatan, cara kerja, dan hasil akhir chatbot."
    ],

    "nilai_uts": [
        "Penilaian UTS dilihat dari kesesuaian hasil dengan modul, fitur chatbot, fitur suara, dokumentasi video, dan ketepatan waktu pengumpulan."
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

user_name = ""

# ================== NLP ==================
def extract_user_name(text):
    patterns = [
        r"\bmy name is\s+(.+)",
        r"\bnama saya\s+(.+)",
        r"\bnamaku\s+(.+)",
        r"\baku bernama\s+(.+)"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            name = re.sub(r"[^\w\s]", "", match.group(1)).strip()
            return name

    return ""

def get_response(user_input):
    global user_name

    original_input = user_input.strip()
    user_input = original_input.lower()

    name = extract_user_name(original_input)
    if name:
        user_name = name.title()
        return f"Halo {user_name}, nice to meet you"

    know_me_questions = [
        "do you know me",
        "who am i",
        "siapa aku",
        "kamu tahu aku"
    ]

    if any(question in user_input for question in know_me_questions):
        if user_name:
            return f"Sure buddy, you are {user_name}"
        return "Aku belum tahu namamu. Coba ketik: My name is Sekar"

    for key, keywords in data.items():
        for word in keywords:
            pattern = r"\b" + re.escape(word.lower()) + r"\b"
            if re.search(pattern, user_input):
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

def set_controls_enabled(enabled):
    state = tk.NORMAL if enabled else tk.DISABLED
    entry.config(state=state)
    send_btn.config(state=state)
    mic_btn.config(state=state)

def speak_async(text):
    set_controls_enabled(False)

    def worker():
        try:
            speak(text)
        finally:
            window.after(0, lambda: set_controls_enabled(True))

    threading.Thread(target=worker, daemon=True).start()

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

    bot_response = get_response(user_text)

    chat.insert(tk.END, "🤖 Bot : " + bot_response + "\n\n")
    chat.yview(tk.END)

    speak_async(bot_response)

def greet_on_start():
    greeting = "Halo, selamat datang di AI Chatbot. Silakan ketik pertanyaan atau gunakan tombol mic."
    chat.insert(tk.END, "🤖 Bot : " + greeting + "\n\n")
    chat.yview(tk.END)
    speak_async(greeting)

# ================== SEND TEXT ==================
def send_text():
    user = entry.get()

    if user.strip() == "":
        return

    chat.insert(tk.END, "🧑 Kamu : " + user + "\n")
    chat.yview(tk.END)

    entry.delete(0, tk.END)

    respond(user)

def send_text_from_enter(event):
    send_text()

# ================== SPEECH TO TEXT ==================
def listen():
    set_controls_enabled(False)
    chat.insert(tk.END, "🎤 Mendengarkan suara...\n")
    chat.yview(tk.END)

    def finish_with_text(text):
        chat.insert(tk.END, "🧑 Kamu : " + text + "\n")
        chat.yview(tk.END)
        respond(text)

    def finish_with_error(message):
        chat.insert(tk.END, message + "\n\n")
        chat.yview(tk.END)
        set_controls_enabled(True)

    def worker():
        r = sr.Recognizer()

        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source, timeout=5, phrase_time_limit=8)

            text = r.recognize_google(audio, language='id-ID')
            window.after(0, lambda: finish_with_text(text))
        except AttributeError:
            window.after(0, lambda: finish_with_error("❌ Fitur mic belum bisa dipakai karena PyAudio belum terinstall"))
        except sr.WaitTimeoutError:
            window.after(0, lambda: finish_with_error("❌ Tidak ada suara yang terdengar"))
        except sr.UnknownValueError:
            window.after(0, lambda: finish_with_error("❌ Suara tidak dikenali"))
        except sr.RequestError:
            window.after(0, lambda: finish_with_error("❌ Layanan pengenal suara tidak dapat diakses"))

    threading.Thread(target=worker, daemon=True).start()

# ================== GUI ==================
window = tk.Tk()
window.title("AI Chatbot 🤖")
window.geometry("500x650")
window.state("zoomed")
window.configure(bg="#1e1e1e")

# ================== BOT IMAGE ==================
img = Image.open(BASE_DIR / "bot.png")
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
entry.bind("<Return>", send_text_from_enter)

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
window.after(500, greet_on_start)
window.mainloop()
