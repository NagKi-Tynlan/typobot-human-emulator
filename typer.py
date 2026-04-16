import tkinter as tk
import pyautogui
import pyperclip
import time
import random
import string
import threading

# Global flag to control the loop
is_running = False

def type_with_errors(text):
    global is_running
    is_running = True
    
    status_label.config(text="Starting in 5 seconds... Switch to your doc!")
    root.update()
    time.sleep(5)
    
    for char in text:
        if not is_running:
            status_label.config(text="Stopped by user")
            break
            
      
        
        # Normal typing delays
        if random.random() < 0.05:
            time.sleep(random.uniform(0.3, 0.8))
        else:
            time.sleep(random.uniform(0.05, 0.15))
        
        # 3% chance of typing error
        if random.random() < 0.03 and char.isalpha():
            wrong_char = random.choice(string.ascii_lowercase)
            pyautogui.write(wrong_char)
            time.sleep(random.uniform(0.1, 0.3))
            pyautogui.press('backspace')
            time.sleep(random.uniform(0.05, 0.15))
        
        if char == '\n':
            pyautogui.press('enter')
        else:
            pyautogui.write(char)
    
    if is_running:
        status_label.config(text="Done!")
    is_running = False

def on_start():
    global is_running
    
    if is_running:
        status_label.config(text="Already running!")
        return
    
    text = text_area.get("1.0", tk.END).strip()
    if not text:
        text = pyperclip.paste()
    
    if not text:
        status_label.config(text="Error: No text found.")
    else:
        status_label.config(text="Typing...")
        threading.Thread(target=type_with_errors, args=(text,), daemon=True).start()

def on_stop():
    global is_running
    is_running = False
    status_label.config(text="Stopping...")

# GUI Setup
root = tk.Tk()
root.title("Human Typer Pro")
root.geometry("500x400")

instruction_label = tk.Label(root, text="Paste text below or copy to clipboard:", font=("Arial", 10))
instruction_label.pack(pady=5)

text_area = tk.Text(root, height=10, width=60, wrap=tk.WORD)
text_area.pack(pady=10)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

start_button = tk.Button(button_frame, text="Start Typing", command=on_start, bg="green", fg="white", font=("Arial", 12, "bold"), width=15)
start_button.pack(side=tk.LEFT, padx=10)

stop_button = tk.Button(button_frame, text="Stop", command=on_stop, bg="red", fg="white", font=("Arial", 12, "bold"), width=15)
stop_button.pack(side=tk.LEFT, padx=10)

status_label = tk.Label(root, text="Status: Ready", font=("Arial", 10), fg="blue")
status_label.pack(pady=10)

root.mainloop()