import requests
import threading
import logging
from zipfile import *

from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext, filedialog

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('downloading.log')
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)

file_handler2 = logging.FileHandler('downloading.log')
file_handler2.setLevel(logging.CRITICAL)
file_handler2.setFormatter(formatter)

file_handler3 = logging.FileHandler('downloading.log')
file_handler3.setLevel(logging.INFO)
file_handler3.setFormatter(formatter)

file_handler4 = logging.FileHandler('downloading.log')
file_handler4.setLevel(logging.WARNING)
file_handler4.setFormatter(formatter)

file_handler5 = logging.FileHandler('downloading.log')
file_handler5.setLevel(logging.DEBUG)
file_handler5.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(file_handler2)
logger.addHandler(file_handler3)
logger.addHandler(file_handler4)
logger.addHandler(file_handler5)
logger.addHandler(stream_handler)

count = 1

def reset(win):
    global count
    count = 1
    win.destroy()

class InstallWebDriver(object):
    def __init__(self, version):
        self.version = version

        self.name = 'geckodriver-v0.26.0-win64.zip'
        self.link = 'https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-win64.zip'
        self.size = ''

    def on_webdriver_window(self):
        thread = threading.Thread(target=self.webdriver_window)
        thread.start()

    def browse_cmd(self):
        if len(self.destination_var.get()) <= 1:
            destination = filedialog.askdirectory(initialdir="C:/", parent=self.webdriver_win)
            self.browse.config(state=NORMAL)
            self.browse.delete(0, END)
            self.browse.insert(0, destination)
            self.browse.config(state=DISABLED)
        elif len(self.destination_var.get()) > 1:
            destination = filedialog.askdirectory(initialdir=self.destination_var.get(), parent=self.webdriver_win)
            self.browse.config(state=NORMAL)
            self.browse.delete(0, END)
            self.browse.insert(0, destination)
            self.browse.config(state=DISABLED)

    def change_architecture(self, event):
        if self.browsers_var.get() == "Firefox":
            self.install_btn.config(state=NORMAL)
            self.architecture.destroy()
            self.architecture_options = [
                "Win64",
                "Win64",
                "Win32",
                "MacOS",
                "Linux64",
                "Linux32"
            ]
            self.architecture_var = StringVar()
            self.architecture = ttk.OptionMenu(self.webdriver_win, self.architecture_var, *self.architecture_options, command=self.insert_textbox)
            self.architecture.place(x=270, y=15, width=120)
            self.architecture_var.set(self.architecture_options[1])

        elif self.browsers_var.get() == "Chrome":
            self.install_btn.config(state=NORMAL)
            self.architecture.destroy()
            self.architecture_options = [
                "Win32",
                "Win32",
                "Mac64",
                "Linux64"
            ]
            self.architecture_var = StringVar()
            self.architecture = ttk.OptionMenu(self.webdriver_win, self.architecture_var, *self.architecture_options, command=self.insert_textbox)
            self.architecture.place(x=270, y=15, width=120)
            self.architecture_var.set(self.architecture_options[1])

        elif self.browsers_var.get() == "Edge":
            self.install_btn.config(state=NORMAL)
            self.architecture.destroy()
            self.architecture_options = [
                "Win64",
                "Win64",
                "Win32",
                "Mac64"
            ]
            self.architecture_var = StringVar()
            self.architecture = ttk.OptionMenu(self.webdriver_win, self.architecture_var, *self.architecture_options, command=self.insert_textbox)
            self.architecture.place(x=270, y=15, width=120)
            self.architecture_var.set(self.architecture_options[1])

        elif self.browsers_var.get() == "Internet Explorer":
            self.install_btn.config(state=NORMAL)
            self.architecture.destroy()
            self.architecture_options = [
                "Win32",
                "Win32",
                "x64"
            ]
            self.architecture_var = StringVar()
            self.architecture = ttk.OptionMenu(self.webdriver_win, self.architecture_var, *self.architecture_options, command=self.insert_textbox)
            self.architecture.place(x=270, y=15, width=120)
            self.architecture_var.set(self.architecture_options[1])

        elif self.browsers_var.get() == "Opera":
            self.install_btn.config(state=NORMAL)
            self.architecture.destroy()
            self.architecture_options = [
                "Win64",
                "Win64",
                "Win32",
                "Mac64",
                "Linux64"
            ]
            self.architecture_var = StringVar()
            self.architecture = ttk.OptionMenu(self.webdriver_win, self.architecture_var, *self.architecture_options, command=self.insert_textbox)
            self.architecture.place(x=270, y=15, width=120)
            self.architecture_var.set(self.architecture_options[1])

        elif self.browsers_var.get() == "Safari (built in, so no need to download)":
            self.install_btn.config(state=DISABLED)
            self.architecture.destroy()
            self.architecture_options = [
                "None",
                "None",
                "None",
                "None"
            ]
            self.architecture_var = StringVar()
            self.architecture = ttk.OptionMenu(self.webdriver_win, self.architecture_var, *self.architecture_options, command=self.insert_textbox)
            self.architecture.place(x=270, y=15, width=120)
            self.architecture_var.set(self.architecture_options[1])

        self.insert_textbox('')

    def insert_textbox(self, event):
        arch = self.architecture_var.get()
        if self.browsers_var.get() == "Firefox":
            self.name = f"geckodriver-v0.26.0-{arch.lower()}.{'zip' if arch == 'Win32' or arch == 'Win64' else 'tar.gz'}"
            self.size = f"{'1.46 MB' if arch == 'Win64' else '1.37 MB' if arch == 'Win32' else '1.91 MB' if arch == 'MacOS' else '2.28 MB' if arch == 'Linux64' else '2.22 MB'}"
            self.link = f"https://github.com/mozilla/geckodriver/releases/download/v0.26.0/{self.name}"
            self.textbox.config(state=NORMAL)
            self.textbox.delete(0.0, "end")
            self.textbox.insert(0.0, f"NAME: {self.name}\nSIZE: {self.size}")
            self.textbox.config(state=DISABLED)

        elif self.browsers_var.get() == "Chrome":
            self.name = f"chromedriver_{arch.lower()}.zip"
            self.size = f"{'4.63 MB' if arch == 'Win32' else '6.99 MB' if arch == 'Mac64' else '5.06 MB'}"
            self.link = f"https://chromedriver.storage.googleapis.com/84.0.4147.30/{self.name}"
            self.textbox.config(state=NORMAL)
            self.textbox.delete(0.0, "end")
            self.textbox.insert(0.0, f"NAME: {self.name}\nSIZE: {self.size}")
            self.textbox.config(state=DISABLED)

        elif self.browsers_var.get() == "Edge":
            self.name = f"edgedriver_{arch.lower()}.zip"
            self.size = f"{'12.6 MB' if arch == 'Mac64' else '6.00 MB' if arch == 'Win64' else '5.49 MB'}"
            self.link = f"https://msedgedriver.azureedge.net/85.0.548.0/{self.name}"
            self.textbox.config(state=NORMAL)
            self.textbox.delete(0.0, "end")
            self.textbox.insert(0.0, f"NAME: {self.name}\nSIZE: {self.size}")
            self.textbox.config(state=DISABLED)

        elif self.browsers_var.get() == "Internet Explorer":
            self.name = f"IEDriverServer_{arch}_3.9.0.zip"
            self.size = f"{'0.94 MB' if arch == 'Win32' else '1.08 MB'}"
            self.link = f"https://selenium-release.storage.googleapis.com/3.9/{self.name}"
            self.textbox.config(state=NORMAL)
            self.textbox.delete(0.0, "end")
            self.textbox.insert(0.0, f"NAME: {self.name}\nSIZE: {self.size}")
            self.textbox.config(state=DISABLED)

        elif self.browsers_var.get() == "Opera":
            self.name = f"operadriver_{arch.lower()}.zip"
            self.size = f"{'4.44 MB' if arch == 'Win64' else '4.27 MB' if arch == 'Win32' else '6.90 MB' if arch == 'Mac64' else '5.23 MB'}"
            self.link = f"https://github.com/operasoftware/operachromiumdriver/releases/download/v.81.0.4044.113/{self.name}"
            self.textbox.config(state=NORMAL)
            self.textbox.delete(0.0, "end")
            self.textbox.insert(0.0, f"NAME: {self.name}\nSIZE: {self.size}")
            self.textbox.config(state=DISABLED)

        elif self.browsers_var.get() == "Safari (built in, so no need to download)":
            self.textbox.config(state=NORMAL)
            self.textbox.delete(0.0, "end")
            self.textbox.insert(0.0, "NAME: ///////\nSIZE: ///////")
            self.textbox.config(state=DISABLED)
        print(self.name, self.size, self.link, sep='\n')

    def webdriver_window(self):
        global count
        if count == 1:
            self.webdriver_win = Toplevel()
            self.webdriver_win.title('Installing WebDriver  |  YoutubeDL GUI  |   v{}'.format(self.version))
            self.webdriver_win.iconbitmap('images/#app.ico')
            self.webdriver_win.resizable(False, False)
            self.webdriver_win.configure(bg='#cbdbfc', bd=5)
            self.webdriver_win.geometry("450x370")
            self.webdriver_win.protocol('WM_DELETE_WINDOW', lambda: reset(self.webdriver_win))

            browser_label = Label(self.webdriver_win, text="Browser", bg='#cbdbfc')
            browser_label.place(x=100, y=-5)

            self.browsers = [
                "Firefox",
                "Firefox",
                "Chrome",
                "Edge",
                "Internet Explorer",
                "Opera",
                "Safari (built in, so no need to download)"
            ]

            self.browsers_var = StringVar()
            self.browser = ttk.OptionMenu(self.webdriver_win, self.browsers_var, *self.browsers, command=self.change_architecture)
            self.browser.place(x=70, y=15, width=120)
            self.browsers_var.set(self.browsers[1])

            architecture_label = Label(self.webdriver_win, text="Architecture", bg='#cbdbfc')
            architecture_label.place(x=290, y=-5)

            self.architecture_options = [
                "Win64",
                "Win64",
                "Win32",
                "MacOS",
                "Linux64",
                "Linux32"
            ]
            self.architecture_var = StringVar()
            self.architecture = ttk.OptionMenu(self.webdriver_win, self.architecture_var, *self.architecture_options, command=self.insert_textbox)
            self.architecture.place(x=270, y=15, width=120)
            self.architecture_var.set(self.architecture_options[1])

            style = ttk.Style()
            style.configure('TCheckbutton', background='#cbdbfc')
            style.configure('some.TButton', background='black')

            self.extract_var = StringVar()
            extract = ttk.Checkbutton(self.webdriver_win, text="Extract file from .zip after download", style='TCheckbutton', variable=self.extract_var,
                                      onvalue=True, offvalue=False)
            extract.place(x=110, y=150)

            self.destination_var = StringVar()

            browse_label = Label(self.webdriver_win, text="WebDriver Destination", bg='#cbdbfc')
            browse_label.place(x=158, y=60)

            self.browse = Entry(self.webdriver_win, bd=1, width=50, relief=SOLID, state=DISABLED, textvariable=self.destination_var)
            self.browse.place(x=62, y=80)

            browse_btn = ttk.Button(self.webdriver_win, text="Browse", style='some.TButton', command=self.browse_cmd)
            browse_btn.place(x=175, y=100)

            self.install_btn = ttk.Button(self.webdriver_win, text="Download WebDriver", style="some.TButton", command=self.on_install)
            self.install_btn.place(x=156, y=175)

            exit_btn = ttk.Button(self.webdriver_win, text="Exit", style="some.TButton", command=lambda: reset(self.webdriver_win))
            exit_btn.place(x=361, y=175)

            self.textbox = scrolledtext.ScrolledText(self.webdriver_win, height=10, width=59, bd=2, state=DISABLED, font='Cooper 9')
            self.textbox.place(x=1, y=200)
            self.insert_textbox('')
            count = 2
        else:
            pass

    def send_content(self):
        try:
            with open(f'{self.destination_var.get()}{"/" if not self.destination_var.get().endswith("/") else ""}{self.name}', 'wb') as install:
                install.write(self.r.content)
                self.textbox.config(state=NORMAL)
                self.textbox.insert(END, "\nAll content has been sent to a .zip file.\n")
                t = threading.Event()
                t.wait(1)
        except:
            self.textbox.config(state=NORMAL)
            self.textbox.insert(END, "\nPermission denied. Download failed.")
            self.textbox.config(state=DISABLED)
            quit(self.send_content)

        if self.extract_var.get():
            try:
                with ZipFile(f'{self.destination_var.get()}{"/" if not self.destination_var.get().endswith("/") else ""}{self.name}') as zipfile:
                    self.textbox.insert(END, "\nExtracting files from .zip file...\n")
                    zipfile.extractall(f'{self.destination_var.get()}')

            except AttributeError:
                t = threading.Event()
                t.wait(2.8)
                self.install_btn.config(state=NORMAL)
                self.textbox.insert(END, f"Extraction was a complete success.\n\nThe WebDriver has successfully been downloaded.")
                self.textbox.config(state=DISABLED)
                zipfile.close()
            except not AttributeError as exc:
                self.install_btn.config(state=NORMAL)
                self.textbox.config(state=NORMAL)
                self.textbox.insert(END, "\nAn error occured and the error has been logged to downloading.log\n")
                self.textbox.config(state=DISABLED)
                logger.exception(f'An error occured while extracting files from the .zip file: {exc}\nIf error says "__enter__", please ignore as this is intended.')
        else:
            t = threading.Event()
            t.wait(1.2)
            self.install_btn.config(state=NORMAL)
            self.textbox.insert(END, f"\nThe WebDriver has successfully been downloaded.\n")
            self.textbox.config(state=DISABLED)

    def on_install(self):
        thread = threading.Thread(target=self.install)
        thread.start()

    def install(self):
        self.textbox.config(state=NORMAL)
        self.textbox.delete(0.0, "end")
        self.textbox.insert(0.0, "Downloading contents...\n")
        self.textbox.config(state=DISABLED)

        try:
            self.r  = requests.get(self.link)
        except Exception as exc:
            self.textbox.config(state=NORMAL)
            self.install_btn.config(state=NORMAL)
            self.textbox.insert(END, "\nAn error occured and the error has been logged to downloading.log\n")
            self.textbox.config(state=DISABLED)
            logger.exception(f'An error occured while grabbing WebDriver installation data for {self.link}:\n {exc}')
            quit(self.install)
        t = threading.Event()
        t.wait(1.25)
        self.textbox.config(state=NORMAL)
        self.textbox.insert(END, "Finished downloading contents...\n\n")

        t = threading.Event()
        t.wait(1.75)
        self.textbox.insert(END, "Sending all content to a .zip file...")
        self.textbox.config(state=DISABLED)

        t = threading.Event()
        t.wait(1.2)
        self.send_content()