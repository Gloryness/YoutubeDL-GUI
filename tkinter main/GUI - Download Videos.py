from __future__ import unicode_literals, print_function

from BorderEntry import BorderedEntry
from tkinter import *
from tkinter import messagebox, filedialog, scrolledtext
from tkinter import ttk

from selenium import webdriver
from selenium.common.exceptions import WebDriverException

import youtube_dl as yt
from youtube_dl import postprocessor
from PIL import ImageTk, Image
import math
import time
import subprocess
import os
import sys

import threading
import logging
import webbrowser

__version__ = '0.6.0 BETA'

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s--%(name)s--%(message)s')

file_handler = logging.FileHandler('downloading.log')
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

PATH = 'C:/Users/Gloryness/geckodriver.exe'

root = Tk()
root.title("Youtube-DL GUI by Gloryness -  v{}".format(__version__))
root.iconbitmap('C:/Users/Gloryness/AppData/Local/atom/app.ico')
root.resizable(False, False)
root.configure(bg='#cbdbfc', bd=5)
root.geometry("550x470")

style1 = ttk.Style()
style1.configure('some.TButton', background='black')

style2 = ttk.Style()
style2.configure('done.TButton', background='black', underline=1)

style3 = ttk.Style()
style3.configure('option.TButton', background='black', width=7)

style4 = ttk.Style()
style4.configure('option1.TButton', background='black', width=9)

style4 = ttk.Style()
style4.configure('dropdown.TMenubutton')

def discord_join():
    webbrowser.open('https://discord.gg/HZcFsmH')

def view_github():
    webbrowser.open('https://github.com/Gloryness/YoutubeDL-GUI')

def donate():
    webbrowser.open('https://streamlabs.com/gloryness/tip')

my_menu = Menu(root)
root.config(menu=my_menu)

file_menu = Menu(my_menu, tearoff=0) # tearoff gets rid of the "- - - - -" at the start
my_menu.add_cascade(label="File", menu=file_menu)

file_menu.add_command(label="Save Settings...", command='')
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

code_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Code", menu=code_menu)
code_menu.add_command(label="View on GitHub", command=view_github)

credits_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Credits", menu=credits_menu)

credits_menu.add_command(label="Made by Gloryness#4341 (discord)")
credits_menu.add_command(label="Join my discord server!", command=discord_join)
credits_menu.add_command(label="Donate to support me!", command=donate)

label1 = Label(root, text="Destination -", bg="#cbdbfc")
label1.grid(row=0, column=0)

destination_var = StringVar()

destination = Entry(root, width=77, state=DISABLED, relief=SOLID, textvariable=destination_var)
destination.grid(row=0, column=1, padx=0, pady=0)

def save_browse_destination():
    if len(file_option.title_var.get()) < 1:
        return '%(title)s'
    else:
        return file_option.title_var.get()


def browse():
    def onbrowse():
        """
        For setting the destination for the download.
        """
        global video_ops
        destination.configure(state=NORMAL)
        get_directory = filedialog.askdirectory(initialdir="R:/Downloaded Videos", title="Destination")
        destination.delete(0, END)
        destination.insert(0, get_directory)

        video_ops.update(outtmpl='{}/{}'.format(destination_var.get(), save_browse_destination()))
        destination.configure(state=DISABLED)
        print(video_ops, end="\n\n")
    browse_thread = threading.Thread(target=onbrowse)
    browse_thread.start()

###########################################################################

browse_btn = ttk.Button(root, text="Browse", style='some.TButton', command=browse)
browse_btn.grid(row=1, columnspan=5)

format_frame = LabelFrame(root, padx=260, bg="#cbdbfc", labelanchor=N, relief=SOLID)
format_frame.grid(row=3, columnspan=5, pady=20, ipady=30)

invis_label = Label(format_frame, text="", bg="#cbdbfc")
invis_label.grid(row=3, column=0)

format_label = Label(root, text="Format", bg="#cbdbfc", fg="blue")
format_label.place(x=242, y=56)

###########################################################################

quality_btn_options = [
    "1080p",
    "1080p",
    "720p",
    "480p",
    "360p",
    "NONE"
]

quality_btn_var = StringVar()
quality_btn_var.set(quality_btn_options[0])

quality_label = Label(root, text="Quality", bg="#cbdbfc", font="Cooper 15")
quality_label.place(x=65, y=71)

quality_btn = ttk.OptionMenu(root, quality_btn_var, *quality_btn_options, style='dropdown.TMenubutton')
quality_btn.place(x=50, y=98, width=90)

###########################################################################

audio_btn_options = [
    "1441k",
    "1441k",
    "800k",
    "467k",
    "258k",
    "NONE"
]

audio_btn_var = StringVar()
audio_btn_var.set(audio_btn_options[0])

audio_label = Label(root, text="Audio", bg="#cbdbfc", font="Cooper 15")
audio_label.place(x=238, y=71)

audio_btn = ttk.OptionMenu(root, audio_btn_var, *audio_btn_options, style='dropdown.TMenubutton')
audio_btn.place(x=220, y=98, width=90)

###########################################################################

ext_btn_options = [
    "MP4",
    "MP4",
    "MP3",
    "MKV",
    "WEBM",
    "WAV",
    "3GP"
]

ext_btn_var = StringVar()
ext_btn_var.set(ext_btn_options[0])

ext_label = Label(root, text="Ext", bg="#cbdbfc", font="Cooper 15")
ext_label.place(x=422, y=71)

ext_btn = ttk.OptionMenu(root, ext_btn_var, *ext_btn_options, style='dropdown.TMenubutton')
ext_btn.place(x=400, y=98, width=90)

###########################################################################

