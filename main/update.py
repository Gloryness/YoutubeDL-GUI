import requests
import threading
import subprocess
from zipfile import *
import os

from tkinter import *
from tkinter import scrolledtext, ttk

count = 1
def reset(win):
    global count
    count = 1
    win.destroy()

def restart(win):
    global count
    count = 1
    win.quit()
    subprocess.call("update_manager.exe")

class SendRequest:
    def __init__(self, version):
        self.version = version

        global count
        if count == 1:
            self.update_win = Toplevel()
            self.update_win.title('Installing WebDriver  |  YoutubeDL GUI  |   v{}'.format(self.version))
            self.update_win.iconbitmap('images/#app.ico')
            self.update_win.resizable(False, False)
            self.update_win.configure(bg='#cbdbfc', bd=5)
            self.update_win.geometry("450x300")
            self.update_win.protocol('WM_DELETE_WINDOW', lambda: reset(self.update_win))

            self.text_box = scrolledtext.ScrolledText(self.update_win, height=17, width=58, bd=2, state=DISABLED, bg="#bfb6b6", fg="#630000", font='Cooper 10')
            self.text_box.place(x=5, y=5)

            count = 2
        else:
            pass

    def on_send_request(self):
        thread = threading.Timer(1, self.send_request)
        thread.start()

    def send_request(self):
        self.r = requests.get('https://raw.githubusercontent.com/Gloryness/YoutubeDL-GUI/master/version.txt')
        self.text_box.config(state=NORMAL)
        self.text_box.insert(0.0, "Comparing GUI version to newest version...\n")
        self.text_box.config(state=DISABLED)
        thread_event = threading.Event()
        thread_event.wait(1.50)
        self.get_request()

    def get_request(self):
        if self.r.text.strip() == self.version:
            self.text_box.config(state=NORMAL)
            self.text_box.insert(END, "GUI is up-to-date!\n")
            self.text_box.config(state=DISABLED)
            thread_event = threading.Event()
            thread_event.wait(1.50)
            reset(self.update_win)
        else:
            self.text_box.config(state=NORMAL)
            self.text_box.insert(END, "GUI seems to be out of date.\n")
            thread_event = threading.Event()
            thread_event.wait(1.20)
            try:
                with open('Youtube-DL GUI.exe') as t:
                    t.close()
            except FileNotFoundError:
                self.text_box.insert(END, "Sorry but before we can update, your current .exe file must be named 'Youtube-DL GUI.exe', thanks!\n")
                self.text_box.config(state=DISABLED)
                quit(self.get_request)
            self.text_box.insert(END, "Downloading contents of newest version...\n")
            self.text_box.config(state=DISABLED)
            try:
                self.download = requests.get('https://github.com/Gloryness/YoutubeDL-GUI/raw/master/exe.zip', timeout=10)
                self.text_box.config(state=NORMAL)
                self.text_box.insert(END, "Finished downloading contents...\n")
                self.text_box.config(state=DISABLED)
                thread_event = threading.Event()
                thread_event.wait(1.20)
            except:
                self.text_box.config(state=NORMAL)
                self.text_box.insert(END, "\nAn error occured while trying to update.\n")
                self.text_box.config(state=DISABLED)
                quit(self.get_request)
            self.file_handling()

    def file_handling(self):
        self.text_box.config(state=NORMAL)
        self.text_box.insert(END, "\nWriting all content to .zip file...\n")
        self.text_box.config(state=DISABLED)
        thread_event = threading.Event()
        thread_event.wait(1.40)
        try:
            with open(f'exe.zip', 'wb') as install:
                install.write(self.download.content)
        except:
            self.text_box.config(state=NORMAL)
            self.text_box.insert(END, "Permission denied. Download failed.\n")
            self.text_box.config(state=DISABLED)
            quit(self.file_handling)

        self.text_box.config(state=NORMAL)
        self.text_box.insert(END, "Extracting all content from .zip file...\n")
        self.text_box.config(state=DISABLED)
        thread_event = threading.Event()
        thread_event.wait(1.60)
        with ZipFile(f'exe.zip') as zipfile:
            try:
                zipfile.extractall(os.getcwd())
            except AttributeError:
                self.text_box.config(state=NORMAL)
                self.text_box.insert(END, "Finished extracting all content from .zip file...\n")
                self.text_box.config(state=DISABLED)
            except not AttributeError:
                self.text_box.config(state=NORMAL)
                self.text_box.insert(END, "\nAn error occured while trying to extract files from .zip.\n")
                self.text_box.config(state=DISABLED)
                quit(self.file_handling)
        thread_event = threading.Event()
        thread_event.wait(1.60)
        self.text_box.config(state=NORMAL)
        self.text_box.insert(END, "\nDeleting content from .zip file...\n")
        self.text_box.config(state=DISABLED)
        os.remove(f'exe.zip')
        thread_event = threading.Event()
        thread_event.wait(1.20)
        self.text_box.config(state=NORMAL)
        self.text_box.insert(END, "Finished deleting content from .zip file...\n")
        thread_event = threading.Event()
        thread_event.wait(0.60)
        self.text_box.insert(END, "\nRestart is required to apply update changes.\n")
        self.text_box.config(state=DISABLED)

        restart_btn = ttk.Button(self.update_win, text="RESTART", style="some.TButton", command=lambda: restart(self.update_win))
        restart_btn.place(x=180, y=250)