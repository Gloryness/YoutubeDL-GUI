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

class InstallFFmpeg(object):
    def __init__(self, version):
        self.version = version
        self.browse = None
        self.textbox = None
        self.install_btn = None

        self.r = None
        self.root = None

        self.destination_var = StringVar()
        self.version_var = StringVar()
        self.architecture_var = StringVar()
        self.linking_var = StringVar()
        self.extract_var = BooleanVar()

        self.name = 'ffmpeg-4.2.3-win64-static.zip'
        self.link = 'https://ffmpeg.zeranoe.com/builds/win64/static/ffmpeg-4.2.3-win64-static.zip'
        self.size = ''

    def on_installation(self):
        thread = threading.Thread(target=self.ffmpeg_window)
        thread.start()

    def determine_both(self, event):
        self.textbox.config(state=NORMAL)
        self.textbox.delete(0.0, "end")
        self.determine_name('')
        self.determine_size('')
        self.textbox.config(state=DISABLED)

    def determine_name(self, event):
        self.name = 'ffmpeg-'
        self.link = 'https://ffmpeg.zeranoe.com/builds/'

        self.name = self.name+self.version_var.get()+'-'+\
                    self.architecture_var.get().replace(self.architecture_var.get(), self.architecture_var.get().lower().replace(" ", ""))\
                    +'-'+self.linking_var.get().lower()+'.zip'

        self.link = self.link+self.architecture_var.get().replace(self.architecture_var.get(), self.architecture_var.get().lower().replace(" ", ""))\
                    +'/'+self.linking_var.get().lower()+'/'+self.name
        print(self.name)
        print(self.link)
        self.textbox.insert(END, f"NAME: {self.name}\n")

    def determine_size(self, event):
        if self.version_var.get().startswith("4.2") \
            and self.architecture_var.get() == "Win 64"\
            and self.linking_var.get() == "Static":
                if self.version_var.get() == "4.2.3":
                    self.size = '66.76 MB'
                elif self.version_var.get() == "4.2.2":
                    self.size = '66.42 MB'
                elif self.version_var.get() == "4.2.1":
                    self.size = '65.14 MB'
                elif self.version_var.get() == "4.2":
                    self.size = '65.95 MB'

        elif self.version_var.get().startswith("4.2") \
            and self.architecture_var.get() == "Win 32" \
            and self.linking_var.get() == "Static":
                if self.version_var.get() == "4.2.3":
                    self.size = '57.99 MB'
                elif self.version_var.get() == "4.2.2":
                    self.size = '57.43 MB'
                elif self.version_var.get() == "4.2.1":
                    self.size = '56.87 MB'
                elif self.version_var.get() == "4.2":
                    self.size = '56.12 MB'

        elif self.version_var.get().startswith("4.2") \
            and self.architecture_var.get() == "Mac OS 64" \
            and self.linking_var.get() == "Static":
                if self.version_var.get() == "4.2.3":
                    self.size = '67.09 MB'
                elif self.version_var.get() == "4.2.2":
                    self.size = '67.13 MB'
                elif self.version_var.get() == "4.2.1":
                    self.size = '66.54 MB'
                elif self.version_var.get() == "4.2":
                    self.size = '66.25 MB'

        elif self.version_var.get().startswith("4.2") \
            and self.architecture_var.get() == "Win 64"\
            and self.linking_var.get() == "Shared":
                if self.version_var.get() == "4.2.3":
                    self.size = '25.17 MB'
                elif self.version_var.get() == "4.2.2":
                    self.size = '25.03 MB'
                elif self.version_var.get() == "4.2.1":
                    self.size = '24.87 MB'
                elif self.version_var.get() == "4.2":
                    self.size = '24.34 MB'

        elif self.version_var.get().startswith("4.2") \
            and self.architecture_var.get() == "Win 32" \
            and self.linking_var.get() == "Shared":
                if self.version_var.get() == "4.2.3":
                    self.size = '22.22 MB'
                elif self.version_var.get() == "4.2.2":
                    self.size = '22.18 MB'
                elif self.version_var.get() == "4.2.1":
                    self.size = '21.77 MB'
                elif self.version_var.get() == "4.2":
                    self.size = '21.53 MB'

        elif self.version_var.get().startswith("4.2") \
            and self.architecture_var.get() == "Mac OS 64" \
            and self.linking_var.get() == "Shared":
                if self.version_var.get() == "4.2.3":
                    self.size = '25.29 MB'
                elif self.version_var.get() == "4.2.2":
                    self.size = '25.01 MB'
                elif self.version_var.get() == "4.2.1":
                    self.size = '24.91 MB'
                elif self.version_var.get() == "4.2":
                    self.size = '24.61 MB'

        elif self.version_var.get().startswith("4.2") \
            and self.architecture_var.get() == "Win 64" \
            and self.linking_var.get() == "Dev":
                if self.version_var.get() == "4.2.3":
                    self.size = '604.90 KB'
                elif self.version_var.get() == "4.2.2":
                    self.size = '604.06 KB'
                elif self.version_var.get() == "4.2.1":
                    self.size = '603.58 KB'
                elif self.version_var.get() == "4.2":
                    self.size = '603.53 KB'

        elif self.version_var.get().startswith("4.2") \
            and self.architecture_var.get() == "Win 32" \
            and self.linking_var.get() == "Dev":
                if self.version_var.get() == "4.2.3":
                    self.size = '605.59 KB'
                elif self.version_var.get() == "4.2.2":
                    self.size = '605.23 KB'
                elif self.version_var.get() == "4.2.1":
                    self.size = '604.51 KB'
                elif self.version_var.get() == "4.2":
                    self.size = '604.15 KB'

        elif self.version_var.get().startswith("4.2") \
            and self.architecture_var.get() == "Mac OS 64" \
            and self.linking_var.get() == "Dev":
                if self.version_var.get() == "4.2.3":
                    self.size = '422.82 KB'
                elif self.version_var.get() == "4.2.2":
                    self.size = '422.48 KB'
                elif self.version_var.get() == "4.2.1":
                    self.size = '421.96KB'
                elif self.version_var.get() == "4.2":
                    self.size = '421.37 KB'

        print(self.size)
        self.textbox.insert(END, f"SIZE: {self.size}")

    def browse_cmd(self):
        if len(self.destination_var.get()) <= 1:
            destination = filedialog.askdirectory(initialdir="C:/", parent=self.root)
        if len(self.destination_var.get()) > 1:
            destination = filedialog.askdirectory(initialdir=self.destination_var.get(), parent=self.root)
        if destination == "C:/" or destination == "R:/" or destination == "D:/" or destination == "P:/" or destination == "S:/" \
            or destination == "U:/" or destination == "Q:/" or destination == "A:/" or destination == "F:/" or destination == "G:/" \
            or destination == "B:/" or destination == "A:/" or destination == "T:/" or destination == "W:/" or destination == "Z:/" \
                or destination == "" or len(destination) <= 2:
            self.browse.config(state=NORMAL)
            self.browse.delete(0, END)
            self.browse.insert(0, destination)
            self.browse.config(state=DISABLED)
        else:
            self.browse.config(state=NORMAL)
            self.browse.delete(0, END)
            self.browse.insert(0, destination+'/')
            self.browse.config(state=DISABLED)

    def ffmpeg_window(self):
        global count
        if count == 1:
            self.root = Toplevel()
            self.root.title('Installing FFmpeg  |  YoutubeDL GUI  |   v{}'.format(self.version))
            self.root.iconbitmap('images/#app.ico')
            self.root.resizable(False, False)
            self.root.configure(bg='#cbdbfc', bd=5)
            self.root.geometry("450x370")
            self.root.protocol('WM_DELETE_WINDOW', lambda: reset(self.root))

            version_label = Label(self.root, text="FFmpeg Version", bg='#cbdbfc')
            version_label.place(x=40, y=20)

            version_options = [
                "4.2.3",
                "4.2.3",
                "4.2.2",
                "4.2.1",
                "4.2"
            ]

            version_opts = ttk.OptionMenu(self.root, self.version_var, *version_options, command=self.determine_both)
            version_opts.place(x=55, y=40)
            self.version_var.set(version_options[1])

            architecture_label = Label(self.root, text="FFmpeg Architecture", bg='#cbdbfc')
            architecture_label.place(x=160, y=20)

            architecture_options = [
                "Win 64",
                "Win 64",
                "Win 32",
                "Mac OS 64"
            ]

            architecture_opts = ttk.OptionMenu(self.root, self.architecture_var, *architecture_options, command=self.determine_both)
            architecture_opts.place(x=185, y=40)
            self.architecture_var.set(architecture_options[1])

            linking_label = Label(self.root, text="FFmpeg Linking", bg='#cbdbfc')
            linking_label.place(x=303, y=20)

            linking_options = [
                "Static",
                "Static",
                "Shared",
                "Dev"
            ]

            linking_opts = ttk.OptionMenu(self.root, self.linking_var, *linking_options, command=self.determine_both)
            linking_opts.place(x=320, y=40)
            self.linking_var.set(linking_options[1])

            browse_label = Label(self.root, text="FFmpeg Destination", bg='#cbdbfc')
            browse_label.place(x=160, y=80)

            self.destination_var = StringVar()

            self.browse = Entry(self.root, bd=1, width=50, relief=SOLID, state=DISABLED, textvariable=self.destination_var)
            self.browse.place(x=62, y=100)

            style1 = ttk.Style()
            style1.configure('some.TButton', background='black')

            browse_btn = ttk.Button(self.root, text="Browse", style='some.TButton', command=self.browse_cmd)
            browse_btn.place(x=175, y=120)

            self.install_btn = ttk.Button(self.root, text="Download FFmpeg", style="some.TButton", command=self.on_install)
            self.install_btn.place(x=158, y=175)

            style = ttk.Style()
            style.configure('TCheckbutton', background='#cbdbfc')

            extract = ttk.Checkbutton(self.root, text="Extract files from .zip after download", style='TCheckbutton', variable=self.extract_var,
                                      onvalue=True, offvalue=False)
            extract.place(x=105, y=150)

            exit_btn = ttk.Button(self.root, text="Exit", style="some.TButton", command=lambda: reset(self.root))
            exit_btn.place(x=361, y=175)

            self.textbox = scrolledtext.ScrolledText(self.root, height=10, width=59, bd=2, state=DISABLED, font='Cooper 9')
            self.textbox.place(x=1, y=200)
            self.textbox.config(state=NORMAL)
            self.textbox.delete(0.0, "end")
            self.textbox.insert(0.0, "NAME: ffmpeg-4.2.3-win64-static.zip\nSIZE: 66.76 MB")
            self.textbox.config(state=DISABLED)
            count = 2
        else:
            pass

    def send_content(self):
        with open(f'{self.destination_var.get()}{self.name}', 'wb') as install:  # since we grabbed the contents, the content was extracted in bytes - therefore we write to it in bytes.
            install.write(self.r.content)
            self.textbox.config(state=NORMAL)
            self.textbox.insert(END, "\nAll content has been sent to a .zip file.\n")
            t = threading.Event()
            t.wait(1)

        if self.extract_var.get():
            try:
                with ZipFile(f'{self.destination_var.get()}{self.name}') as zipfile:
                    self.textbox.insert(END, "\nExtracting files from .zip file...\n")
                    with zipfile.extractall(f'{self.destination_var.get()}') as yeet:
                        pass
            except AttributeError:
                t = threading.Event()
                t.wait(2.8)
                self.install_btn.config(state=ACTIVE)
                self.textbox.insert(END, "Extraction was a complete success.\n\nFFmpeg has successfully been downloaded.")
                self.textbox.config(state=DISABLED)
                zipfile.close()
            except not AttributeError as exc:
                self.install_btn.config(state=ACTIVE)
                self.textbox.config(state=NORMAL)
                self.textbox.insert(END, "\nAn error occured and the error has been logged to downloading.log\n")
                self.textbox.config(state=DISABLED)
                logger.exception(f'An error occured while extracting files from the .zip file: {exc}\nIf error says "__enter__", please ignore as this is intended.')
        else:
            t = threading.Event()
            t.wait(1.2)
            self.install_btn.config(state=ACTIVE)
            self.textbox.insert(END, "\nFFmpeg has successfully been downloaded.\n")
            self.textbox.config(state=DISABLED)

    def on_install(self):
        self.install_btn.config(state=DISABLED)
        thread = threading.Thread(target=self.install)
        thread.start()

    def install(self):

        self.textbox.config(state=NORMAL)
        self.textbox.delete(0.0, "end")
        self.textbox.insert(0.0, "Downloading contents...\n")
        self.textbox.config(state=DISABLED)

        t = threading.Event()
        t.wait(1)
        try:
            self.r = requests.get(self.link)
        except Exception as exc:
            self.textbox.config(state=NORMAL)
            self.install_btn.config(state=ACTIVE)
            self.textbox.insert(END, "\nAn error occured and the error has been logged to downloading.log\n")
            self.textbox.config(state=DISABLED)
            logger.exception(f'An error occured while grabbing FFmpeg installation data: {exc}')
            quit(self.install)
        self.textbox.config(state=NORMAL)
        self.textbox.insert(END, "Finished downloading contents...\n\n")

        t = threading.Event()
        t.wait(1.75)
        self.textbox.insert(END, "Sending all content to a .zip file...")
        self.textbox.config(state=DISABLED)

        t = threading.Event()
        t.wait(1.2)
        self.send_content()