class Updates(object):
    _format = ''

    @staticmethod
    def on_update_video():
        update_video_thread = threading.Thread(target=do.update_video_dict)
        update_video_thread.start()

    @staticmethod
    def on_update_audio():
        update_audio_thread = threading.Thread(target=do.update_audio_dict)
        update_audio_thread.start()

    @staticmethod
    def on_update_both():
        update_both_thread = threading.Thread(target=do.update_both_dict)
        update_both_thread.start()

    @staticmethod
    def on_update_ext():
        update_ext_thread = threading.Thread(target=do.update_ext_dict)
        update_ext_thread.start()


    @classmethod
    def update_video_dict(cls):
        """
        Updates the 'format' option with the required height/width
        """
        global video_ops
        if quality_btn_var.get() == "NONE":
            pass

        else:
            if quality_btn_var.get() == "1080p":
                index = len(quality_btn_var.get()) - 1
                width = quality_btn_var.get()[0:index]
                video_ops.update(format='bestvideo[height<={},width<={}]'.format(int(quality_btn_var.get()[0:index])+20, math.ceil(float(width)*1.777777777777777)))
                cls._format = video_ops.get('format')
            else:
                index = len(quality_btn_var.get()) - 1
                width = quality_btn_var.get()[0:index]
                video_ops.update(format='bestvideo[height<={},width<={}]'.format(quality_btn_var.get()[0:index], math.ceil(float(width)*1.777777777777777)))
                cls._format = video_ops.get('format')
        print(video_ops, "VIDEO", sep="   ", end="\n\n")

    @classmethod
    def update_audio_dict(cls):
        """
        Adds onto the 'format' option with audio, only effective if quality is None.
        """
        global video_ops
        if audio_btn_var.get() == "NONE":
            video_ops.update(extractaudio=False)

        elif quality_btn_var.get() == "NONE":
            index = len(audio_btn_var.get()) - 1
            video_ops.update(zip(['format', 'extractaudio', 'audioformat'],
                                 ['bestaudio/best[abr<={}]'.format(audio_btn_var.get()[0:index]), True, ext_btn_var.get().lower()]))
            cls._format = video_ops.get('format')
        print(video_ops, "AUDIO", sep="   ",  end="\n\n")

    @classmethod
    def update_both_dict(cls):
        """
        Handles both of the formats, as well as MP3's and videos without sound.
        """
        global video_ops
        if quality_btn_var.get() != "NONE" \
            and audio_btn_var.get() != "NONE":
                index = len(audio_btn_var.get()) - 1
                video_ops.update(format=cls._format+'+bestaudio/best[abr<={}]'.format(audio_btn_var.get()[0:index]))
                cls._format = video_ops.get('format')

        elif audio_btn_var.get() == "NONE" \
            and quality_btn_var.get() != "NONE":
                video_ops.update(format=cls._format+'+worstaudio')

        elif audio_btn_var.get() != "NONE" \
            and quality_btn_var.get() == "NONE":
                video_ops.update(postprocessors=[{
                    "key": 'FFmpegExtractAudio',
                    "preferredcodec": '{}'.format(ext_btn_var.get().lower())
                }])

        print(video_ops, "BOTH", sep="   ",  end="\n\n")

    @classmethod
    def update_ext_dict(cls):
        """
        Updates the 'merge_output_format' and 'ext' options, to ensure merge with required format.\n
        If uncompatible, errors will therefore handle it.
        """
        global video_ops
        if quality_btn_var.get() != "NONE" \
            and audio_btn_var.get() != "NONE":
                if ext_btn_var.get() == "3GP":
                    video_ops.update(ext='{}'.format(ext_btn_var.get().lower()), merge_output_format='mkv')
                else:
                    video_ops.update(ext='{}'.format(ext_btn_var.get().lower()), merge_output_format='{}'.format(ext_btn_var.get().lower()))

        elif quality_btn_var.get() == "NONE" \
            and audio_btn_var.get() != "NONE":
                if ext_btn_var.get() == "3GP":
                    video_ops.update(ext='{}'.format(ext_btn_var.get().lower()), merge_output_format='mkv')
                else:
                    video_ops.update(ext='{}'.format(ext_btn_var.get().lower()), merge_output_format='{}'.format(ext_btn_var.get().lower()))

        elif audio_btn_var.get() == "NONE" \
            and quality_btn_var.get() != "NONE":
                if ext_btn_var.get() == "3GP":
                    video_ops.update(ext='{}'.format(ext_btn_var.get().lower()), merge_output_format='mkv')
                else:
                    video_ops.update(ext='{}'.format(ext_btn_var.get().lower()), merge_output_format='{}'.format(ext_btn_var.get().lower()))

        print(video_ops, "EXT", sep="   ", end="\n\n")

    @staticmethod
    def clear_url_box():
        url_box.delete("0.0", END)

    @staticmethod
    def update_format_btns():
        done_btn.configure(state=DISABLED)
        style2.configure('done.TButton', bd=1)
        quality_btn.configure(state=DISABLED)
        audio_btn.configure(state=DISABLED)
        ext_btn.configure(state=DISABLED)

    @staticmethod
    def edit_format_btns():
        confirm = messagebox.askquestion("Are You Sure?", "Would you like to edit your video formats?")
        if confirm == "yes":
            done_btn.configure(state=ACTIVE)
            style2.configure('done.TButton', bd=2)
            quality_btn.configure(state=ACTIVE)
            audio_btn.configure(state=ACTIVE)
            ext_btn.configure(state=ACTIVE)
            do.disable_options()
        else:
            pass

    @staticmethod
    def after_done_btn():
        file_options_btn.configure(state=ACTIVE)
        download_options_btn.configure(state=ACTIVE)
        other_options_btn.configure(state=ACTIVE)
        detect_btn.configure(state=ACTIVE)
        download_btn.configure(state=ACTIVE)
        edit_format.configure(state=ACTIVE)
        url_box.configure(state=NORMAL, bd=4)
        clear_btn.configure(state=ACTIVE)

    @staticmethod
    def disable_options():
        file_options_btn.configure(state=DISABLED)
        download_options_btn.configure(state=DISABLED)
        other_options_btn.configure(state=DISABLED)
        url_box.configure(state=DISABLED, bd=2)
        clear_btn.configure(state=DISABLED)
        detect_btn.configure(state=DISABLED)
        edit_format.configure(state=DISABLED)
        download_btn.configure(state=DISABLED)


do = Updates()

###########################################################################

def done_btn():
    def on_done_btn():
        verify = messagebox.askquestion("Are You Sure?", "This will be your format, are you sure you want to continue?")
        if verify == "yes":

            if quality_btn_var.get() == "NONE" \
                and audio_btn_var.get() == "NONE":
                    none_types = messagebox.showerror("?????", "You have asked for no audio and no quality, therefore cannot continue.")

            elif quality_btn_var.get() == "NONE" \
                and audio_btn_var.get() != "NONE" \
                and ext_btn_var.get() != "MP3" \
                and ext_btn_var.get() != "WAV":
                    none_types2 = messagebox.showerror("?????", "If you want an audio-only file, please use an MP3 or WAV extension.")

            elif quality_btn_var.get() != "NONE" \
                and audio_btn_var.get() != "NONE":
                    if ext_btn_var.get() == "MP3" \
                        or ext_btn_var.get() == "WAV":
                        none_types3 = messagebox.showerror("?????", f"Sorry, but {ext_btn_var.get()} is not a supported file-type for videos.")
                    else:
                        thread_event = threading.Event()

                        do.update_format_btns()
                        do.after_done_btn()

                        thread_event.wait(0.10)
                        do.on_update_video()
                        thread_event.wait(0.10)
                        do.on_update_audio()
                        thread_event.wait(0.10)
                        do.on_update_both()
                        thread_event.wait(0.10)
                        do.on_update_ext()

            elif quality_btn_var.get() != "NONE" \
                and audio_btn_var.get() == "NONE":
                    if ext_btn_var.get() == "MP3" \
                        or ext_btn_var.get() == "WAV":
                        none_types3 = messagebox.showerror("?????", f"Sorry, but {ext_btn_var.get()} is not a supported file-type for videos.")
                    else:
                        thread_event = threading.Event()

                        do.update_format_btns()
                        do.after_done_btn()

                        thread_event.wait(0.10)
                        do.on_update_video()
                        thread_event.wait(0.10)
                        do.on_update_audio()
                        thread_event.wait(0.10)
                        do.on_update_both()
                        thread_event.wait(0.10)
                        do.on_update_ext()

            else:
                thread_event = threading.Event()

                do.update_format_btns()
                do.after_done_btn()

                thread_event.wait(0.10)
                do.on_update_video()
                thread_event.wait(0.10)
                do.on_update_audio()
                thread_event.wait(0.10)
                do.on_update_both()
                thread_event.wait(0.10)
                do.on_update_ext()
        else:
            pass
    done_btn_thread = threading.Thread(target=on_done_btn)
    done_btn_thread.start()

done_btn = ttk.Button(root, text="Done", style='done.TButton', command=done_btn)
done_btn.place(x=228, y=154)

###########################################################################

second_format_frame = LabelFrame(root, padx=260, bg="#cbdbfc", labelanchor=N, relief=SOLID)
second_format_frame.grid(row=6, columnspan=5, pady=35, ipady=40)

second_invis_label = Label(second_format_frame, text="", bg="#cbdbfc")
second_invis_label.grid(row=6, column=0)

second_format_label = Label(root, text="Options", bg="#cbdbfc", fg="blue")
second_format_label.place(x=242, y=197)

file_count = 1
download_count = 1
other_count = 1
_stabalize = [file_count, download_count, other_count]

def reset_window(win):
    global _stabalize
    win.destroy()
    _stabalize[0] = 1
    _stabalize[1] = 1
    _stabalize[2] = 1

class FileOptionWindow(object):
    """
    * Filesystem Options
    """
    def __init__(self):
        self._title = 'Youtube-DL GUI by Gloryness -  v{}'.format(__version__)
        self._icon = 'C:/Users/Gloryness/AppData/Local/atom/app.ico'
        self._size = '600x450'
        self.title_var = StringVar()
        self.title_menu_var = StringVar()

        self.var_1, self.var_2, self.var_3, self.var_4, self.var_5, self.var_6, self.var_7, self.var_8, self.var_9, self.var_10, self.var_11, self.var_12 = \
            StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()

        self.title_entry = None
        self.apply_btn = None
        self.length = []
        self.index = 0

    def on_file_options(self):
        file_options_thread = threading.Thread(target=self.file_options_window)
        file_options_thread.start()

    def file_options_window(self):
        global _stabalize
        if _stabalize[0] == 1:
            global file_win
            file_win = Toplevel()
            file_win.title(self._title)
            file_win.iconbitmap(self._icon)
            file_win.resizable(False, False)
            file_win.configure(bg='#cbdbfc', bd=5)
            file_win.geometry(self._size)
            file_win.protocol("WM_DELETE_WINDOW", lambda: reset_window(file_win))

            border = LabelFrame(file_win, height=425, width=560, bg='#cbdbfc', bd=2, text="Filesystem Options", font="Cooper 18", labelanchor=N, relief=SOLID)
            border.place(x=15, y=7)

            in_border = Frame(file_win, height=380, width=522, bg='#afc2e9')
            in_border.place(x=35, y=36)

            title_label = Label(file_win, text="Title:", font='Cooper 14', bg='#afc2e9')
            title_label.place(x=40, y=40)

            self.title_entry = Entry(file_win, width=74, state=NORMAL, relief=SOLID, textvariable=self.title_var)
            self.title_entry.place(x=90, y=45)
            if not self.title_var.get().startswith('%(title)s'):
                self.title_entry.insert(0, '%(title)s')
            else:
                pass
            self.title_entry.configure(state=DISABLED)

            title_options = [
                "id",                  "id",
                "title",                "ext",
                "uploader",                "upload_date",
                "channel",                "duration",
                "view_count",                "like_count",
                "dislike_count",                "is_live",
                "playlist",                "playlist_title",
                "chapter",                "series",
                "season",                "episode",
                "track",                "artist",
                "genre",                "album"
            ]
            self.title_menu_var.set(title_options[1])

            file_name_menu = ttk.OptionMenu(file_win, self.title_menu_var, *title_options, style='dropdown.TMenubutton')
            file_name_menu.place(x=90, y=75, width=110)

            add_outtmpl = ttk.Button(file_win, text="ADD", style='option1.TButton', command=self.__add__)
            add_outtmpl.place(x=230, y=75)

            remove_outtmpl = ttk.Button(file_win, text="REMOVE", style='option1.TButton', command=self.__delete__)
            remove_outtmpl.place(x=300, y=75)


            exit_btn = ttk.Button(file_win, text="Exit", style='option.TButton', command=lambda: reset_window(file_win))
            exit_btn.place(x=420, y=386)

            self.apply_btn = ttk.Button(file_win, text="Apply", state=ACTIVE, style='option.TButton', command=self.file_apply)
            self.apply_btn.place(x=490, y=386)
            style = ttk.Style()
            style.configure('TCheckbutton', background='#afc2e9')

            check_1 = ttk.Checkbutton(file_win, text="Write video description to a .description file.", variable=self.var_1, onvalue="True", offvalue="False", style='TCheckbutton', command=self.update_apply_btn)
            check_1.place(x=40, y=120)

            check_2 = ttk.Checkbutton(file_win, text="Write video description to a .info.json file.", variable=self.var_2, onvalue="True", offvalue="False", style='TCheckbutton', command=self.update_apply_btn)
            check_2.place(x=40, y=150)

            check_3 = ttk.Checkbutton(file_win, text="Write video annotations to a .annotations.xml file.", variable=self.var_3, onvalue="True", offvalue="False", style='TCheckbutton', command=self.update_apply_btn)
            check_3.place(x=40, y=180)

            check_4 = ttk.Checkbutton(file_win, text="Write the thumbnail image to a file.", variable=self.var_4, onvalue="True", offvalue="False", style='TCheckbutton', command=self.update_apply_btn)
            check_4.place(x=40, y=210)

            check_5 = ttk.Checkbutton(file_win, text="Write all thumbnail formats to files.", variable=self.var_5, onvalue="True", offvalue="False", style='TCheckbutton', command=self.update_apply_btn)
            check_5.place(x=40, y=240)

            check_6 = ttk.Checkbutton(file_win, text="Write the video subtitles to a file.", variable=self.var_6, onvalue="True", offvalue="False", style='TCheckbutton', command=self.update_apply_btn)
            check_6.place(x=40, y=270)

            check_7 = ttk.Checkbutton(file_win, text="Write the automatically generated subtitles \nto a file.", variable=self.var_7, onvalue="True", offvalue="False", style='TCheckbutton', command=self.update_apply_btn)
            check_7.place(x=304, y=110)

            check_8 = ttk.Checkbutton(file_win, text="Lists all available subtitles for the video.", variable=self.var_8, onvalue="True", offvalue="False", style='TCheckbutton', command=self.update_apply_btn)
            check_8.place(x=304, y=150)

            check_9 = ttk.Checkbutton(file_win, text="Enable / Disable filesystem caching", variable=self.var_9, onvalue="True", offvalue="False", style='TCheckbutton', command=self.update_apply_btn)
            check_9.place(x=304, y=180)

            check_10 = ttk.Checkbutton(file_win, text="Overwrite files", variable=self.var_10, onvalue="True", offvalue="False", style='TCheckbutton', command=self.update_apply_btn)
            check_10.place(x=304, y=210)

            check_11 = ttk.Checkbutton(file_win, text="Restrict filenames\n(do not allow spaces and '&')", variable=self.var_11, onvalue="True", offvalue="False", style='TCheckbutton', command=self.update_apply_btn)
            check_11.place(x=304, y=235)

            style_1 = ttk.Style()
            style_1.configure('TLabel', background='#afc2e9')

            cookie_label = ttk.Label(file_win, text="Where cookies should be read from and dumpted to", style='TLabel')
            cookie_label.place(x=270, y=275)

            style_2 = ttk.Style()
            style_2.configure('TEntry', relief=SOLID, borderwidth=2)

            cookie_entry = BorderedEntry(file_win, state=DISABLED, textvariable=self.var_12, style='TEntry', width=40, bordercolor="black")
            cookie_entry.place(x=280, y=295)

            def browse():
                self.update_apply_btn()
                cookie_browse = filedialog.askopenfilename(initialdir="C:/", title="Destination For Cookies", filetypes=(("all files", "*.*"), ("txt files", "*.txt")))
                cookie_entry.configure(state=NORMAL)
                cookie_entry.delete(0, END)
                cookie_entry.insert(0, cookie_browse)
                cookie_entry.configure(state=DISABLED)

            def clear_text():
                cookie_entry.configure(state=NORMAL)
                cookie_entry.delete(0, END)
                cookie_entry.configure(state=DISABLED)

            cookie_button = ttk.Button(file_win, text="Browse", style='some.TButton', command=browse)
            cookie_button.place(x=360, y=320)
            global clear_img
            clear_img = ImageTk.PhotoImage(Image.open('delete_28px.png'))
            clearbtn = Button(file_win, image=clear_img, command=clear_text)
            clearbtn.place(x=530, y=294)



            index = 0
            for i in range(3):
                _stabalize[index] += 1
                index += 1
            index = 0
            print(_stabalize)
        else:
            pass

    def __add__(self):
        self.apply_btn.configure(state=ACTIVE)
        self.title_entry.configure(state=NORMAL)
        self.title_entry.insert(END, ".%(" + self.title_menu_var.get() + ")s")
        self.length.append(str(".%(" + self.title_menu_var.get() + ")s"))
        self.title_entry.configure(state=DISABLED)
        print(self.length)

    def __delete__(self):
        self.apply_btn.configure(state=ACTIVE)
        try:
            self.index = len(self.length) - 1
            self.title_entry.configure(state=NORMAL)
            self.title_entry.delete(len(self.title_var.get()) - len(self.length[self.index]), END)
            self.title_entry.configure(state=DISABLED)
            self.length.pop(self.index)
            print(self.length)
        except IndexError:
            self.length.clear()
            self.title_entry.configure(state=DISABLED)

    def update_apply_btn(self):
        self.apply_btn.configure(state=ACTIVE)

    def file_apply(self):
        global video_ops
        self.apply_btn.configure(state=DISABLED)
        video_ops.update(outtmpl=f"{destination_var.get()}/{self.title_var.get()}")

        if self.var_1.get() == "True":
            video_ops.update(writedescription=True)
        else:
            video_ops.update(writedescription=False)

        if self.var_2.get() == "True":
            video_ops.update(writeinfojson=True)
        else:
            video_ops.update(writeinfojson=False)

        if self.var_3.get() == "True":
            video_ops.update(writeannotations=True)
        else:
            video_ops.update(writeannotations=False)

        if self.var_4.get() == "True":
            video_ops.update(writethumbnail=True)
        else:
            video_ops.update(writethumbnail=False)

        if self.var_5.get() == "True":
            video_ops.update(write_all_thumbnails=True)
        else:
            video_ops.update(write_all_thumbnails=False)

        if self.var_6.get() == "True":
            video_ops.update(writesubtitles=True)
        else:
            video_ops.update(writesubtitles=False)

        if self.var_7.get() == "True":
            video_ops.update(writeautomaticsub=True)
        else:
            video_ops.update(writeautomaticsub=False)

        if self.var_8.get() == "True":
            video_ops.update(listsubtitles=True)
        else:
            video_ops.update(listsubtitles=False)

        if self.var_9.get() == "True":
            video_ops.update(cachedir='~/.cache/youtube-dl')
        else:
            video_ops.update(cachedir=False)

        if self.var_10.get() == "True":
            video_ops.update(nooverwrites=False)
        else:
            video_ops.update(nooverwrites=True)

        if self.var_11.get() == "True":
            video_ops.update(restrictfilenames=True)
        else:
            video_ops.update(restrictfilenames=False)

        if len(self.var_12.get()) <= 2:
            pass
        else:
            video_ops.update(cookiefile=self.var_12.get())

        print(video_ops, "FILE OPTIONS", sep="   ", end="\n\n")


class DownloadOptionWindow(object):
    """
    * Download Options
    """
    def __init__(self):
        self._title = 'Youtube-DL GUI by Gloryness -  v{}'.format(__version__)
        self._icon = 'C:/Users/Gloryness/AppData/Local/atom/app.ico'
        self._size = '600x450'
        self.apply_btn = None

    def on_download_options(self):
        download_options_thread = threading.Thread(target=self.download_options_window)
        download_options_thread.start()

    def download_options_window(self):
        global _stabalize
        if _stabalize[2] == 1:
            global download_win
            download_win = Toplevel()
            download_win.title(self._title)
            download_win.iconbitmap(self._icon)
            download_win.resizable(False, False)
            download_win.configure(bg='#cbdbfc', bd=5)
            download_win.geometry(self._size)
            download_win.protocol("WM_DELETE_WINDOW", lambda: reset_window(download_win))

            border = LabelFrame(download_win, height=425, width=560, bg='#cbdbfc', bd=2, text="Download Options",
                                font="Cooper 18", labelanchor=N, relief=SOLID)
            border.place(x=15, y=7)

            # stuff go here

            index = 0
            for i in range(3):
                _stabalize[index] += 1
                index += 1
            index = 0
            print(_stabalize)
        else:
            pass



class OtherOptionWindow(object):
    """
    * Other Options
    """
    def __init__(self):
        self._title = 'Youtube-DL GUI by Gloryness -  v{}'.format(__version__)
        self._icon = 'C:/Users/Gloryness/AppData/Local/atom/app.ico'
        self._size = '600x450'
        self.apply_btn = None

    def on_other_options(self):
        other_options_thread = threading.Thread(target=self.other_options_window)
        other_options_thread.start()

    def other_options_window(self):
        global _stabalize
        if _stabalize[1] == 1:
            global other_win
            other_win = Toplevel()
            other_win.title(self._title)
            other_win.iconbitmap(self._icon)
            other_win.resizable(False, False)
            other_win.configure(bg='#cbdbfc', bd=5)
            other_win.geometry(self._size)
            other_win.protocol("WM_DELETE_WINDOW", lambda: reset_window(other_win))

            border = LabelFrame(other_win, height=425, width=560, bg='#cbdbfc', bd=2, text="Other Options",
                                font="Cooper 18", labelanchor=N, relief=SOLID)
            border.place(x=15, y=7)

            # stuff go here

            index = 0
            for i in range(3):
                _stabalize[index] += 1
                index += 1
            index = 0
            print(_stabalize)

        else:
            pass


file_option = FileOptionWindow()
download_option = DownloadOptionWindow()
other_option = OtherOptionWindow()

### OPTION 1

file_option_label = Label(root, text="File Options", bg="#cbdbfc", font="Cooper 14")
file_option_label.place(x=42, y=221)

file_options_btn = ttk.Button(root, text="Click Me", state=DISABLED, style='some.TButton', command=file_option.on_file_options)
file_options_btn.place(x=50, y=248, width=90)

### OPTION 2

download_option_label = Label(root, text="Download Options", bg="#cbdbfc", font="Cooper 14")
download_option_label.place(x=184, y=221)

download_options_btn = ttk.Button(root, text="Click Me", state=DISABLED, style='some.TButton', command=download_option.on_download_options)
download_options_btn.place(x=220, y=248, width=90)

### OPTION 3

other_options_label = Label(root, text="Other Options", bg="#cbdbfc", font="Cooper 14")
other_options_label.place(x=380, y=221)

other_options_btn = ttk.Button(root, text="Click Me", state=DISABLED, style='some.TButton', command=other_option.on_other_options)
other_options_btn.place(x=400, y=248, width=90)

###########################################################################

url_box = scrolledtext.ScrolledText(root, height=6, width=56, bd=2, state=DISABLED, font='Cooper 9')
url_box.place(x=5, y=340)


class StdDirector(object):
    """
    How it puts the output into the text box
    """

    def __init__(self, output):
        self.output = output

    def write(self, string):
        self.output.config(state=NORMAL)
        self.output.insert("end", string)
        self.output.see("end")
        self.output.config(state=DISABLED)


class CoreGUI(object):
    """
    Creating the text box for output and redirecting the stdout and stderr to text box

    Also to create the kill opertion
    """

    def __init__(self, parent):
        self.count = 1

        self.text_box = scrolledtext.ScrolledText(parent, state=DISABLED, height=25, width=80, bd=4, font='Cooper 9', bg='#cbdbfc')
        self.text_box.place(x=0, y=0)

        sys.stdout = StdDirector(self.text_box)
        sys.stderr = StdDirector(self.text_box)

    def undo(self):
        sys.stdout = StdDirector(self.text_box)
        sys.stderr = StdDirector(self.text_box)


class DownloadConversion(object):
    """
    Needs threading otherwise errors will occur, and multiple freezes.

    This class deals with selenium, conversion, text box and the downloading.
    """

    def __init__(self):
        self._index = 0
        self.win_count = 1
        self.terminate_count = 1
        self._driver = None
        self.output_win = None
        self.new_win_thread = None
        self.window_thread = None
        self.terminate_thread = None
        self.download_thread = None
        self.selenium_thread = None
        self.get_urls_thread = None

    _downloadError = yt.utils.DownloadError
    _FFmpegPostProcessorError = postprocessor.ffmpeg.FFmpegPostProcessorError

    def reset_count(self, win):
        win.destroy()
        edit_format.configure(state=ACTIVE)
        self.win_count = 1
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def reset_countV2(self, win):
        win.destroy()
        edit_format.configure(state=ACTIVE)
        self.win_count = 1

    def new_win(self):
        if self.win_count == 1:
            self.output_win = Toplevel()
            self.output_win.title("Youtube-DL GUI by Gloryness -  v{}".format(__version__))
            self.output_win.iconbitmap('C:/Users/Gloryness/AppData/Local/atom/app.ico')
            self.output_win.resizable(False, False)
            self.output_win.configure(bg='#badbfc', bd=5)
            self.output_win.geometry("600x400")
            self.output_win.protocol("WM_DELETE_WINDOW", lambda: self.reset_count(self.output_win))

            self.win_count = 2
            CoreGUI(self.output_win)
        else:
            pass

    def quit_win(self):
        self.output_win.after(2400, lambda: self.reset_count(self.output_win))

    def short_quit_win(self):
        self.output_win.after(1700, lambda: self.reset_count(self.output_win))

    def undo(self):
        t = CoreGUI(self.output_win)
        sys.stdout = StdDirector(t.undo())
        sys.stderr = StdDirector(t.undo())

    def kill_button(self):
        edit_format.configure(state=DISABLED)
        kill_button = ttk.Button(self.output_win, text="   Kill Operation   ", state=ACTIVE, style='some.TButton', command=self.terminate_download)
        kill_button.place(x=455, y=356)

    def terminate_download(self):
        self.output_win.after(250, lambda: self.reset_countV2(self.output_win))

    def window(self):
        self.on_new_win()
        timeout = threading.Event()
        timeout.wait(0.90)
        self.output_win.after(200, self.on_download)

    @staticmethod
    def my_hook(d):
        if d['status'] == 'finished':
            print('Done downloading, now converting ...')

    @classmethod
    def download(cls):

        """
        Mainly handles the errors, aswell as the downloading.
        """
        index = 0
        video_download = 1
        _url = url_box.get("1.0", END).split()
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        print(_url)
        download_call.undo()
        video_ops.update(logger=MyLogger(),
                         progress_hooks=[download_call.my_hook])

        with yt.YoutubeDL(video_ops) as ydl:
            try:

                if len(_url) < 1:
                    print("You must enter a URL")
                    download_call.short_quit_win()

                elif not _url[0].startswith('https://'):
                    print("You must enter a VALID URL")
                    download_call.short_quit_win()

                elif ext_btn_var.get() == "WAV":
                    download_call.kill_button()
                    raise cls._downloadError("without this, will cause a bug - unknown why.")

                elif len(_url) == 1:
                    download_call.kill_button()
                    if quality_btn_var.get() != "NONE" \
                        and audio_btn_var.get() == "NONE":
                            ydl.download([_url[0]])
                            extract7 = ydl.extract_info(_url[0], download=False)
                            time.sleep(1)
                            subprocess.call('ffmpeg' + ' -i "' + destination_var.get() + '/' + extract7['title'] + '".' + ext_btn_var.get().lower() + ' -an -y -preset fast "'
                                            + destination_var.get() + '/' + extract7['title'] + 'V2"' + '.' + ext_btn_var.get().lower(), shell=False)
                            os.remove(destination_var.get() + '/' + extract7['title'] + '.' + extract7['ext'])

                    else:
                        download_call.kill_button()
                        ydl.download([_url[0]])
                        t = threading.Event()
                        t.wait(1.5)

                elif len(_url) > 1:
                    download_call.kill_button()
                    if quality_btn_var.get() != "NONE" \
                        and audio_btn_var.get() == "NONE":
                        index = 0
                        for i in range(len(list(_url))):
                            thread = threading.Event()
                            thread.wait(1.75)
                            ydl.download([_url[index]])
                            extract5 = ydl.extract_info(_url[0], download=False)
                            time.sleep(1)
                            subprocess.call('ffmpeg' + ' -i "' + destination_var.get() + '/' + extract5['title'] + '".' + ext_btn_var.get().lower() + ' -an -y -preset fast "'
                                            + destination_var.get() + '/' + extract5['title'] + 'V2"' + '.' + ext_btn_var.get().lower(), shell=False)
                            _url.pop(index)
                            os.remove(destination_var.get() + '/' + extract5['title'] + '.' + extract5['ext'])
                            print("\nDownload [{}] completed\n".format(video_download))
                            video_download += 1
                        video_download = 1
                        download_call.quit_win()
                    else:
                        download_call.kill_button()
                        for i in range(len(list(_url))):
                            thread = threading.Event()
                            thread.wait(1.75)
                            ydl.download([_url[index]])
                            _url.pop(index)
                            print("\nDownload [{}] completed\n".format(video_download))
                            video_download += 1
                        video_download = 1
                        download_call.quit_win()


            except yt.utils.DownloadError or postprocessor.ffmpeg.FFmpegPostProcessorError or Exception:
                logger.exception(msg='\n{} was unable to convert to {} due to no available formats.\n'
                           .format(_url[0], video_ops.get('merge_output_format')))
                t = threading.Event()
                t.wait(1)
                print("Sorry, but we could not download the requested format {}!\nThe video will be merged into a more suitable format instead. Such as MKV."
                      .format(ext_btn_var.get().lower()))
                t.wait(1.75)

                if quality_btn_var.get() != "NONE" \
                    and audio_btn_var.get() != "NONE":
                        video_ops.update(merge_output_format='mkv', nooverwrites=False)
                        with yt.YoutubeDL(video_ops) as ytd:
                            try:
                                if len(_url) == 1:
                                    ytd.download([_url[0]])
                                if len(_url) > 1:
                                    for i in range(len(list(_url))):
                                        thread = threading.Event()
                                        thread.wait(1.75)
                                        ytd.download([_url[index]])
                                        _url.pop(index)
                                        print("\nDownload [{}] completed\n".format(video_download))
                                        video_download += 1
                                    video_download = 1
                                    download_call.quit_win()

                            except cls._downloadError or cls._FFmpegPostProcessorError or Exception:
                                logger.exception(level=logging.WARNING, msg='\n{} was unable to convert to {} due to no available formats.\n'
                                           .format(_url[0], video_ops.get('merge_output_format')))
                                video_ops.pop('merge_output_format')
                                video_ops.update(nooverwrites=False, ext='{}'.format(ext_btn_var.get().lower()))
                                with yt.YoutubeDL(video_ops) as ytk:
                                    try:
                                        if len(_url) == 1:
                                            ytd.download([_url[0]])
                                        if len(_url) > 1:
                                            for i in range(len(list(_url))):
                                                thread = threading.Event()
                                                thread.wait(1.75)
                                                ytd.download([_url[index]])
                                                _url.pop(index)
                                                print("\nDownload [{}] completed\n".format(video_download))
                                                video_download += 1
                                            video_download = 1
                                            download_call.quit_win()
                                    except Exception as exc:
                                        logger.exception('\nCRITICAL : an error occured and was unable to merge... error: %s\n' % exc)
                                        download_call.quit_win()

                                    finally:
                                        print("\nDownload COMPLETE!\n")
                                        download_call.quit_win()
                            finally:
                                print("\nDownload COMPLETE!\n")
                                download_call.quit_win()

                elif quality_btn_var.get() == "NONE" \
                    and audio_btn_var.get() != "NONE":
                        if ext_btn_var.get() == ext_btn_options[2]:
                            video_ops.update(postprocessors=[{
                                "key": 'FFmpegExtractAudio',
                                "preferredcodec": 'mp3'
                                }], nooverwrites=False)
                            with yt.YoutubeDL(video_ops) as ytd:
                                try:
                                    if len(_url) == 1:
                                        ytd.download([_url[0]])
                                    if len(_url) > 1:
                                        for i in range(len(list(_url))):
                                            thread = threading.Event()
                                            thread.wait(1.75)
                                            ytd.download([_url[index]])
                                            _url.pop(index)
                                            print("\nDownload [{}] completed\n".format(video_download))
                                            video_download += 1
                                        video_download = 1
                                        download_call.quit_win()
                                except cls._downloadError or cls._FFmpegPostProcessorError or Exception:
                                    logger.exception(msg='\n{} was unable to convert to {} due to no available formats.\n'
                                               .format(_url[0], video_ops.get('merge_output_format')))
                                    video_ops.update(postprocessors=[{
                                        "key": 'FFmpegExtractAudio',
                                        "preferredcodec": 'wav'
                                    }], nooverwrites=False, ext='{}'.format(ext_btn_var.get().lower()))
                                    with yt.YoutubeDL(video_ops) as ytk:
                                        try:
                                            if len(_url) == 1:
                                                ytk.download([_url[0]])
                                            if len(_url) > 1:
                                                for i in range(len(list(_url))):
                                                    thread = threading.Event()
                                                    thread.wait(1.75)
                                                    ytk.download([_url[index]])
                                                    _url.pop(index)
                                                    print("\nDownload [{}] completed\n".format(video_download))
                                                    video_download += 1
                                                video_download = 1
                                                download_call.quit_win()
                                        except Exception as exc:
                                            logger.exception(msg='\nCRITICAL : an error occured and was unable to merge/download... error: %s\n' % exc)
                                            download_call.quit_win()

                                        finally:
                                            print("\nDownload COMPLETE!\n")
                                            download_call.quit_win()
                                finally:
                                    print("\nDownload COMPLETE!\n")
                                    download_call.quit_win()

                        elif ext_btn_var.get() == ext_btn_options[5]:
                            video_ops.update(postprocessors=[{
                                "key": 'FFmpegExtractAudio',
                                "preferredcodec": 'wav'
                            }], nooverwrites=False)
                            with yt.YoutubeDL(video_ops) as ytd:
                                try:
                                    if len(_url) == 1:
                                        ytd.download([_url[0]])
                                    if len(_url) > 1:
                                        for i in range(len(list(_url))):
                                            thread = threading.Event()
                                            thread.wait(1.75)
                                            ytd.download([_url[index]])
                                            _url.pop(index)
                                            print("\nDownload [{}] completed\n".format(video_download))
                                            video_download += 1
                                        video_download = 1
                                        download_call.quit_win()
                                except cls._downloadError or cls._FFmpegPostProcessorError or Exception:
                                    logger.exception(msg='\n{} was unable to convert to {} due to no available formats.\n'
                                               .format(_url[0], video_ops.get('merge_output_format')))
                                    video_ops.update(postprocessors=[{
                                        "key": 'FFmpegExtractAudio',
                                        "preferredcodec": 'mp3'
                                    }], nooverwrites=False, ext='{}'.format(ext_btn_var.get().lower()))
                                    with yt.YoutubeDL(video_ops) as ytk:
                                        try:
                                            if len(_url) == 1:
                                                ytk.download([_url[0]])
                                            if len(_url) > 1:
                                                for i in range(len(list(_url))):
                                                    thread = threading.Event()
                                                    thread.wait(1.75)
                                                    ytk.download([_url[index]])
                                                    _url.pop(index)
                                                    print("\nDownload [{}] completed\n".format(video_download))
                                                    video_download += 1
                                                video_download = 1
                                        except Exception as exc:
                                            logger.exception(msg='\nCRITICAL : an error occured and was unable to merge/download... error: %s\n' % exc)
                                            download_call.quit_win()

                                        finally:
                                            print("\nDownload COMPLETE!\n")
                                            download_call.quit_win()
                                finally:
                                    print("\nDownload COMPLETE!\n")
                                    download_call.quit_win()

                elif audio_btn_var.get() == "NONE" \
                    and quality_btn_var.get() != "NONE":
                        video_ops.update(merge_output_format='mkv', nooverwrites=False, ext='mkv')
                        with yt.YoutubeDL(video_ops) as ytd:
                            try:
                                if len(_url) == 1:
                                    ytd.download([_url[0]])
                                    extract1 = ytd.extract_info(_url[0], download=False)
                                    time.sleep(1)
                                    subprocess.call('ffmpeg' + ' -i "' + destination_var.get() + '/' + extract1['title'] + '".mkv'
                                                    + ' -an -y -preset fast "'
                                                    + destination_var.get() + '/' + extract1['title'] + 'V2"' + '.mkv', shell=False)
                                    os.remove(destination_var.get() + '/' + extract1['title'] + '.mkv')
                                if len(_url) > 1:
                                    for i in range(len(list(_url))):
                                        thread = threading.Event()
                                        thread.wait(1.75)
                                        ytd.download([_url[index]])
                                        extract2 = ytd.extract_info(_url[0], download=False)
                                        time.sleep(1)
                                        subprocess.call('ffmpeg' + ' -i "' + destination_var.get() + '/' + extract2['title'] + '".mkv'
                                                        + ' -an -y -preset fast "'
                                                        + destination_var.get() + '/' + extract2['title'] + 'V2"' + '.mkv', shell=False)
                                        _url.pop(index)
                                        os.remove(destination_var.get() + '/' + extract2['title'] + '.mkv')
                                        print("\nDownload [{}] completed\n".format(video_download))
                                        video_download += 1
                                    video_download = 1
                                    download_call.quit_win()

                            except cls._downloadError or cls._FFmpegPostProcessorError or Exception:
                                logger.exception(msg='\n{} was unable to convert to {} due to no available formats.\n'
                                           .format(_url[0], video_ops.get('merge_output_format')))
                                video_ops.pop('merge_output_format')
                                extract = ydl.extract_info(_url[0], download=False)
                                video_ops.update(nooverwrites=False)
                                video_ops.pop('ext')
                                with yt.YoutubeDL(video_ops) as ytk:
                                    try:
                                        if len(_url) == 1:
                                            ytk.download([_url[0]])
                                            extract4 = ytk.extract_info(_url[0], download=False)
                                            time.sleep(1)
                                            subprocess.call('ffmpeg' + ' -i "' + destination_var.get() + '/' + extract4['title'] + '.' + extract4['ext']
                                                            + '" -an -y -preset fast "'
                                                            + destination_var.get() + '/' + extract4['title'] + 'V2"' + '.' + extract4['ext'], shell=False)
                                            os.remove(destination_var.get() + '/' + extract4['title'] + '.' + extract4['ext'])
                                        if len(_url) > 1:
                                            for i in range(len(list(_url))):
                                                thread = threading.Event()
                                                thread.wait(1.75)
                                                ytk.download([_url[index]])
                                                video_ops.update(outtmpl=destination_var.get() + '/%(title)s.%(ext)s')
                                                extract3 = ytk.extract_info(_url[0], download=False)
                                                time.sleep(1)
                                                subprocess.call('ffmpeg' + ' -i "' + destination_var.get() + '/' + extract3['title'] + '.' + extract3['ext']
                                                    + '" -an -y -preset fast "'
                                                    + destination_var.get() + '/' + extract3['title'] + 'V2"' + '.' + extract3['ext'], shell=False)
                                                _url.pop(index)
                                                os.remove(destination_var.get() + '/' + extract3['title'] + '.' + extract3['ext']) # Delete the orignal file w/ sound
                                                print("\nDownload [{}] completed\n".format(video_download))
                                                video_download += 1
                                            video_download = 1
                                            download_call.quit_win()

                                    except Exception as exc:
                                        logger.exception(msg='\nCRITICAL : an error occured and was unable to merge/download... error: %s\n' % exc)
                                        download_call.quit_win()

                                    finally:
                                        print("\nDownload COMPLETE!\n")
                                        download_call.quit_win()
                            finally:
                                print("\nDownload COMPLETE!\n")
                                download_call.quit_win()
            finally:
                if len(_url) < 1:
                    pass
                elif not _url[0].startswith('https://'):
                    pass
                else:
                    print("\nDownload COMPLETE!\n")
                    download_call.quit_win()

    def open_selenium(self):
        """
        A fun feature to use when your browsing youtube.
        """
        confirm = messagebox.askyesnocancel("Execute URLS / Open Selenium", "Please make sure that you've configured the 'Settings' "
                                            "to make sure you have the required WebDriver location + Browser"
                                            "\n\nWould you like to OPEN Selenium / Execute URLS / Cancel"
                                            "\nYES - Open Browser via Selenium"
                                            "\nNO - Execute URLS from Selenium"
                                            "\nCANCEL - Cancel")
        if confirm is True:
            try:
                self._driver = webdriver.Firefox(executable_path=PATH)
                self._driver.get('https://www.youtube.com/')
                self._driver.maximize_window()
            except Exception as exc:
                logger.log(level=logging.ERROR, msg="An error occured: %s" % exc)
        elif confirm is False:
            download_call.on_get_urls()
        else:
            pass

    def get_urls(self):
        try:
            self._index = 0
            self._driver.switch_to.window(self._driver.window_handles[self._index])

            for i in range(len(self._driver.window_handles)):
                if str(self._driver.current_url).startswith('https://www.youtube.com/watch?v='):
                    url_box.insert("1.0", self._driver.current_url + "\n")
                    self._index += 1
                try:
                    self._driver.switch_to.window(self._driver.window_handles[self._index])
                except IndexError:
                    pass
            self._index = 0
            self._driver.switch_to.window(self._driver.window_handles[self._index])
        except AttributeError as exc:
            url_box.delete("1.0", END)
            url_box.insert("1.0", "Selenium is not open, therefore no URLS detected.")
            logger.exception("Not able to detect Selenium. error: %s" % exc)

        except WebDriverException as exc:
            url_box.delete("1.0", END)
            url_box.insert("1.0", "Selenium is not open, therefore no URLS detected.")
            logger.exception("Selenium was not able to detect any valid URLS. error: %s" % exc)

        except Exception as exc:
            url_box.delete("1.0", END)
            url_box.insert("1.0", "Selenium is not open, therefore no URLS detected.")
            logger.exception("Selenium was not able to detect any valid URLS. error: %s" % exc)

    def on_new_win(self):
        self.new_win_thread = threading.Thread(target=self.new_win)
        self.new_win_thread.start()

    def on_window(self):
        self.window_thread = threading.Thread(target=self.window)
        self.window_thread.start()

    def on_download(self):
        self.download_thread = threading.Thread(target=self.download)
        self.download_thread.start()

    def on_selenium(self):
        self.selenium_thread = threading.Thread(target=self.open_selenium)
        self.selenium_thread.start()

    def on_get_urls(self):
        self.get_urls_thread = threading.Thread(target=self.get_urls)
        self.get_urls_thread.start()


class MyLogger(object):

    @staticmethod
    def debug(msg):
        now = threading.Event()
        now.wait(0.30)
        print(msg)

    @staticmethod
    def warning(msg):
        now = threading.Event()
        now.wait(0.30)
        print(msg)

    @staticmethod
    def error(msg):
        now = threading.Event()
        now.wait(0.30)
        print(msg)
        logger.exception(msg="ERROR : {}".format(msg))


download_call = DownloadConversion()

download_btn = ttk.Button(root, text="      Download      ", style='some.TButton', state=DISABLED, command=download_call.on_window)
download_btn.place(x=435, y=410)

edit_format = ttk.Button(root, text="    Edit Formats    ", style='some.TButton', state=DISABLED, command=do.edit_format_btns)
edit_format.place(x=435, y=375)

detect_btn = ttk.Button(root, text="     Detect URLS    ", style='some.TButton', state=DISABLED, command=download_call.on_selenium)
detect_btn.place(x=435, y=340)

clear_btn = ttk.Button(root, text="    Clear    ", style='some.TButton', state=DISABLED, command=do.clear_url_box)
clear_btn.place(x=8, y=314)

detect_info_label = Label(root, text="(selenium-use-only)", bg='#cbdbfc', font='Cooper 10')
detect_info_label.place(x=425, y=318)

info = Label(root, text="Enter URLS (new line each)", bg='#cbdbfc', font='Cooper 10')
info.place(x=170, y=315)

## Videos
video_ops = {
}

mainloop()
