from __future__ import unicode_literals

from valid_extractors import AllExtractors
from install_ffmpeg import InstallFFmpeg
from install_webdriver import InstallWebDriver
from update import SendRequest
from settings_window import SettingsWindow
from help_window import Help

from _tkinter import TclError
from tkinter import *
from tkinter import messagebox, filedialog, scrolledtext
from tkinter import ttk

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from cryptography.fernet import Fernet

import youtube_dl as yt
from youtube_dl import postprocessor
from PIL import ImageTk, Image
import math
import string
import json
import subprocess
import os
import sys

import threading
import logging
import webbrowser

__version__ = '1.0.6'

## Main Dictionary
video_ops = {
}

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s--%(name)s--%(message)s')

file_handler = logging.FileHandler('downloading.log')
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)

file_handler1 = logging.FileHandler('downloading.log')
file_handler1.setLevel(logging.CRITICAL)
file_handler1.setFormatter(formatter)

file_handler2 = logging.FileHandler('downloading.log')
file_handler2.setLevel(logging.WARNING)
file_handler2.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(file_handler1)
logger.addHandler(file_handler2)
logger.addHandler(stream_handler)

root = Tk()
root.title("Youtube-DL GUI   |   Gloryness  |  v{}".format(__version__))
root.iconbitmap('images/#app.ico')
root.resizable(False, False)
root.configure(bg='#cbdbfc', bd=5)
root.geometry("550x470")

style1 = ttk.Style()
style1.configure('some.TButton', background='black')

style1.configure('done.TButton', background='black', underline=1)

style1.configure('option.TButton', background='black', width=7)

style1.configure('option1.TButton', background='black', width=9)

style1.configure('dropdown.TMenubutton')

all_extractors = AllExtractors()

wait_time = 1.75

def discord_join():
    webbrowser.open('https://discord.gg/HZcFsmH')

def view_github():
    webbrowser.open('https://github.com/Gloryness/YoutubeDL-GUI')

def donate():
    webbrowser.open('https://streamlabs.com/gloryness/tip')

FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
def explore(path):
    # explorer would choke on forward slashes
    path = os.path.normpath(path)

    if os.path.isdir(path):
        subprocess.run([FILEBROWSER_PATH, path])
    elif os.path.isfile(path):
        subprocess.run([FILEBROWSER_PATH, '/select,', os.path.normpath(path)])

def go_to():
    if len(destination_var.get()) <= 1:
        messagebox.showwarning("???", "There is no folder to jump to since your 'Destination' is not set", parent=root)
    else:
        destination2 = destination_var.get().replace("\\", "/")
        explore(destination2 + "/")

my_menu = Menu(root)
root.config(menu=my_menu)

file_menu = Menu(my_menu, tearoff=0) # tearoff gets rid of the "- - - - -" at the start
my_menu.add_cascade(label="File", menu=file_menu)

def init_settings():
    global setting
    setting = SettingsWindow(__version__, download_btn, done_btn, _stabalize)

def settings():
    setting.on_settings()

file_menu.add_command(label="Settings", command=settings)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

tools_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Tools", menu=tools_menu)

def installffmpeg():
    ffmpeg = InstallFFmpeg(__version__)
    ffmpeg.on_ffmpeg_window()

def installwebdriver():
    web = InstallWebDriver(__version__)
    web.on_webdriver_window()

def updategui():
    req = SendRequest(__version__)
    req.on_send_request()

def request_help(topic):
    help_ = Help(__version__)
    if topic == "ffmpeg":
        help_.ffmpeg_thread()
    elif topic == "urls":
        help_.detect_urls_thread()
    elif topic == "video":
        help_.downloading_videos_thread()
    elif topic == "other":
        help_.other_issues_thread()

tools_menu.add_command(label="Go To Destination Folder", command=go_to)
tools_menu.add_separator()
tools_menu.add_command(label="Install FFmpeg", command=installffmpeg)
tools_menu.add_command(label="Install WebDriver", command=installwebdriver)
tools_menu.add_separator()
tools_menu.add_command(label="Update GUI", command=updategui)

credits_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Credits", menu=credits_menu)

credits_menu.add_command(label="Made by Gloryness#4341 (discord)")
credits_menu.add_separator()
credits_menu.add_command(label="Join my discord server!", command=discord_join)
credits_menu.add_command(label="Donate to support me!", command=donate)
credits_menu.add_command(label="View code on GitHub", command=view_github)

help_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="Installing/Setting up FFmpeg", command=lambda: request_help("ffmpeg"))
help_menu.add_command(label="How do you use 'Detect URLS'?", command=lambda: request_help("urls"))
help_menu.add_command(label="Downloading Videos", command=lambda: request_help("video"))
help_menu.add_command(label="Other Issues", command=lambda: request_help("other"))
help_menu.add_separator()

label1 = Label(root, text="Destination -", bg="#cbdbfc")
label1.grid(row=0, column=0)

destination_var = StringVar()

destination = Entry(root, width=77, state=DISABLED, relief=SOLID, textvariable=destination_var)
destination.grid(row=0, column=1, padx=0, pady=0)

def save_browse_destination():
    if len(file_option.title_var.get()) < 1:
        return '%(title)s.%(ext)s'
    else:
        return file_option.title_var.get()

def browse():
    def onbrowse():
        """
        For setting the destination for the download.
        """
        global video_ops
        destination.configure(state=NORMAL)
        with open(setting.name_of_json) as f:
            data = json.load(f)

        for key, value in data.items():
            if key == 'settings':
                for general_name, general_detail in value[0].items():
                    pass
        if len(destination_var.get()) <= 1:
            get_directory = filedialog.askdirectory(initialdir=general_detail['initialdir'], title="Destination")

        elif len(destination_var.get()) > 1:
            get_directory = filedialog.askdirectory(initialdir=destination_var.get(), title="Destination")

        destination.delete(0, END)
        destination.insert(0, get_directory)

        video_ops.update(outtmpl=f'{destination_var.get()}{"" if get_directory.endswith("/") else "/"}{save_browse_destination()}')
        destination.configure(state=DISABLED)
        print(video_ops, end="\n\n")
    browse_thread = threading.Thread(target=onbrowse)
    browse_thread.start()

def auto_fill():
    with open(setting.name_of_json) as f:
        data = json.load(f)

    for key, value in data.items():
        if key == 'settings':
            for general_name, general_detail in value[0].items():
                pass
            for config_name, config_detail in value[2].items():
                pass
    if general_detail['auto_fill_destination'] != "":
        destination.config(state=NORMAL)
        destination.delete(0, END)
        destination.insert(0, general_detail['auto_fill_destination'])
        destination.config(state=DISABLED)
        video_ops.update(outtmpl='{}/{}'.format(destination_var.get(), save_browse_destination()))
        print(video_ops, end="\n\n")

def set_path():
    with open(setting.name_of_json) as f:
        data = json.load(f)

    for key, value in data.items():
        if key == 'settings':
            for sel_name, sel_detail in value[1].items():
                pass
    global PATH
    PATH = sel_detail['path']

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

quality_label = Label(root, text="Quality", bg="#cbdbfc", font="Cooper 15")
quality_label.place(x=65, y=71)

quality_dropdown = ttk.OptionMenu(root, quality_btn_var, *quality_btn_options, style='dropdown.TMenubutton')
quality_dropdown.place(x=50, y=98, width=90)

quality_btn_var.set(quality_btn_options[1])

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

audio_label = Label(root, text="Audio", bg="#cbdbfc", font="Cooper 15")
audio_label.place(x=238, y=71)

audio_dropdown = ttk.OptionMenu(root, audio_btn_var, *audio_btn_options, style='dropdown.TMenubutton')
audio_dropdown.place(x=220, y=98, width=90)

audio_btn_var.set(audio_btn_options[1])

###########################################################################

ext_btn_options = [
    "MP4",
    "MP4",
    "MP3",
    "MKV",
    "WEBM",
    "WAV",
    "FLV",
    "M4A",
    "AVI",
    "OGG"
]

ext_btn_var = StringVar()

ext_label = Label(root, text="Ext", bg="#cbdbfc", font="Cooper 15")
ext_label.place(x=422, y=71)

ext_dropdown = ttk.OptionMenu(root, ext_btn_var, *ext_btn_options, style='dropdown.TMenubutton')
ext_dropdown.place(x=400, y=98, width=90)

ext_btn_var.set(ext_btn_options[3])

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
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        global video_ops
        if quality_btn_var.get() == "NONE":
            pass

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
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
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
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        global video_ops
        if quality_btn_var.get() != "NONE" \
            and audio_btn_var.get() != "NONE":
                index = len(audio_btn_var.get()) - 1
                video_ops.update(format=cls._format+'+bestaudio/best[abr<={}]'.format(audio_btn_var.get()[0:index]))
                cls._format = video_ops.get('format')

        elif audio_btn_var.get() != "NONE" \
            and quality_btn_var.get() == "NONE":
                if ext_btn_var.get() == "OGG":
                    video_ops.update(postprocessors=[{
                        "key": 'FFmpegExtractAudio',
                        "preferredcodec": 'mp3'
                    }])
                else:
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
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        global video_ops
        if quality_btn_var.get() != "NONE" \
            and audio_btn_var.get() != "NONE":
                if ext_btn_var.get() == "MP4":
                    video_ops.update(ext='{}'.format(ext_btn_var.get().lower()), merge_output_format='mkv')
                elif ext_btn_var.get() == "WEBM":
                    video_ops.update(ext='{}'.format(ext_btn_var.get().lower()), merge_output_format='mkv')
                elif ext_btn_var.get() == "FLV":
                    video_ops.update(ext='{}'.format(ext_btn_var.get().lower()), merge_output_format='mkv')
                elif ext_btn_var.get() == "AVI":
                    video_ops.update(ext='{}'.format(ext_btn_var.get().lower()), merge_output_format='mkv')
                else:
                    video_ops.update(ext='{}'.format(ext_btn_var.get().lower()), merge_output_format='{}'.format(ext_btn_var.get().lower()))

        elif quality_btn_var.get() == "NONE" \
            and audio_btn_var.get() != "NONE":
                if ext_btn_var.get() == "OGG":
                    video_ops.update(ext='mp3', merge_output_format='{}'.format(ext_btn_var.get().lower()))
                else:
                    video_ops.update(ext='{}'.format(ext_btn_var.get().lower()), merge_output_format='{}'.format(ext_btn_var.get().lower()))

        elif audio_btn_var.get() == "NONE" \
            and quality_btn_var.get() != "NONE":
                if ext_btn_var.get() == "MP4":
                    video_ops.update(ext='{}'.format(ext_btn_var.get().lower()), merge_output_format='mkv')
                elif ext_btn_var.get() == "WEBM":
                    video_ops.update(ext='{}'.format(ext_btn_var.get().lower()), merge_output_format='mkv')
                elif ext_btn_var.get() == "FLV":
                    video_ops.update(ext='{}'.format(ext_btn_var.get().lower()), merge_output_format='mkv')
                elif ext_btn_var.get() == "AVI":
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
        style1.configure('done.TButton', bd=1)
        quality_dropdown.configure(state=DISABLED)
        audio_dropdown.configure(state=DISABLED)
        ext_dropdown.configure(state=DISABLED)

    @staticmethod
    def edit_format_btns():
        with open(setting.name_of_json) as f:
            data = json.load(f)

        for key, value in data.items():
            if key == 'settings':
                for general_name, general_detail in value[0].items():
                    pass
        if general_detail['disabled_editformat_messagebox'] is True:
            done_btn.configure(state=NORMAL)
            style1.configure('done.TButton', bd=2)
            quality_dropdown.configure(state=NORMAL)
            audio_dropdown.configure(state=NORMAL)
            ext_dropdown.configure(state=NORMAL)
            do.disable_options()
        else:
            confirm = messagebox.askquestion("Are You Sure?", "Would you like to edit your video formats?")
            if confirm == "yes":
                done_btn.configure(state=NORMAL)
                style1.configure('done.TButton', bd=2)
                quality_dropdown.configure(state=NORMAL)
                audio_dropdown.configure(state=NORMAL)
                ext_dropdown.configure(state=NORMAL)
                do.disable_options()
            else:
                pass

    @staticmethod
    def after_done_btn():
        file_options_btn.configure(state=NORMAL)
        download_options_btn.configure(state=NORMAL)
        other_options_btn.configure(state=NORMAL)
        detect_btn.configure(state=NORMAL)
        download_btn.configure(state=NORMAL)
        edit_format.configure(state=NORMAL)
        url_box.configure(state=NORMAL, bd=4)
        clear_btn.configure(state=NORMAL)

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

def click():
    if quality_btn_var.get() == "NONE" \
        and audio_btn_var.get() == "NONE":
        messagebox.showerror("?????", "You have asked for no audio and no quality, therefore cannot continue.")

    elif quality_btn_var.get() == "NONE" \
        and audio_btn_var.get() != "NONE" \
        and ext_btn_var.get() != "MP3" \
        and ext_btn_var.get() != "WAV" \
        and ext_btn_var.get() != "M4A" \
        and ext_btn_var.get() != "OGG":
            messagebox.showerror("?????", "If you want an audio-only file, please use an MP3 or WAV or M4A or OGG extension.")

    elif quality_btn_var.get() != "NONE" \
        and audio_btn_var.get() != "NONE":
            if ext_btn_var.get() == "MP3" \
                or ext_btn_var.get() == "WAV" \
                or ext_btn_var.get() == "M4A" \
                or ext_btn_var.get() == "OGG":
                    messagebox.showerror("?????", f"Sorry, but {ext_btn_var.get()} is not a supported file-type for videos.\nWell it could be, but let's act professional here.")
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
                or ext_btn_var.get() == "WAV" \
                or ext_btn_var.get() == "M4A" \
                or ext_btn_var.get() == "OGG":
                    messagebox.showerror("?????", f"Sorry, but {ext_btn_var.get()} is not a supported file-type for videos.")
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

def done_btn_func():
    def on_done_btn():
        with open(setting.name_of_json) as f:
            data = json.load(f)

        for key, value in data.items():
            if key == 'settings':
                for general_name, general_detail in value[0].items():
                    pass
        if general_detail['disable_done_messagebox'] is True:
            click()
        else:
            verify = messagebox.askquestion("Are You Sure?", "This will be your format, are you sure you want to continue?")
            if verify == "yes":
                click()
            else:
                pass
    done_btn_thread = threading.Thread(target=on_done_btn)
    done_btn_thread.start()

def auto_fill_and_click_thread():
    my_thread = threading.Timer(1.25, auto_fill_and_click)
    my_thread.start()

def auto_fill_and_click():
    with open(setting.name_of_json) as f:
        data = json.load(f)

    for key, value in data.items():
        if key == 'settings':
            for general_name, general_detail in value[0].items():
                pass
    if general_detail['auto_format_and_click'] is True:
        quality_btn_var.set(general_detail['formats'][0])
        audio_btn_var.set(general_detail['formats'][1])
        ext_btn_var.set(general_detail['formats'][2])
        if general_detail['formats'][3] == "Auto-Click":
            click()
        else:
            pass
    else:
        pass

def check():
    with open(setting.name_of_json) as f:
        data = json.load(f)

    for key, value in data.items():
        if key == 'options':
            for file_name, file_detail in value[0].items():
                pass
            for download_name, download_detail in value[1].items():
                pass
            for other_name, other_detail in value[2].items():
                pass
        if key == 'settings':
            for config_name, config_detail in value[2].items():
                pass
    if not config_detail['dont_save_file_options']:
        if file_detail['cachedir'] is True:
            video_ops.update(cachedir=False)
        if file_detail['nooverwrites'] is True:
            video_ops.update(nooverwrites=True)
        if file_detail['restrictfilenames'] is True:
            video_ops.update(restrictfilenames=True)
        if len(file_detail['cookiefile']) >= 1:
            video_ops.update(cookiefile=file_detail['cookiefile'])

    if not config_detail['dont_save_download_options']:
        if download_detail['prefer_avconv'] is True:
            video_ops.update(prefer_ffmpeg=False)
        if download_detail['external_downloader'] != 'Default':
            video_ops.update(external_downloader=download_detail['external_downloader'])
        if len(download_detail['ffmpeg_location']) >= 1:
            video_ops.update(ffmpeg_location=download_detail['ffmpeg_location'])

    if not config_detail['dont_save_other_options']:
        if other_detail['no_warnings'] is True:
            video_ops.update(no_warnings=True)
        if other_detail['ignoreerrors'] is True:
            video_ops.update(ignoreerrors=True)
        if other_detail['age_limit'] is True:
            video_ops.update(age_limit=other_detail['age_limit'])
        if other_detail['rejecttitle'] is True:
            video_ops.update(rejecttitle=True)
        if other_detail['keepvideo'] is True:
            video_ops.update(keepvideo=True)
        if other_detail['no_check_certificate'] is True:
            video_ops.update(nocheckcertificate=True)
        global max_downloads, wait_time
        max_downloads = other_detail['max_downloads']
        wait_time = other_detail['time_between_downloads']
    print(video_ops, "CHECK\n", sep="   ")

done_btn = ttk.Button(root, text="Done", style='done.TButton', command=done_btn_func)
done_btn.place(x=228, y=154)

###########################################################################

second_format_frame = LabelFrame(root, padx=260, bg="#cbdbfc", labelanchor=N, relief=SOLID)
second_format_frame.grid(row=6, columnspan=5, pady=35, ipady=40)

second_invis_label = Label(second_format_frame, text="", bg="#cbdbfc")
second_invis_label.grid(row=6, column=0)

second_format_label = Label(root, text="Options", bg="#cbdbfc", fg="blue")
second_format_label.place(x=242, y=197)

infinity = 9999999
max_downloads = infinity
file_count = 1
download_count = 1
other_count = 1
settings_count = 1
_stabalize = [file_count, download_count, other_count, settings_count]

def reset_file_window(win):
    global _stabalize
    _stabalize[0] = 1
    _stabalize[1] = 1
    _stabalize[2] = 1
    _stabalize[3] = 1
    state = str(done_btn['state'])
    if state == 'disabled':
        download_btn.configure(state=NORMAL)
    file_option.hold_variables()

def reset_download_window(win):
    global _stabalize
    _stabalize[0] = 1
    _stabalize[1] = 1
    _stabalize[2] = 1
    _stabalize[3] = 1
    state = str(done_btn['state'])
    if state == 'disabled':
        download_btn.configure(state=NORMAL)
    download_option.hold_variables()

def reset_other_window(win):
    global _stabalize
    _stabalize[0] = 1
    _stabalize[1] = 1
    _stabalize[2] = 1
    _stabalize[3] = 1
    state = str(done_btn['state'])
    if state == 'disabled':
        download_btn.configure(state=NORMAL)
    other_option.hold_variables()

class FileOptionWindow(object):
    """
    * Filesystem Options
    """
    def __init__(self):
        self._title = 'File Options   |   Gloryness  |  v{}'.format(__version__)
        self._icon = 'images/#app.ico'
        self._size = '600x450'
        self.title_var = StringVar()
        self.title_menu_var = StringVar()
        self.seperator_var = StringVar()

        self.remember = 'id'
        self.remember2 = '.'
        self.storage = '%(title)s.%(ext)s'
        self.backup_length = ['%(title)s', '.%(ext)s']
        self.length = ['%(title)s', '.%(ext)s']
        self.index = 0

        self.isSaved = False
        self.title_saved = True

    def on_file_options(self):
        file_options_thread = threading.Thread(target=self.file_options_window)
        file_options_thread.start()

    def hold_saved_variables(self):
        if not self.isSaved:
            if not self.title_saved:
                self.title_entry.delete(0, END)
                self.title_var.set(self.storage)
                self.length = self.backup_length.copy()

        if self.isSaved:
            pass

    def hold_variables(self):
        if len(self.title_var.get()) <= 2:
            messagebox.showwarning("???", "Must include a actual title bud.", parent=self.file_win)
        else:
            state = str(self.apply_btn['state'])
            if state == 'disabled':
                self.file_win.destroy()
            else:
                responce = messagebox.askquestion("Are You Sure?", "You have made unsaved changed, are you sure you want to exit?", parent=self.file_win)
                if responce == 'yes':
                    self.hold_saved_variables()
                    self.file_win.destroy()
                else:
                    pass

    def add(self):
        self.isSaved = False
        self.title_saved = False
        seperator = self.seperator_var.get()
        if seperator == "Space":
            self.apply_btn.configure(state=ACTIVE)
            self.title_entry.configure(state=NORMAL)
            self.title_entry.insert(END, " %(" + self.title_menu_var.get() + ")s")
            self.length.append(str(" %(" + self.title_menu_var.get() + ")s"))
            self.title_entry.configure(state=DISABLED)
        elif seperator == "None":
            self.apply_btn.configure(state=ACTIVE)
            self.title_entry.configure(state=NORMAL)
            self.title_entry.insert(END, "%(" + self.title_menu_var.get() + ")s")
            self.length.append(str("%(" + self.title_menu_var.get() + ")s"))
            self.title_entry.configure(state=DISABLED)
        else:
            self.apply_btn.configure(state=ACTIVE)
            self.title_entry.configure(state=NORMAL)
            self.title_entry.insert(END, f"{self.seperator_var.get()}%(" + self.title_menu_var.get() + ")s")
            self.length.append(str(f"{self.seperator_var.get()}%(" + self.title_menu_var.get() + ")s"))
            self.title_entry.configure(state=DISABLED)
        print(self.length)

    def delete(self):
        self.isSaved = False
        self.title_saved = False
        self.apply_btn.configure(state=ACTIVE)
        try:
            self.index = len(self.length) - 1
            self.title_entry.configure(state=NORMAL)
            self.title_entry.delete(len(self.title_var.get()) - len(self.length[self.index]), END)
            self.title_entry.configure(state=DISABLED)
            self.length.pop(self.index)
            print(self.length)
        except IndexError:
            self.title_entry.configure(state=NORMAL)
            self.length.clear()
            self.title_entry.delete(0, END)
            self.title_entry.configure(state=DISABLED)

    def update_apply_btn(self):
        self.apply_btn.configure(state=ACTIVE)

    def option_update_apply_btn(self, event):
        self.apply_btn.configure(state=ACTIVE)
        self.isSaved = False

    def file_options_window(self):
        global _stabalize
        if _stabalize[0] == 1:
            with open(setting.name_of_json) as f:
                data = json.load(f)

            for key, value in data.items():
                if key == 'options':
                    for file_name, file_detail in value[0].items():
                        pass
                if key == 'settings':
                    for config_name, config_detail in value[2].items():
                        pass
            download_btn.configure(state=DISABLED)
            print(self.length)
            self.file_win = Toplevel()
            self.file_win.title(self._title)
            self.file_win.iconbitmap(self._icon)
            self.file_win.resizable(False, False)
            self.file_win.configure(bg='#cbdbfc', bd=5)
            self.file_win.geometry(self._size)
            self.file_win.protocol("WM_DELETE_WINDOW", lambda: reset_file_window(self.file_win))

            border = LabelFrame(self.file_win, height=425, width=560, bg='#cbdbfc', bd=2, text="Filesystem Options", font="Cooper 18", labelanchor=N, relief=SOLID)
            border.place(x=15, y=7)

            in_border = Frame(self.file_win, height=380, width=522, bg='#afc2e9')
            in_border.place(x=35, y=36)

            title_label = Label(self.file_win, text="Title:", font='Cooper 14', bg='#afc2e9')
            title_label.place(x=40, y=40)

            self.title_entry = Entry(self.file_win, width=74, state=NORMAL, relief=SOLID, textvariable=self.title_var)
            self.title_entry.place(x=90, y=45)

            if not self.title_var.get().endswith(("%(id)s", "%(title)s", "%(ext)s", "%(uploader)s", "%(upload_date)s", "%(channel)s", "%(duration)s",
                "%(view_count)s", "%(like_count)s", "%(dislike_count)s", "%(is_live)s", "%(playlist)s", "%(playlist_title)s",
                    "%(chapter)s", "%(series)s", "%(season)s", "%(episode)s", "%(track)s", "%(artist)s", "%(genre)s", "%(album)s")):
                self.title_entry.insert(0, self.storage)
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

            file_name_menu = ttk.OptionMenu(self.file_win, self.title_menu_var, *title_options, style='dropdown.TMenubutton', command=self.option_update_apply_btn)
            file_name_menu.place(x=90, y=75, width=110)

            self.title_menu_var.set(self.remember)

            add_outtmpl = ttk.Button(self.file_win, text="ADD", style='option1.TButton', command=self.add)
            add_outtmpl.place(x=230, y=75)

            remove_outtmpl = ttk.Button(self.file_win, text="REMOVE", style='option1.TButton', command=self.delete)
            remove_outtmpl.place(x=300, y=75)

            seperator_options = [
                'Space',
                'None',
                'Space',
                ' - ',
                '.',
                ' , ',
                ' ~ ',
                ' # ',
                ' + ',
                ' _ ',
                ' ! ',
                ' / ',
                ' \ ',
                ' > ',
                ' < '
            ]

            seperator_label = Label(self.file_win, text="Seperator:", font='Cooper 9', bg='#afc2e9')
            seperator_label.place(x=380, y=75)

            seperator = ttk.OptionMenu(self.file_win, self.seperator_var, *seperator_options, style='dropdown.TMenubutton', command=self.option_update_apply_btn)
            seperator.place(x=450, y=75)

            self.seperator_var.set(self.remember2)


            exit_btn = ttk.Button(self.file_win, text="Exit", style='option.TButton', command=lambda: reset_file_window(self.file_win))
            exit_btn.place(x=430, y=386)

            self.apply_btn = ttk.Button(self.file_win, text="Apply", state=DISABLED, style='option.TButton', command=self.file_apply)
            self.apply_btn.place(x=500, y=386)
            style = ttk.Style()
            style.configure('TCheckbutton', background='#afc2e9')

            self.var_1 = BooleanVar()
            check_1 = ttk.Checkbutton(self.file_win, text="Write video description to a .description file.",
                                      variable=self.var_1, onvalue=True, offvalue=False, style='TCheckbutton', command=self.update_apply_btn)
            check_1.place(x=40, y=120)

            self.var_2 = BooleanVar()
            check_2 = ttk.Checkbutton(self.file_win, text="Write video description to a .json file.",
                                      variable=self.var_2, onvalue=True, offvalue=False, style='TCheckbutton', command=self.update_apply_btn)
            check_2.place(x=40, y=150)

            self.var_3 = BooleanVar()
            check_3 = ttk.Checkbutton(self.file_win, text="Write video annotations to a .xml file.",
                                      variable=self.var_3, onvalue=True, offvalue=False, style='TCheckbutton', command=self.update_apply_btn)
            check_3.place(x=40, y=180)

            self.var_4 = BooleanVar()
            check_4 = ttk.Checkbutton(self.file_win, text="Write the thumbnail image to a file.",
                                      variable=self.var_4, onvalue=True, offvalue=False, style='TCheckbutton', command=self.update_apply_btn)
            check_4.place(x=40, y=210)

            self.var_5 = BooleanVar()
            check_5 = ttk.Checkbutton(self.file_win, text="Write all thumbnail formats to files.",
                                      variable=self.var_5, onvalue=True, offvalue=False, style='TCheckbutton', command=self.update_apply_btn)
            check_5.place(x=40, y=240)

            self.var_6 = BooleanVar()
            check_6 = ttk.Checkbutton(self.file_win, text="Write the video subtitles to a file.",
                                      variable=self.var_6, onvalue=True, offvalue=False, style='TCheckbutton', command=self.update_apply_btn)
            check_6.place(x=40, y=270)

            self.var_7 = BooleanVar()
            check_7 = ttk.Checkbutton(self.file_win, text="Write the automatically generated subtitles \nto a file.",
                                      variable=self.var_7, onvalue=True, offvalue=False, style='TCheckbutton', command=self.update_apply_btn)
            check_7.place(x=304, y=110)

            self.var_8 = BooleanVar()
            check_8 = ttk.Checkbutton(self.file_win, text="Lists all available subtitles for the video.",
                                      variable=self.var_8, onvalue=True, offvalue=False, style='TCheckbutton', command=self.update_apply_btn)
            check_8.place(x=304, y=150)

            self.var_9 = BooleanVar()
            check_9 = ttk.Checkbutton(self.file_win, text="Disable filesystem caching",
                                      variable=self.var_9, onvalue=True, offvalue=False, style='TCheckbutton', command=self.update_apply_btn)
            check_9.place(x=304, y=180)

            self.var_10 = BooleanVar()
            check_10 = ttk.Checkbutton(self.file_win, text="Do not overwrite files",
                                       variable=self.var_10, onvalue=True, offvalue=False, style='TCheckbutton', command=self.update_apply_btn)
            check_10.place(x=304, y=210)

            self.var_11 = BooleanVar()
            check_11 = ttk.Checkbutton(self.file_win, text="Restrict filenames\n(do not allow spaces and '&')",
                                       variable=self.var_11, onvalue=True, offvalue=False, style='TCheckbutton', command=self.update_apply_btn)
            check_11.place(x=304, y=235)


            cookie_label = Label(self.file_win, text="Where cookies should be read from and dumpted to:", bg='#afc2e9')
            cookie_label.place(x=268, y=275)

            self.var_12 = StringVar()
            cookie_entry = Entry(self.file_win, state=DISABLED, relief=SOLID, width=40, textvariable=self.var_12)
            cookie_entry.place(x=280, y=295)

            if not config_detail['dont_save_file_options']:
                self.title_entry.configure(state=NORMAL)
                self.title_entry.delete(0, END)
                self.title_var.set(file_detail['outtmpl'])
                self.title_entry.configure(state=DISABLED)
                self.var_1.set(file_detail['writedescription'])
                self.var_2.set(file_detail['writeinfojson'])
                self.var_3.set(file_detail['writeannotations'])
                self.var_4.set(file_detail['writethumbnail'])
                self.var_5.set(file_detail['write_all_thumbnails'])
                self.var_6.set(file_detail['writesubtitles'])
                self.var_7.set(file_detail['writeautomaticsub'])
                self.var_8.set(file_detail['listsubtitles'])
                self.var_9.set(file_detail['cachedir'])
                self.var_10.set(file_detail['nooverwrites'])
                self.var_11.set(file_detail['restrictfilenames'])
                cookie_entry.configure(state=NORMAL)
                cookie_entry.delete(0, END)
                self.var_12.set(file_detail['cookiefile'])
                cookie_entry.configure(state=DISABLED)

                self.apply_btn.configure(state=NORMAL)

            def browse():
                self.update_apply_btn()
                with open(setting.name_of_json) as f:
                    data = json.load(f)

                for key, value in data.items():
                    if key == 'settings':
                        for general_name, general_detail in value[0].items():
                            pass
                if len(self.var_12.get()) <= 1:
                    cookie_browse = filedialog.askopenfilename(initialdir=general_detail['initialdir'], title="Destination For Cookies",
                                                               filetypes=(("all files", "*.*"), ("txt files", "*.txt")), parent=self.file_win)

                elif len(self.var_12.get()) > 1:
                    cookie_browse = filedialog.askopenfilename(initialdir=self.var_12.get(), title="Destination For Cookies",
                                                               filetypes=(("all files", "*.*"), ("txt files", "*.txt")), parent=self.file_win)

                cookie_entry.configure(state=NORMAL)
                cookie_entry.delete(0, END)
                cookie_entry.insert(0, cookie_browse)
                cookie_entry.configure(state=DISABLED)

            def clear_text():
                self.update_apply_btn()
                cookie_entry.configure(state=NORMAL)
                cookie_entry.delete(0, END)
                cookie_entry.configure(state=DISABLED)

            cookie_button = ttk.Button(self.file_win, text="Browse", style='some.TButton', command=browse)
            cookie_button.place(x=360, y=320)
            global clear_img
            clear_img = ImageTk.PhotoImage(Image.open('images/#delete_18px.png'))
            clearbtn = ttk.Button(self.file_win, image=clear_img, command=clear_text)
            clearbtn.place(x=530, y=294)

            for index, var in enumerate(_stabalize):
                _stabalize[index] += 1
            print(_stabalize)
        else:
            pass

    def file_apply(self):
        with open(setting.name_of_json) as f:
            data = json.load(f)

        for key, value in data.items():
            if key == 'options':
                for file_name, file_detail in value[0].items():
                    pass
            if key == 'settings':
                for config_name, config_detail in value[2].items():
                    pass

        if len(self.title_var.get()) >= 3:
            global video_ops
            self.apply_btn.configure(state=DISABLED)
            if len(destination_var.get()) <= 2:
                video_ops.update(outtmpl=f"{destination_var.get()}{self.title_var.get()}")
            else:
                video_ops.update(outtmpl=f"{destination_var.get()}/{self.title_var.get()}")

            self.isSaved = True
            self.title_saved = True
            self.remember = self.title_menu_var.get()
            self.remember2 = self.seperator_var.get()
            self.storage = self.title_var.get()
            self.backup_length = self.length.copy()

            if self.var_1.get():
                video_ops.update(writedescription=True)
            else:
                video_ops.update(writedescription=False)
                video_ops.pop('writedescription')

            if self.var_2.get():
                video_ops.update(writeinfojson=True)
            else:
                video_ops.update(writeinfojson=False)
                video_ops.pop('writeinfojson')

            if self.var_3.get():
                video_ops.update(writeannotations=True)
            else:
                video_ops.update(writeannotations=False)
                video_ops.pop('writeannotations')

            if self.var_4.get():
                video_ops.update(writethumbnail=True)
            else:
                video_ops.update(writethumbnail=False)
                video_ops.pop('writethumbnail')

            if self.var_5.get():
                video_ops.update(write_all_thumbnails=True)
            else:
                video_ops.update(write_all_thumbnails=False)
                video_ops.pop('write_all_thumbnails')

            if self.var_6.get():
                video_ops.update(writesubtitles=True)
            else:
                video_ops.update(writesubtitles=False)
                video_ops.pop('writesubtitles')

            if self.var_7.get():
                video_ops.update(writeautomaticsub=True)
            else:
                video_ops.update(writeautomaticsub=False)
                video_ops.pop('writeautomaticsub')

            if self.var_8.get():
                video_ops.update(listsubtitles=True)
            else:
                video_ops.update(listsubtitles=False)
                video_ops.pop('listsubtitles')

            if self.var_9.get():
                video_ops.update(cachedir=False)
            else:
                video_ops.update(cachedir='~/.cache/youtube-dl')
                video_ops.pop('cachedir')

            if self.var_10.get():
                video_ops.update(nooverwrites=True)
            else:
                video_ops.update(nooverwrites=False)
                video_ops.pop('nooverwrites')

            if self.var_11.get():
                video_ops.update(restrictfilenames=True)
            else:
                video_ops.update(restrictfilenames=False)
                video_ops.pop('restrictfilenames')

            if len(self.var_12.get()) <= 2:
                video_ops.update(cookiefile=None)
                video_ops.pop('cookiefile')
            else:
                video_ops.update(cookiefile=self.var_12.get())

            if not config_detail['dont_save_file_options']:
                file_detail['outtmpl'] = self.title_var.get()
                file_detail['writedescription'] = self.var_1.get()
                file_detail['writeinfojson'] = self.var_2.get()
                file_detail['writeannotations'] = self.var_3.get()
                file_detail['writethumbnail'] = self.var_4.get()
                file_detail['write_all_thumbnails'] = self.var_5.get()
                file_detail['writesubtitles'] = self.var_6.get()
                file_detail['writeautomaticsub'] = self.var_7.get()
                file_detail['listsubtitles'] = self.var_8.get()
                file_detail['cachedir'] = self.var_9.get()
                file_detail['nooverwrites'] = self.var_10.get()
                file_detail['restrictfilenames'] = self.var_11.get()
                file_detail['cookiefile'] = self.var_12.get()
                with open(setting.name_of_json, 'w') as f:
                    json.dump(data, f, indent=3)
                    f.close()
            else:
                file_detail['outtmpl'] = "%(title)s.%(ext)s"
                file_detail['writedescription'] = False
                file_detail['writeinfojson'] = False
                file_detail['writeannotations'] = False
                file_detail['writethumbnail'] = False
                file_detail['write_all_thumbnails'] = False
                file_detail['writesubtitles'] = False
                file_detail['writeautomaticsub'] = False
                file_detail['listsubtitles'] = False
                file_detail['cachedir'] = False
                file_detail['nooverwrites'] = False
                file_detail['restrictfilenames'] = False
                file_detail['cookiefile'] = ""
                with open(setting.name_of_json, 'w') as f:
                    json.dump(data, f, indent=3)
                    f.close()

            sys.stderr = sys.__stderr__
            sys.stdout = sys.__stdout__
            print(video_ops, "FILE OPTIONS", sep="   ", end="\n\n")

        else:
            messagebox.showwarning("???", "Must include a actual title bud.", parent=self.file_win)

###############################################################################################################

class DownloadOptionWindow(object):
    """
    * Download Options
    """
    def __init__(self):
        self._title = 'Download Options   |   Gloryness  |  v{}'.format(__version__)
        self._icon = 'images/#app.ico'
        self._size = '600x450'
        self.apply_btn = None
        self.input_entry1 = None
        self.input_entry2 = None
        self.input_entry3 = None
        self.input_entry4 = None
        self.ffmpeg_location = None
        self.download_win = None
        self.remember_speed = '4.2M'
        self.remember_downloader = 'Default'
        self.isSaved = False
        self.count = 1

        self.input_entry1_saved = False
        self.input_entry2_saved = False
        self.input_entry3_saved = False
        self.input_entry4_saved = False

        self.storage1 = ''
        self.storage2 = ''
        self.storage3 = ''
        self.storage4 = ''

        self.var_1, self.var_2, self.var_3, self.var_4, self.var_5, self.var_6, self.var_7, self.var_8, \
            self.var_9, self.var_10, self.var_11, self.var_12, self.var_13, self.var_14, self.var_15 = \
            BooleanVar(), BooleanVar(), BooleanVar(), BooleanVar(), BooleanVar(), BooleanVar(), BooleanVar(), BooleanVar(), \
            StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()

    def on_download_options(self):
        download_options_thread = threading.Thread(target=self.download_options_window)
        download_options_thread.start()

    def update_apply_btn(self):
        self.apply_btn.configure(state=ACTIVE)
        self.isSaved = False

    def option_update_apply_btn(self, event):
        self.apply_btn.configure(state=ACTIVE)
        self.isSaved = False

    def hold_saved_variables(self):
        if not self.isSaved:
            if self.input_entry1_saved is False:
                self.input_entry1.delete(0, END)
                self.var_9.set(self.storage1)

            if self.input_entry2_saved is False:
                self.input_entry2.delete(0, END)
                self.var_10.set(self.storage2)

            if self.input_entry3_saved is False:
                self.input_entry3.delete(0, END)
                self.var_11.set(self.storage3)

            if self.input_entry4_saved is False:
                self.input_entry4.delete(0, END)
                self.var_12.set(self.storage4)
        if self.isSaved:
            pass

    def hold_variables(self):
        state = str(self.apply_btn['state'])
        if state == 'disabled':
            self.download_win.destroy()
        else:
            responce = messagebox.askquestion("Are You Sure?", "You have made unsaved changed, are you sure you want to exit?", parent=self.download_win)
            if responce == 'yes':
                self.hold_saved_variables()
                self.download_win.destroy()
            else:
                pass

    def download_options_window(self):
        global _stabalize
        if _stabalize[1] == 1:
            with open(setting.name_of_json) as f:
                data = json.load(f)

            for key, value in data.items():
                if key == 'options':
                    for download_name, download_detail in value[1].items():
                        pass
                if key == 'settings':
                    for config_name, config_detail in value[2].items():
                        pass
            download_btn.configure(state=DISABLED)
            self.download_win = Toplevel()
            self.download_win.title(self._title)
            self.download_win.iconbitmap(self._icon)
            self.download_win.resizable(False, False)
            self.download_win.configure(bg='#cbdbfc', bd=5)
            self.download_win.geometry(self._size)
            self.download_win.protocol("WM_DELETE_WINDOW", lambda: reset_download_window(self.download_win))

            border = LabelFrame(self.download_win, height=425, width=560, bg='#cbdbfc', bd=2, text="Download Options",
                                font="Cooper 18", labelanchor=N, relief=SOLID)
            border.place(x=15, y=7)

            in_border = Frame(self.download_win, height=380, width=522, bg='#afc2e9')
            in_border.place(x=35, y=36)

            exit_btn = ttk.Button(self.download_win, text="Exit", style='option.TButton', command=lambda: reset_download_window(self.download_win))
            exit_btn.place(x=430, y=386)

            self.apply_btn = ttk.Button(self.download_win, text="Apply", state=DISABLED, style='option.TButton', command=self.download_apply)
            self.apply_btn.place(x=500, y=386)

            style = ttk.Style()
            style.configure('TCheckbutton', background='#afc2e9')
            i = 46
            check_1 = ttk.Checkbutton(self.download_win, text="Prefer avconv instead of ffmpeg",
                                      variable=self.var_1, onvalue=True, offvalue=False, style='TCheckbutton', command=self.update_apply_btn)
            check_1.place(x=46, y=i)
            i += 32
            check_2 = ttk.Checkbutton(self.download_win, text="Use native HLS downloader instead",
                                      variable=self.var_2, onvalue=True, offvalue=False, style='TCheckbutton', command=self.update_apply_btn)
            check_2.place(x=46, y=i)
            i += 32
            check_3 = ttk.Checkbutton(self.download_win, text="Do not use temporary .part files",
                                      variable=self.var_3, onvalue=True, offvalue=False, style='TCheckbutton', command=self.update_apply_btn)
            check_3.place(x=46, y=i)
            i += 32
            check_4 = ttk.Checkbutton(self.download_win, text="Download ads as well (may not work)",
                                      variable=self.var_4, onvalue=True, offvalue=False, style='TCheckbutton', command=self.update_apply_btn)
            check_4.place(x=46, y=i)
            i += 32
            check_5 = ttk.Checkbutton(self.download_win, text="Keep fragments after download",
                                      variable=self.var_5, onvalue=True, offvalue=False, style='TCheckbutton', command=self.update_apply_btn)
            check_5.place(x=46, y=i)
            i += 32
            check_6 = ttk.Checkbutton(self.download_win, text="Download playlist in random order",
                                      variable=self.var_6, onvalue=True, offvalue=False, style='TCheckbutton', command=self.update_apply_btn)
            check_6.place(x=46, y=i)
            i += 32
            check_8 = ttk.Checkbutton(self.download_win, text="Download only video from playlist",
                                      variable=self.var_8, onvalue=True, offvalue=False, style='TCheckbutton', command=self.update_apply_btn)
            check_8.place(x=46, y=i)
            i += 32
            check_7 = ttk.Checkbutton(self.download_win, text="Download playlist in reverse order",
                                      variable=self.var_7, onvalue=True, offvalue=False, style='TCheckbutton', command=self.update_apply_btn)
            check_7.place(x=46, y=i)

            label_6 = Label(self.download_win, text='Specific items in playlist to download:', bg='#afc2e9')
            label_6.place(x=46, y=325)
            eg3 = Label(self.download_win, text="(e.g 1-3,5,7 >>> 1+2+3+5+7)", bg='#afc2e9')
            eg3.place(x=66, y=348)

            self.input_entry1 = Entry(self.download_win, width=32, state=NORMAL, relief=SOLID, textvariable=self.var_9, background='#f0f0f0')
            self.input_entry1.place(x=50, y=370)

            canvas = Canvas(self.download_win, height=377, width=3, bg='#afc2e9')
            canvas.place(x=285, y=36)
            canvas.create_line(300, 35, 300, 200, dash=(4, 2))

            label_1 = Label(self.download_win, text="Skip files larger than..", bg='#afc2e9', font=(None, 10))
            label_1.place(x=297, y=46)
            eg1 = Label(self.download_win, text="(1k to 44.6m)", bg='#afc2e9')
            eg1.place(x=453, y=65)

            self.input_entry2 = Entry(self.download_win, width=16, state=NORMAL, relief=SOLID, textvariable=self.var_10, background='#f0f0f0')
            self.input_entry2.place(x=443, y=49)

            label_2 = Label(self.download_win, text='Playlist item to start at..', bg='#afc2e9', font=(None, 10))
            label_2.place(x=297, y=89)
            eg2 = Label(self.download_win, text="(e.g 1 or 2)", bg='#afc2e9')
            eg2.place(x=464, y=111)

            self.input_entry3 = Entry(self.download_win, width=15, state=NORMAL, relief=SOLID, textvariable=self.var_11, background='#f0f0f0')
            self.input_entry3.place(x=448, y=93)

            label_3 = Label(self.download_win, text='Playlist item to end at..', bg='#afc2e9', font=(None, 10))
            label_3.place(x=297, y=129)

            self.input_entry4 = Entry(self.download_win, width=15, state=NORMAL, relief=SOLID, textvariable=self.var_12, background='#f0f0f0')
            self.input_entry4.place(x=448, y=133)

            label_4 = Label(self.download_win, text='Download speed in bytes/sec..', bg='#afc2e9', font=(None, 10))
            label_4.place(x=297, y=169)

            download_speed_opts = [
                '50K',
                '50K',
                '150K',
                '250K',
                '350K',
                '450K',
                '650K',
                '850K',
                '1.5M',
                '2.5M',
                '3.5M',
                '4.2M'
            ]

            download_speed = ttk.OptionMenu(self.download_win, self.var_13, *download_speed_opts, command=self.option_update_apply_btn)
            download_speed.place(x=485, y=169)
            self.var_13.set(self.remember_speed)

            label_5 = Label(self.download_win, text='Name of external downloader..', bg='#afc2e9', font=(None, 10))
            label_5.place(x=297, y=209)

            downloader_opts = [
                'Default',
                'Default',
                'aria2c',
                'axel',
                'curl',
                'httpie',
                'wget'
            ]

            downloader = ttk.OptionMenu(self.download_win, self.var_14, *downloader_opts, command=self.option_update_apply_btn)
            downloader.place(x=477, y=209)
            self.var_14.set(self.remember_downloader)

            label_7 = Label(self.download_win, text='Location of the ffmpeg/avconv binary:', bg='#afc2e9')
            label_7.place(x=320, y=260)

            self.ffmpeg_location = Entry(self.download_win, width=34, state=DISABLED, relief=SOLID, textvariable=self.var_15)
            self.ffmpeg_location.place(x=314, y=290)

            if not config_detail['dont_save_download_options']:
                self.var_1.set(download_detail['prefer_avconv'])
                self.var_2.set(download_detail['hls_prefer_native'])
                self.var_3.set(download_detail['nopart'])
                self.var_4.set(download_detail['include_ads'])
                self.var_5.set(download_detail['keep_fragments'])
                self.var_6.set(download_detail['playlistrandom'])
                self.var_8.set(download_detail['noplaylist'])
                self.var_7.set(download_detail['playlistreverse'])
                self.input_entry1.delete(0, END)
                self.input_entry1.insert(0, download_detail['playlist_items'])
                self.input_entry2.delete(0, END)
                self.input_entry2.insert(0, download_detail['max_filesize'])
                self.input_entry3.delete(0, END)
                self.input_entry3.insert(0, download_detail['playliststart'])
                self.input_entry4.delete(0, END)
                self.input_entry4.insert(0, download_detail['playlistend'])
                self.var_13.set(download_detail['ratelimit'])
                self.var_14.set(download_detail['external_downloader'])
                self.ffmpeg_location.configure(state=NORMAL)
                self.ffmpeg_location.delete(0, END)
                self.ffmpeg_location.insert(0, download_detail['ffmpeg_location'])
                self.ffmpeg_location.configure(state=DISABLED)
                self.apply_btn.configure(state=ACTIVE)

            def delete_input_cmd():
                self.apply_btn.configure(state=ACTIVE)
                self.ffmpeg_location.configure(state=NORMAL)
                self.ffmpeg_location.delete(0, END)
                self.ffmpeg_location.configure(state=DISABLED)
                self.isSaved = False

            def delete_input_cmd2():
                self.apply_btn.configure(state=ACTIVE)
                self.input_entry1.delete(0, END)
                self.isSaved = False

            def on_press():
                with open(setting.name_of_json) as f:
                    data = json.load(f)

                for key, value in data.items():
                    if key == 'settings':
                        for general_name, general_detail in value[0].items():
                            pass

                if len(self.var_15.get()) <= 1:
                    ask = filedialog.askopenfilename(initialdir=general_detail['initialdir'], filetypes=(("Executable Files (.exe)", "*.exe"), ("", "*.exe")), parent=self.download_win)

                elif len(self.var_15.get()) >= 2:
                    ask = filedialog.askopenfilename(initialdir=self.var_15.get(), filetypes=(("Executable Files (.exe)", "*.exe"), ("", "*.exe")), parent=self.download_win)
                self.apply_btn.configure(state=ACTIVE)
                self.ffmpeg_location.configure(state=NORMAL)
                self.ffmpeg_location.delete(0, END)
                self.ffmpeg_location.insert(0, ask)
                self.ffmpeg_location.configure(state=DISABLED)
                self.isSaved = False

            global img
            img = ImageTk.PhotoImage(Image.open('images/#delete_18px.png'))
            delete_input = ttk.Button(self.download_win, image=img, command=delete_input_cmd)
            delete_input.place(x=526, y=290)

            delete_input2 = ttk.Button(self.download_win, image=img, command=delete_input_cmd2)
            delete_input2.place(x=249, y=370)

            browse_ffmpeg = ttk.Button(self.download_win, text="Browse", style='some.TButton', command=on_press)
            browse_ffmpeg.place(x=380, y=312)

            def handleReturn(event):
                self.apply_btn.configure(state=ACTIVE)
                self.isSaved = False
                self.input_entry1_saved = False

            def handleReturn2(event):
                self.apply_btn.configure(state=ACTIVE)
                self.isSaved = False
                self.input_entry2_saved = False

            def handleReturn3(event):
                self.apply_btn.configure(state=ACTIVE)
                self.isSaved = False
                self.input_entry3_saved = False

            def handleReturn4(event):
                self.apply_btn.configure(state=ACTIVE)
                self.isSaved = False
                self.input_entry4_saved = False

            self.input_entry1.bind("<Key>", handleReturn)
            self.input_entry2.bind("<Key>", handleReturn2)
            self.input_entry3.bind("<Key>", handleReturn3)
            self.input_entry4.bind("<Key>", handleReturn4)

            for index, var in enumerate(_stabalize):
                _stabalize[index] += 1
            print(_stabalize)
        else:
            pass

    def download_apply(self):
        self.isSaved = True
        self.input_entry1_saved = True
        self.input_entry2_saved = True
        self.input_entry3_saved = True
        self.input_entry4_saved = True
        self.apply_btn.configure(state=DISABLED)

        self.remember_speed = self.var_13.get()
        self.remember_downloader = self.var_14.get()

        with open(setting.name_of_json) as f:
            data = json.load(f)

        for key, value in data.items():
            if key == 'options':
                for download_name, download_detail in value[1].items():
                    pass
            if key == 'settings':
                for config_name, config_detail in value[2].items():
                    pass

        if self.var_1.get():
            video_ops.update(prefer_ffmpeg=False)
        else:
            video_ops.update(prefer_ffmpeg=True)
            video_ops.pop('prefer_ffmpeg')

        if self.var_2.get():
            video_ops.update(hls_prefer_native=True)
        else:
            video_ops.update(hls_prefer_native=False)
            video_ops.pop('hls_prefer_native')

        if self.var_3.get():
            video_ops.update(nopart=True)
        else:
            video_ops.update(nopart=False)
            video_ops.pop('nopart')

        if self.var_4.get():
            video_ops.update(include_ads=True)
        else:
            video_ops.update(include_ads=False)
            video_ops.pop('include_ads')

        if self.var_5.get():
            video_ops.update(keep_fragments=True)
        else:
            video_ops.update(keep_fragments=False)
            video_ops.pop('keep_fragments')

        if self.var_6.get():
            video_ops.update(playlistrandom=True)
        else:
            video_ops.update(playlistrandom=False)
            video_ops.pop('playlistrandom')

        if self.var_7.get():
            video_ops.update(playlistreverse=True)
        else:
            video_ops.update(playlistreverse=False)
            video_ops.pop('playlistreverse')

        if self.var_8.get():
            video_ops.update(noplaylist=True)
        else:
            video_ops.update(noplaylist=False)
            video_ops.pop('noplaylist')

        if len(self.var_9.get()) <= 0:
            video_ops.update(playlist_items=None)
            video_ops.pop('playlist_items')
        else:
            for letter in self.var_9.get():
                if letter.lower() in string.ascii_letters + ';:@~#]{[}_()*^%$£"!¬`?/>.<':
                    if self.count == 1:
                        messagebox.showerror("???", "Invalid response for Specific Playlist section.\nEXAMPLE: 1-5,9,12 will download 1 up to 5 and 9 and 12", parent=self.download_win)
                        self.count += 1
                    video_ops.update(playlist_items=None)
                    video_ops.pop('playlist_items')
                    self.input_entry1.delete(0, END)
                else:
                    count1 = letter.count('-')
                    count2 = letter.count(',')
                    count3 = letter.count('1')
                    count4 = letter.count('2')
                    count5 = letter.count('3')
                    count6 = letter.count('4')
                    count7 = letter.count('5')
                    count8 = letter.count('6')
                    count9 = letter.count('7')
                    count10 = letter.count('8')
                    count11 = letter.count('9')
                    count12 = letter.count('0')
                    if count1 >= 1 \
                            or count2 >= 1\
                            or count3 >= 1\
                            or count4 >= 1\
                            or count5 >= 1\
                            or count6 >= 1\
                            or count7 >= 1\
                            or count8 >= 1\
                            or count9 >= 1\
                            or count10 >= 1\
                            or count11 >= 1\
                            or count12 >= 1:
                        video_ops.update(playlist_items=self.var_9.get())
                    else:
                        if self.count == 1:
                            messagebox.showerror("???", "Invalid response for Specific Playlist section.\nEXAMPLE: 1-5,9,12 will download 1 up to 5 and 9 and 12", parent=self.download_win)
                            self.count += 1
                        video_ops.update(playlist_items=None)
                        video_ops.pop('playlist_items')
            self.count = 1

        if len(self.var_10.get()) <= 1:
            video_ops.update(max_filesize=None)
            video_ops.pop('max_filesize')
            self.input_entry2.delete(0, END)
        else:
            if self.var_10.get().startswith(('1', '2', '3', '4', '5', '6', '7', '8', '9', '0')):
                if self.var_10.get().endswith("k"):
                    video_ops.update(max_filesize=self.var_10.get())

                elif self.var_10.get().endswith("m"):
                    video_ops.update(max_filesize=self.var_10.get())

                else:
                    if self.count == 1:
                        messagebox.showerror("???", "Max Filesize ERROR: Can only use integers with a \"k\" or \"m\" on the end. Ones with 'm' may contain up to 2 decimals."
                                                    "\nEXAMPLE: 10k .. 2.5m .. 135k .. 44.6m .. 54k .. 14.95m", parent=self.download_win)
                        self.count += 1
                    video_ops.update(max_filesize=None)
                    video_ops.pop('max_filesize')
                    self.input_entry2.delete(0, END)
            else:
                if self.count == 1:
                    messagebox.showerror("???", "Max Filesize ERROR: Can only use integers with a \"k\" or \"m\" on the end. Ones with 'm' may contain up to 2 decimals."
                                                "\nEXAMPLE: 10k .. 2.5m .. 135k .. 44.6m .. 54k .. 14.95m", parent=self.download_win)
                    self.count += 1
                video_ops.update(max_filesize=None)
                video_ops.pop('max_filesize')
                self.input_entry2.delete(0, END)

        if len(self.var_11.get()) <= 0:
            video_ops.update(playliststart=None)
            video_ops.pop('playliststart')
            self.input_entry3.delete(0, END)
        else:
            if self.var_11.get().startswith(('1', '2', '3', '4', '5', '6', '7', '8', '9', '0')):
                if self.var_11.get().endswith(('1', '2', '3', '4', '5', '6', '7', '8', '9', '0')):
                    if self.var_11.get().isnumeric():
                        video_ops.update(playliststart=self.var_11.get())
                    else:
                        if self.count == 1:
                            messagebox.showerror("???", "Error on Start Playlist section.\nYou can only use integers.", parent=self.download_win)
                            self.count += 1
                        video_ops.update(playliststart=None)
                        video_ops.pop('playliststart')
                        self.input_entry3.delete(0, END)
                else:
                    if self.count == 1:
                        messagebox.showerror("???", "Error on Start Playlist section.\nYou can only use integers.", parent=self.download_win)
                        self.count += 1
                    video_ops.update(playliststart=None)
                    video_ops.pop('playliststart')
                    self.input_entry3.delete(0, END)
            else:
                if self.count == 1:
                    messagebox.showerror("???", "Error on Start Playlist section.\nYou can only use integers.", parent=self.download_win)
                    self.count += 1
                video_ops.update(playliststart=None)
                video_ops.pop('playliststart')
                self.input_entry3.delete(0, END)

        if len(self.var_12.get()) <= 0:
            video_ops.update(playlistend=None)
            video_ops.pop('playlistend')
            self.input_entry4.delete(0, END)
        else:
            if self.var_12.get().startswith(('1', '2', '3', '4', '5', '6', '7', '8', '9', '0')):
                if self.var_12.get().endswith(('1', '2', '3', '4', '5', '6', '7', '8', '9', '0')):
                    if self.var_12.get().isnumeric():
                        video_ops.update(playlistend=self.var_12.get())
                    else:
                        if self.count == 1:
                            messagebox.showerror("???", "Error on End Playlist section.\nYou can only use integers.", parent=self.download_win)
                            self.count += 1
                        video_ops.update(playlistend=None)
                        video_ops.pop('playlistend')
                        self.input_entry4.delete(0, END)
                else:
                    if self.count == 1:
                        messagebox.showerror("???", "Error on End Playlist section.\nYou can only use integers.", parent=self.download_win)
                        self.count += 1
                    video_ops.update(playlistend=None)
                    video_ops.pop('playlistend')
                    self.input_entry4.delete(0, END)
            else:
                if self.count == 1:
                    messagebox.showerror("???", "Error on End Playlist section.\nYou can only use integers.", parent=self.download_win)
                    self.count += 1
                video_ops.update(playlistend=None)
                video_ops.pop('playlistend')
                self.input_entry4.delete(0, END)

        if self.var_13.get() == '4.2M':
            video_ops.update(ratelimit=None)
            video_ops.pop('ratelimit')
        else:
            video_ops.update(ratelimit=self.var_13.get())

        if self.var_14.get() == 'Default':
            video_ops.update(external_downloader=None)
            video_ops.pop('external_downloader')
        else:
            video_ops.update(external_downloader=self.var_14.get())

        if len(self.var_15.get()) <= 2:
            video_ops.update(ffmpeg_location=None)
            video_ops.pop('ffmpeg_location')
        else:
            video_ops.update(ffmpeg_location=self.var_15.get())

        if not config_detail['dont_save_download_options']:
            download_detail['prefer_ffmpeg'] = self.var_1.get()
            download_detail['hls_prefer_native'] = self.var_2.get()
            download_detail['nopart'] = self.var_3.get()
            download_detail['include_ads'] = self.var_4.get()
            download_detail['keep_fragments'] = self.var_5.get()
            download_detail['playlistrandom'] = self.var_6.get()
            download_detail['noplaylist'] = self.var_8.get()
            download_detail['playlistreverse'] = self.var_7.get()
            download_detail['playlist_items'] = self.input_entry1.get()
            download_detail['max_filesize'] = self.input_entry2.get()
            download_detail['playliststart'] = self.input_entry3.get()
            download_detail['playlistend'] = self.input_entry4.get()
            download_detail['ratelimit'] = self.var_13.get()
            download_detail['external_downloader'] = self.var_14.get()
            download_detail['ffmpeg_location'] = self.ffmpeg_location.get()
            with open(setting.name_of_json, 'w') as f:
                json.dump(data, f, indent=3)
                f.close()
        else:
            download_detail['prefer_ffmpeg'] = False
            download_detail['hls_prefer_native'] = False
            download_detail['nopart'] = False
            download_detail['include_ads'] = False
            download_detail['keep_fragments'] = False
            download_detail['playlistrandom'] = False
            download_detail['noplaylist'] = False
            download_detail['playlistreverse'] = False
            download_detail['playlist_items'] = ""
            download_detail['max_filesize'] = ""
            download_detail['playliststart'] = ""
            download_detail['playlistend'] = ""
            download_detail['ratelimit'] = "4.2M"
            download_detail['external_downloader'] = "Default"
            download_detail['ffmpeg_location'] = ""
            with open(setting.name_of_json, 'w') as f:
                json.dump(data, f, indent=3)
                f.close()

        self.storage1 = self.input_entry1.get()
        self.storage2 = self.input_entry2.get()
        self.storage3 = self.input_entry3.get()
        self.storage4 = self.input_entry4.get()
        self.count = 1
        sys.stderr = sys.__stderr__
        sys.stdout = sys.__stdout__
        print(video_ops, "DOWNLOAD OPTIONS", sep="   ", end="\n\n")

###############################################################################################################

class OtherOptionWindow(object):
    """
    * Other Options
    """
    def __init__(self):
        self._title = 'Other Options   |   Gloryness  |  v{}'.format(__version__)
        self._icon = 'images/#app.ico'
        self._size = '600x450'
        self.apply_btn = None
        self.other_win = None
        self.var_1, self.var_2, self.var_3, self.var_4 = \
            StringVar(), StringVar(), StringVar(), StringVar()

        self.var1, self.var2, self.var3, self.var4, self.var5 = \
            BooleanVar(), BooleanVar(), BooleanVar(), BooleanVar(), BooleanVar()

        self.var_5, self.var_6, self.var_7, self.var_8, self.var_9, self.var_10, self.var_11, self.var_12,\
            self.var_13, self.var_14, self.var_15, self.var_16, self.var_17, self.var_18, self.var_19, self.var_20, self.var_21= \
            BooleanVar(), BooleanVar(), BooleanVar(), BooleanVar(), BooleanVar(), BooleanVar(), StringVar(), StringVar(), \
            StringVar(), BooleanVar(), BooleanVar(), BooleanVar(), BooleanVar(), BooleanVar(), BooleanVar(), StringVar(), DoubleVar()

        self.username_entry = None
        self.twofactor_entry = None
        self.password_entry = None
        self.videopass_entry = None

        self.count = 1

        self.age_limit_entry = None
        self.min_views_entry = None
        self.max_views_entry = None
        self.max_downloads_entry = None
        self.time_between_entry = None

        self.isSaved = False
        self.username_saved = False
        self.twofactor_saved = False
        self.password_saved = False
        self.videopass_saved = False
        self.age_limit_saved = False
        self.min_views_saved = False
        self.max_views_saved = False
        self.max_download_saved = False
        self.time_between_saved = True

        self.username_storage = ''
        self.twofactor_storage = ''
        self.password_storage = ''
        self.videopass_storage = ''
        self.age_limit_storage = ''
        self.min_views_storage = ''
        self.max_views_storage = ''
        self.max_download_storage = ''
        self.time_between_storage = ''

    def on_other_options(self):
        other_options_thread = threading.Thread(target=self.other_options_window)
        other_options_thread.start()

    def hold_saved_variables(self):
        if not self.isSaved:
            if not self.username_saved:
                self.username_entry.configure(state=NORMAL)
                self.username_entry.delete(0, END)
                self.var_1.set(self.username_storage)
                self.username_entry.configure(state=DISABLED)

            if not self.twofactor_saved:
                self.twofactor_entry.configure(state=NORMAL)
                self.twofactor_entry.delete(0, END)
                self.var_2.set(self.twofactor_storage)
                self.twofactor_entry.configure(state=DISABLED)

            if not self.password_saved:
                self.password_entry.configure(state=NORMAL)
                self.password_entry.delete(0, END)
                self.var_3.set(self.password_storage)
                self.password_entry.configure(state=DISABLED)

            if not self.videopass_saved:
                self.videopass_entry.configure(state=NORMAL)
                self.videopass_entry.delete(0, END)
                self.var_4.set(self.videopass_storage)
                self.videopass_entry.configure(state=DISABLED)

            if not self.age_limit_saved:
                self.age_limit_entry.delete(0, END)
                self.var_11.set(self.age_limit_storage)

            if not self.min_views_saved:
                self.min_views_entry.delete(0, END)
                self.var_12.set(self.min_views_storage)

            if not self.max_views_saved:
                self.max_views_entry.delete(0, END)
                self.var_13.set(self.max_views_storage)

            if not self.max_download_saved:
                self.max_downloads_entry.delete(0, END)
                self.var_20.set(self.max_download_storage)

            if not self.time_between_saved:
                self.time_between_entry.delete(0, END)
                self.var_21.set(self.time_between_storage)

        if self.isSaved:
            pass

    def hold_variables(self):
        state = str(self.apply_btn['state'])
        if state == 'disabled':
            self.other_win.destroy()
        else:
            responce = messagebox.askquestion("Are You Sure?", "You have made unsaved changed, are you sure you want to exit?", parent=self.other_win)
            if responce == 'yes':
                self.hold_saved_variables()
                self.other_win.destroy()
            else:
                pass

    def other_options_window(self):
        global _stabalize
        if _stabalize[2] == 1:
            with open(setting.name_of_json) as f:
                data = json.load(f)

            for key, value in data.items():
                if key == 'options':
                    for other_name, other_detail in value[2].items():
                        pass
                if key == 'settings':
                    for config_name, config_detail in value[2].items():
                        pass
            download_btn.configure(state=DISABLED)
            self.other_win = Toplevel()
            self.other_win.title(self._title)
            self.other_win.iconbitmap(self._icon)
            self.other_win.resizable(False, False)
            self.other_win.configure(bg='#cbdbfc', bd=5)
            self.other_win.geometry(self._size)
            self.other_win.protocol("WM_DELETE_WINDOW", lambda: reset_other_window(self.other_win))

            border = LabelFrame(self.other_win, height=425, width=560, bg='#cbdbfc', bd=2, text="Other Options", font="Cooper 18", labelanchor=N, relief=SOLID)
            border.place(x=15, y=7)

            in_border1 = Frame(self.other_win, height=120, width=534, bg='#afc2e9')  # frame 1
            in_border1.place(x=29, y=34)

            in_border2 = Frame(self.other_win, height=120, width=534, bg='#afc2e9')  # frame 2
            in_border2.place(x=29, y=168)

            in_border3 = Frame(self.other_win, height=115, width=534, bg='#afc2e9')  # frame 3
            in_border3.place(x=29, y=302)

            auth = Label(self.other_win, text="Authentication", font=(None, 14), bg='#afc2e9')
            auth.place(x=240, y=35)

            general = Label(self.other_win, text="General", font=(None, 13), bg='#afc2e9')
            general.place(x=160, y=44)

            video = Label(self.other_win, text="Video", font=(None, 13), bg='#afc2e9')
            video.place(x=420, y=44)

            username = Label(self.other_win, text="Username:", font=(None, 10), bg='#afc2e9')
            username.place(x=38, y=65)

            twofactor = Label(self.other_win, text="Two-factor:", font=(None, 10), bg='#afc2e9')
            twofactor.place(x=38, y=95)

            password = Label(self.other_win, text="Password:", font=(None, 10), bg='#afc2e9')
            password.place(x=38, y=125)

            vid_password = Label(self.other_win, text="Password:", font=(None, 10), bg='#afc2e9')
            vid_password.place(x=325, y=65)

            exit_btn = ttk.Button(self.other_win, text="Exit", style='option.TButton', command=lambda: reset_other_window(self.other_win))
            exit_btn.place(x=440, y=415)

            self.apply_btn = ttk.Button(self.other_win, text="Apply", state=DISABLED, style='option.TButton', command=self.options_apply)
            self.apply_btn.place(x=510, y=415)

            self.username_entry = Entry(self.other_win, width=28, state=DISABLED, relief=SOLID, textvariable=self.var_1)
            self.username_entry.place(x=108, y=68)

            self.twofactor_entry = Entry(self.other_win, width=28, state=DISABLED, relief=SOLID, textvariable=self.var_2)
            self.twofactor_entry.place(x=108, y=98)

            self.password_entry = Entry(self.other_win, width=28, state=DISABLED, relief=SOLID, textvariable=self.var_3)
            self.password_entry.place(x=108, y=128)

            self.videopass_entry = Entry(self.other_win, width=23, state=DISABLED, relief=SOLID, textvariable=self.var_4)
            self.videopass_entry.place(x=394, y=66)

            style = ttk.Style()
            style.configure('TCheckbutton', background='#afc2e9')

            def update_auths(entry, var):
                self.apply_btn.configure(state=ACTIVE)
                if var.get():
                    entry.configure(state=NORMAL)
                elif not var.get():
                    entry.delete(0, END)
                    entry.configure(state=DISABLED)

            def update_apply_btn():
                self.apply_btn.configure(state=ACTIVE)

            confirm_username = ttk.Checkbutton(self.other_win, variable=self.var1, onvalue=True, offvalue=False,
                                               style='TCheckbutton', command=lambda: update_auths(self.username_entry, self.var1))
            confirm_username.place(x=284, y=66)

            confirm_twofactor = ttk.Checkbutton(self.other_win, variable=self.var2, onvalue=True, offvalue=False,
                                                style='TCheckbutton', command=lambda: update_auths(self.twofactor_entry, self.var2))
            confirm_twofactor.place(x=284, y=96)

            confirm_password = ttk.Checkbutton(self.other_win, variable=self.var3, onvalue=True, offvalue=False,
                                               style='TCheckbutton', command=lambda: update_auths(self.password_entry, self.var3))
            confirm_password.place(x=284, y=126)

            confirm_vidpassword = ttk.Checkbutton(self.other_win, variable=self.var4, onvalue=True, offvalue=False,
                                               style='TCheckbutton', command=lambda: update_auths(self.videopass_entry, self.var4))
            confirm_vidpassword.place(x=540, y=65)

            use_netrc = ttk.Checkbutton(self.other_win, text="Use .netrc for authentication instead", variable=self.var5, onvalue=True, offvalue=False,
                                                style='TCheckbutton', command=update_apply_btn)
            use_netrc.place(x=325, y=126)

            # .instate() will return True if ttk.Checkbutton is checked.

            if confirm_username.instate(['selected']):
                self.username_entry.configure(state=NORMAL)
            if confirm_twofactor.instate(['selected']):
                self.twofactor_entry.configure(state=NORMAL)
            if confirm_password.instate(['selected']):
                self.password_entry.configure(state=NORMAL)
            if confirm_vidpassword.instate(['selected']):
                self.videopass_entry.configure(state=NORMAL)

            style1 = ttk.Style()
            style1.configure('t.TCheckbutton', background='#afc2e9', font=(None, 9))

            restrictions = Label(self.other_win, text="Restrictions", font=(None, 14), bg='#afc2e9')
            restrictions.place(x=246, y=168)

            no_warnings = ttk.Checkbutton(self.other_win, text="Don't print out warnings", style='t.TCheckbutton',
                                          onvalue=True, offvalue=False, variable=self.var_5, command=update_apply_btn)
            no_warnings.place(x=36, y=199)

            no_download_video = ttk.Checkbutton(self.other_win, text="Do not download video", style='t.TCheckbutton',
                                                onvalue=True, offvalue=False, variable=self.var_6, command=update_apply_btn)
            no_download_video.place(x=36, y=232)

            no_stop_on_errors = ttk.Checkbutton(self.other_win, text="Don't stop on errors", style='t.TCheckbutton',
                                                onvalue=True, offvalue=False, variable=self.var_7, command=update_apply_btn)
            no_stop_on_errors.place(x=36, y=265)

            no_dash_formats = ttk.Checkbutton(self.other_win, text="Don't include DASH manifests\n(can reduce network I/O)", style='t.TCheckbutton',
                                          onvalue=True, offvalue=False, variable=self.var_8, command=update_apply_btn)
            no_dash_formats.place(x=196, y=194)

            dont_auto_resize_buffer = ttk.Checkbutton(self.other_win, text="Don't auto-resize download buffer", style='t.TCheckbutton',
                                                onvalue=True, offvalue=False, variable=self.var_9, command=update_apply_btn)
            dont_auto_resize_buffer.place(x=196, y=232)

            no_playlist_only_list = ttk.Checkbutton(self.other_win, text="Don't download a playlist, only list videos", style='t.TCheckbutton',
                                                onvalue=True, offvalue=False, variable=self.var_10, command=update_apply_btn)
            no_playlist_only_list.place(x=196, y=265)

            age_limit_label = Label(self.other_win, text="Age Limit:", font=(None, 9), bg='#afc2e9')
            age_limit_label.place(x=442, y=177)
            self.age_limit_entry = Entry(self.other_win, width=9, relief=SOLID, state=NORMAL, font=(None, 8), textvariable=self.var_11)
            self.age_limit_entry.place(x=504, y=179)

            min_views_label = Label(self.other_win, text="Min views:", font=(None, 9), bg='#afc2e9')
            min_views_label.place(x=442, y=217)
            self.min_views_entry = Entry(self.other_win, width=9, relief=SOLID, state=NORMAL, font=(None, 8), textvariable=self.var_12)
            self.min_views_entry.place(x=504, y=219)

            max_views_label = Label(self.other_win, text="Max views:", font=(None, 9), bg='#afc2e9')
            max_views_label.place(x=442, y=257)
            self.max_views_entry = Entry(self.other_win, width=9, relief=SOLID, state=NORMAL, font=(None, 8), textvariable=self.var_13)
            self.max_views_entry.place(x=504, y=259)

            style2 = ttk.Style()
            style2.configure('e.TCheckbutton', background='#afc2e9', font=(None, 9))

            other = Label(self.other_win, text="Other", font=(None, 14), bg='#afc2e9')
            other.place(x=266, y=302)

            only_match_titles = ttk.Checkbutton(self.other_win, text="Download only matching titles", style='e.TCheckbutton',
                                          onvalue=True, offvalue=False, variable=self.var_14, command=update_apply_btn)
            only_match_titles.place(x=36, y=327)

            reject_matching_titles = ttk.Checkbutton(self.other_win, text="Reject matching titles", style='e.TCheckbutton',
                                                onvalue=True, offvalue=False, variable=self.var_15, command=update_apply_btn)
            reject_matching_titles.place(x=36, y=360)

            delete_cache = ttk.Checkbutton(self.other_win, text="Delete all filesystem cache files", style='e.TCheckbutton',
                                                onvalue=True, offvalue=False, variable=self.var_16, command=update_apply_btn)
            delete_cache.place(x=36, y=393)

            verbose = ttk.Checkbutton(self.other_win, text="Print various debugging info", style='e.TCheckbutton',
                                              onvalue=True, offvalue=False, variable=self.var_17, command=update_apply_btn)
            verbose.place(x=234, y=327)

            keep_file = ttk.Checkbutton(self.other_win, text="Keep files after download", style='e.TCheckbutton',
                                                      onvalue=True, offvalue=False, variable=self.var_18, command=update_apply_btn)
            keep_file.place(x=234, y=360)

            no_check_certificate = ttk.Checkbutton(self.other_win, text="Suppress HTTPS validation", style='e.TCheckbutton',
                                                    onvalue=True, offvalue=False, variable=self.var_19, command=update_apply_btn)
            no_check_certificate.place(x=234, y=393)

            download_buffer_label = Label(self.other_win, text="Max downloads:", bg='#afc2e9', font=(None, 9))
            download_buffer_label.place(x=415, y=312)

            time_between_label = Label(self.other_win, text="Time between downloads:\n(secs):", bg='#afc2e9', font=(None, 9))
            time_between_label.place(x=408, y=356)

            self.max_downloads_entry = Entry(self.other_win, width=18, relief=SOLID, state=NORMAL, font=(None, 9), textvariable=self.var_20)
            self.max_downloads_entry.place(x=418, y=334)

            self.time_between_entry = Entry(self.other_win, width=18, relief=SOLID, state=NORMAL, font=(None, 9), textvariable=self.var_21)
            self.time_between_entry.place(x=418, y=390)
            if len(str(self.var_21.get())) <= 0 or self.var_21.get() == 0.0:
                self.time_between_entry.delete(0, END)
                self.time_between_entry.insert(0, 1.75)

            if not config_detail['dont_save_other_options']:
                key = b'BF9A3HUIkKn_lvrVJlhN4zUwWBIxj7jQaBCg3hkqBos='
                fernet = Fernet(key)
                self.username_entry.config(state=NORMAL)
                self.username_entry.delete(0, END)
                self.username_entry.insert(0, other_detail['username'])
                self.twofactor_entry.config(state=NORMAL)
                self.twofactor_entry.delete(0, END)
                self.twofactor_entry.insert(0, other_detail['twofactor'])
                self.password_entry.config(state=NORMAL)
                self.password_entry.delete(0, END)
                self.videopass_entry.config(state=NORMAL)
                self.videopass_entry.delete(0, END)
                if other_detail['password'] == "":
                    self.password_entry.insert(0, other_detail['password'])
                else:
                    self.password_entry.insert(0, fernet.decrypt(bytes(other_detail['password'].encode('utf-8'))).decode('utf-8'))

                if other_detail['videopassword'] == "":
                    self.videopass_entry.insert(0, other_detail['videopassword'])
                else:
                    self.videopass_entry.insert(0, fernet.decrypt(bytes(other_detail['videopassword'].encode('utf-8'))).decode('utf-8'))

                if other_detail['username'] != "":
                    self.var1.set(True)
                else:
                    self.username_entry.configure(state=DISABLED)
                if other_detail['twofactor'] != "":
                    self.var2.set(True)
                else:
                    self.twofactor_entry.configure(state=DISABLED)
                if other_detail['password'] != "":
                    self.var3.set(True)
                else:
                    self.password_entry.configure(state=DISABLED)
                if other_detail['videopassword'] != "":
                    self.var4.set(True)
                else:
                    self.videopass_entry.configure(state=DISABLED)
                self.var5.set(other_detail['netrc'])
                self.var_5.set(other_detail['no_warnings'])
                self.var_6.set(other_detail['skip_download'])
                self.var_7.set(other_detail['ignoreerrors'])
                self.var_8.set(other_detail['youtube_include_dash_manifest'])
                self.var_9.set(other_detail['noresizebuffer'])
                self.var_10.set(other_detail['extract_flat'])
                self.age_limit_entry.delete(0, END)
                self.min_views_entry.delete(0, END)
                self.max_views_entry.delete(0, END)
                self.age_limit_entry.insert(0, other_detail['age_limit'])
                self.min_views_entry.insert(0, other_detail['min_views'])
                self.max_views_entry.insert(0, other_detail['max_views'])
                self.var_14.set(other_detail['matchtitle'])
                self.var_15.set(other_detail['rejecttitle'])
                self.var_16.set(other_detail['rm_cachedir'])
                self.var_17.set(other_detail['verbose'])
                self.var_18.set(other_detail['keepvideo'])
                self.var_19.set(other_detail['no_check_certificate'])
                self.max_downloads_entry.delete(0, END)
                self.time_between_entry.delete(0, END)
                self.max_downloads_entry.insert(0, other_detail['max_downloads'])
                self.time_between_entry.insert(0, other_detail['time_between_downloads'])
                if not self.var5.get() and not self.var_5.get() and not self.var_6.get() and not self.var_7.get() and not self.var_8.get() and not self.var_9.get() \
                    and not self.var_10.get() and not self.var_14.get() and not self.var_15.get() and not self.var_16.get() and not self.var_17.get() \
                    and not self.var_18.get() and not self.var_19.get():
                        pass
                else:
                    self.apply_btn.configure(state=NORMAL)

            def handleReturn(event):
                self.apply_btn.configure(state=ACTIVE)
                self.isSaved = False
            def handleReturn1(event):
                self.apply_btn.configure(state=ACTIVE)
                self.username_saved = False
                self.isSaved = False
            def handleReturn2(event):
                self.apply_btn.configure(state=ACTIVE)
                self.twofactor_saved = False
                self.isSaved = False
            def handleReturn3(event):
                self.apply_btn.configure(state=ACTIVE)
                self.password_saved = False
                self.isSaved = False
            def handleReturn4(event):
                self.apply_btn.configure(state=ACTIVE)
                self.videopass_saved = False
                self.isSaved = False
            def handleReturn5(event):
                self.apply_btn.configure(state=ACTIVE)
                self.age_limit_saved = False
                self.isSaved = False
            def handleReturn6(event):
                self.apply_btn.configure(state=ACTIVE)
                self.min_views_saved = False
                self.isSaved = False
            def handleReturn7(event):
                self.apply_btn.configure(state=ACTIVE)
                self.max_views_saved = False
                self.isSaved = False
            def handleReturn8(event):
                self.apply_btn.configure(state=ACTIVE)
                self.max_download_saved = False
                self.isSaved = False
            def handleReturn9(event):
                self.apply_btn.configure(state=ACTIVE)
                self.time_between_saved = False
                self.isSaved = False

            self.username_entry.bind("<Key>", handleReturn1)
            self.twofactor_entry.bind("<Key>", handleReturn2)
            self.password_entry.bind("<Key>", handleReturn3)
            self.videopass_entry.bind("<Key>", handleReturn4)
            self.age_limit_entry.bind("<Key>", handleReturn5)
            self.min_views_entry.bind("<Key>", handleReturn6)
            self.max_views_entry.bind("<Key>", handleReturn7)
            self.max_downloads_entry.bind("<Key>", handleReturn8)
            self.time_between_entry.bind("<Key>", handleReturn9)

            for index, var in enumerate(_stabalize):
                _stabalize[index] += 1
            print(_stabalize)

        else:
            pass

    def options_apply(self):
        self.isSaved = True
        self.username_saved = True
        self.twofactor_saved = True
        self.password_saved = True
        self.videopass_saved = True
        self.age_limit_saved = True
        self.min_views_saved = True
        self.max_views_saved = True
        self.max_download_saved = True
        self.time_between_saved = True
        self.username_storage = self.var_1.get()
        self.twofactor_storage = self.var_2.get()
        self.password_storage = self.var_3.get()
        self.videopass_storage = self.var_4.get()
        self.age_limit_storage = self.var_11.get()
        self.min_views_storage = self.var_12.get()
        self.max_views_storage = self.var_13.get()
        self.max_download_storage = self.var_20.get()
        try:
            if len(str(self.var_21.get())) <= 0:
                self.var_21.set(1.75)
            self.time_between_storage = self.var_21.get()
        except:
            self.var_21.set(1.75)

        with open(setting.name_of_json) as f:
            data = json.load(f)

        for key, value in data.items():
            if key == 'options':
                for other_name, other_detail in value[2].items():
                    pass
            if key == 'settings':
                for config_name, config_detail in value[2].items():
                    pass

        if self.var1.get(): # Username
            if len(self.var_1.get()) <= 0:
                video_ops.update(username=None)
                video_ops.pop('username')
            else:
                video_ops.update(username=self.var_1.get())
        else:
            video_ops.update(username=None)
            video_ops.pop('username')

        if self.var2.get(): # Two-Factor
            if len(self.var_2.get()) <= 0:
                video_ops.update(twofactor=None)
                video_ops.pop('twofactor')
            else:
                for letter in self.var_2.get():
                    if letter.lower() in string.ascii_letters + ';:@~#]{[}_()*^%$£"!¬`?/>.<':
                        if self.count == 1:
                            messagebox.showwarning("???", "Two-Factor can be digit-only.", parent=self.other_win)
                            video_ops.update(twofactor=None)
                            video_ops.pop('twofactor')
                            self.count = 2
                        else:
                            pass
                    else:
                        num = 0
                        t = []

                        for i in range(len(string.ascii_lowercase)):
                            t.append(string.ascii_lowercase[num])
                            num += 1

                        if self.var_2.get().lower().startswith(tuple(t)):
                            video_ops.update(twofactor=None)
                            video_ops.pop('twofactor')
                        else:
                            video_ops.update(twofactor=self.var_2.get())
            self.count = 1
        else:
            video_ops.update(twofactor=None)
            video_ops.pop('twofactor')

        if self.var3.get(): # Password
            if len(self.var_3.get()) <= 0:
                video_ops.update(password=None)
                video_ops.pop('password')
            else:
                video_ops.update(password=self.var_3.get())
        else:
            video_ops.update(password=None)
            video_ops.pop('password')

        if self.var4.get(): # Video Password
            if len(self.var_4.get()) <= 0:
                video_ops.update(videopassword=None)
                video_ops.pop('videopassword')
            else:
                video_ops.update(videopassword=self.var_4.get())
        else:
            video_ops.update(videopassword=None)
            video_ops.pop('videopassword')

        if self.var5.get(): # Use .netrc
            video_ops.update(usenetrc=True)
        else:
            video_ops.update(usenetrc=None)
            video_ops.pop('usenetrc')

        if self.var_5.get(): # Don't print out warnings
            video_ops.update(no_warnings=True)
        else:
            video_ops.update(no_warnings=None)
            video_ops.pop('no_warnings')

        if self.var_6.get(): # Do not download video
            video_ops.update(skip_download=True)
        else:
            video_ops.update(skip_download=None)
            video_ops.pop('skip_download')

        if self.var_7.get(): # Don't stop on errors
            video_ops.update(ignoreerrors=True)
        else:
            video_ops.update(ignoreerrors=None)
            video_ops.pop('ignoreerrors')

        if self.var_8.get(): # Don't include DASH manifests
            video_ops.update(youtube_include_dash_manifest=False)
        else:
            video_ops.update(youtube_include_dash_manifest=None)
            video_ops.pop('youtube_include_dash_manifest')

        if self.var_9.get(): # Don't auto-resize the download buffer
            video_ops.update(noresizebuffer=True)
        else:
            video_ops.update(noresizebuffer=None)
            video_ops.pop('noresizebuffer')

        if self.var_10.get(): # Don't download a playlist, only list the videos.
            video_ops.update(extract_flat=True)
        else:
            video_ops.update(extract_flat=None)
            video_ops.pop('extract_flat')

        if self.var_14.get(): # Download only matching titles
            video_ops.update(matchtitle=True)
        else:
            video_ops.update(matchtitle=None)
            video_ops.pop('matchtitle')

        if self.var_15.get(): # Reject matching titles
            video_ops.update(rejecttitle=True)
        else:
            video_ops.update(rejecttitle=None)
            video_ops.pop('rejecttitle')

        if self.var_16.get(): # Delete all filesystem cache files
            video_ops.update(rm_cachedir=True)
        else:
            video_ops.update(rm_cachedir=None)
            video_ops.pop('rm_cachedir')

        if self.var_17.get(): # Print various debugging info
            video_ops.update(verbose=True)
        else:
            video_ops.update(verbose=None)
            video_ops.pop('verbose')

        if self.var_18.get(): # Keep files after download
            video_ops.update(keepvideo=True)
        else:
            video_ops.update(keepvideo=None)
            video_ops.pop('keepvideo')

        if self.var_19.get(): # Suppress HTTPS certificate validation
            video_ops.update(nocheckcertificate=True)
        else:
            video_ops.update(nocheckcertificate=None)
            video_ops.pop('nocheckcertificate')

        if len(self.var_11.get()) <= 0: # Age limit
            video_ops.update(age_limit=None)
            video_ops.pop('age_limit')
        else:
            if self.var_11.get().isnumeric():
                video_ops.update(age_limit=int(self.var_11.get()))
            else:
                messagebox.showwarning("???", "AGE LIMIT: You must have numeric characters only.", parent=self.other_win)
                video_ops.update(age_limit=None)
                video_ops.pop('age_limit')

        if len(self.var_12.get()) <= 0: # Min views
            video_ops.update(min_views=None)
            video_ops.pop('min_views')
        else:
            if self.var_12.get().isnumeric():
                video_ops.update(min_views=int(self.var_12.get()))
            else:
                messagebox.showwarning("???", "MIN VIEWS: You must have numeric characters only.", parent=self.other_win)
                video_ops.update(min_views=None)
                video_ops.pop('min_views')

        if len(self.var_13.get()) <= 0: # Max views
            video_ops.update(max_views=None)
            video_ops.pop('max_views')
        else:
            if self.var_13.get().isnumeric():
                video_ops.update(max_views=int(self.var_13.get()))
            else:
                messagebox.showwarning("???", "MAX VIEWS: You must have numeric characters only.", parent=self.other_win)
                video_ops.update(max_views=None)
                video_ops.pop('max_views')

        global max_downloads
        if len(self.var_20.get()) <= 0: # Max downloads
            max_downloads = infinity
        else:
            if self.var_20.get().isnumeric():
                max_downloads = int(self.var_20.get())
            else:
                messagebox.showwarning("???", "MAX DOWNLOADS: You must have numeric characters only.")

        def after_test():
            self.time_between_entry.delete(0, END)
            self.time_between_entry.insert(0, 1.75)
        try:
            if len(str(self.var_21.get())) <= 0 or self.var_21.get() < 0.50: # Time between downloads
                self.time_between_entry.delete(0, END)
                self.time_between_entry.insert(0, "0.50 or over.")
                self.time_between_entry.after(1400, func=after_test)
            else:
                if self.var_21.get():
                    global wait_time
                    wait_time = float(self.var_21.get()) # changing value of wait_time
                else:
                    messagebox.showwarning("???", "TIME BETWEEN: Can only include a float (1.0, 1.00).", parent=self.other_win)
        except TclError:
            messagebox.showwarning("???", "TIME BETWEEN: Can only include a float (1.0, 1.00).", parent=self.other_win)

        if not config_detail['dont_save_other_options']:
            key = b'BF9A3HUIkKn_lvrVJlhN4zUwWBIxj7jQaBCg3hkqBos='
            fernet = Fernet(key)

            other_detail['username'] = self.username_entry.get()
            other_detail['twofactor'] = self.twofactor_entry.get()
            if self.var_3.get() == "":
                other_detail['password'] = ""
            else:
                other_detail['password'] = fernet.encrypt(bytes(self.var_3.get().encode('utf-8'))).decode('utf-8')
            if self.var_4.get() == "":
                other_detail['videopassword'] = ""
            else:
                other_detail['videopassword'] = fernet.encrypt(bytes(self.var_4.get().encode('utf-8'))).decode('utf-8')
            other_detail['netrc'] = self.var5.get()
            other_detail['no_warnings'] = self.var_5.get()
            other_detail['skip_download'] = self.var_6.get()
            other_detail['ignoreerrors'] = self.var_7.get()
            other_detail['youtube_include_dash_manifest'] = self.var_8.get()
            other_detail['noresizebuffer'] = self.var_9.get()
            other_detail['extract_flat'] = self.var_10.get()
            other_detail['age_limit'] = self.var_11.get()
            other_detail['min_views'] = self.var_12.get()
            other_detail['max_views'] = self.var_13.get()
            other_detail['matchtitle'] = self.var_14.get()
            other_detail['rejecttitle'] = self.var_15.get()
            other_detail['rm_cachedir'] = self.var_16.get()
            other_detail['verbose'] = self.var_17.get()
            other_detail['keepvideo'] = self.var_18.get()
            other_detail['no_check_certificate'] = self.var_19.get()
            other_detail['max_downloads'] = self.var_20.get()
            other_detail['time_between_downloads'] = self.var_21.get()
            with open(setting.name_of_json, 'w') as f:
                json.dump(data, f, indent=3)
                f.close()
        else:
            other_detail['username'] = ""
            other_detail['twofactor'] = ""
            other_detail['password'] = ""
            other_detail['videopassword'] = ""
            other_detail['netrc'] = False
            other_detail['no_warnings'] = False
            other_detail['skip_download'] = False
            other_detail['ignoreerrors'] = False
            other_detail['youtube_include_dash_manifest'] = False
            other_detail['noresizebuffer'] = False
            other_detail['extract_flat'] = False
            other_detail['age_limit'] = ""
            other_detail['min_views'] = ""
            other_detail['max_views'] = ""
            other_detail['matchtitle'] = False
            other_detail['rejecttitle'] = False
            other_detail['rm_cachedir'] = False
            other_detail['verbose'] = False
            other_detail['keepvideo'] = False
            other_detail['no_check_certificate'] = False
            other_detail['max_downloads'] = 9999999
            other_detail['time_between_downloads'] = 1.75
            with open(setting.name_of_json, 'w') as f:
                json.dump(data, f, indent=3)
                f.close()

        self.apply_btn.configure(state=DISABLED)
        sys.stderr = sys.__stderr__
        sys.stdout = sys.__stdout__
        print(max_downloads, "MAX DOWNLOADS", sep="   ")
        print(wait_time, "WAIT TIME", sep="   ")
        print(video_ops, "OTHER OPTIONS", sep="   ", end="\n\n")

###############################################################################################################

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

floatnum = "3.0"
part_type = "-- VIDEO --"
toggle = 0

class CoreGUI:
    """
    Creating the text box for output and redirecting the stdout and stderr to the text box.
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

    def delete_lines(self):
        try:
            self.text_box.config(state=NORMAL)
            self.text_box.delete(floatnum, "end")
            print("\n\n"+part_type)
            self.text_box.see("end")
            self.text_box.config(state=DISABLED)
        except:
            pass

    def normal_delete(self):
        try:
            self.text_box.config(state=NORMAL)
            self.text_box.delete("3.0", "end")
            self.text_box.see("end")
            self.text_box.config(state=DISABLED)
        except:
            pass


class DownloadConversion:
    """
    Needs threading otherwise errors will occur, and multiple freezes.

    This class deals with selenium, conversion, text box and the downloading.
    """

    def __init__(self):
        self._index = 0
        self.win_count = 1
        self.terminate_count = 1
        self._driver = None
        self._downloadError = yt.utils.DownloadError
        self._FFmpegPostProcessorError = postprocessor.ffmpeg.FFmpegPostProcessorError

    def reset_count(self, win):
        global floatnum, part_type
        floatnum = "3.0"
        part_type = "-- VIDEO --"
        video_ops.update(logger=None, progress_hooks=None)
        video_ops.pop('logger')
        video_ops.pop('progress_hooks')
        win.destroy()
        edit_format.configure(state=ACTIVE)
        detect_btn.configure(state=ACTIVE)
        self.win_count = 1
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def reset_countV2(self, win):
        global floatnum, part_type
        floatnum = "3.0"
        part_type = "-- VIDEO --"
        video_ops.update(logger=None, progress_hooks=None)
        video_ops.pop('logger')
        video_ops.pop('progress_hooks')
        win.destroy()
        edit_format.configure(state=ACTIVE)
        detect_btn.configure(state=ACTIVE)
        self.win_count = 1

    def reset_countV3(self, win):
        win.destroy()
        self.win_count = 1

    def new_win(self):
        if self.win_count == 1:
            self.output_win = Toplevel()
            self.output_win.title("Youtube-DL GUI   |   Gloryness  |  v{}".format(__version__))
            self.output_win.iconbitmap('images/#app.ico')
            self.output_win.resizable(False, False)
            self.output_win.configure(bg='#badbfc', bd=5)
            self.output_win.geometry("600x400")
            self.output_win.protocol("WM_DELETE_WINDOW", lambda: self.reset_count(self.output_win))

            self.win_count = 2
            global t
            t = CoreGUI(self.output_win)
            t.text_box.delete("0.0", "end")
        else:
            pass

    def quit_win(self):
        self.output_win.after(2400, lambda: self.reset_count(self.output_win))

    def short_quit_win(self):
        self.output_win.after(1700, lambda: self.reset_count(self.output_win))

    @staticmethod
    def undo():
        sys.stdout = StdDirector(t.undo())
        sys.stderr = StdDirector(t.undo())

    def kill_button(self):
        edit_format.configure(state=DISABLED)
        detect_btn.configure(state=DISABLED)
        kill_button = ttk.Button(self.output_win, text="   Kill Operation (RISKY)   ", state=ACTIVE, style='some.TButton', command=self.terminate_download)
        kill_button.place(x=425, y=356)

    def terminate_download(self):
        self.output_win.after(250, lambda: self.reset_countV2(self.output_win))

    def window(self):
        self.on_new_win()
        timeout = threading.Event()
        timeout.wait(0.90)
        self.output_win.after(200, self.on_download)

    @staticmethod
    def _delete_lines():
        t.normal_delete()

    @staticmethod
    def my_hook(d):
        global floatnum
        global part_type
        global toggle
        if d['status'] == 'finished':
            thread = threading.Event()
            thread.wait(0.1)
            print('\nDone downloading, now converting ...')
            if len(_url) == 1: # this is to support the downloading of playlists.
                if toggle == 0:
                    floatnum = "10.0"
                    part_type = "-- AUDIO --"
                    toggle = 1
                elif toggle == 1:
                    floatnum = "3.0"
                    part_type = "-- VIDEO --"
                    toggle = 0
            else:
                floatnum = "10.0"
                part_type = "-- AUDIO --"
            thread = threading.Event()
            thread.wait(1.5)
        if d['status'] == 'downloading':
            t.delete_lines()
            print('\nFILE: %s' % d['filename'], 'SPEED: %s' % d['_speed_str'], 'PERCENT: %s' % d['_percent_str'], 'ETA: %s' % d['_eta_str'], sep='\n')
            '''
            _speed_str
            _percent_str -- these are all the more accurate-like strings rather than just "eta". They give more information, and are also located in source code.
            _eta_str
            '''

    def download(self):
        """
        Mainly handles the errors, aswell as the downloading.
        An error is a rare occurance now thanks to the update in v0.7.6 BETA.
        """
        global max_downloads
        global floatnum, part_type, _url
        floatnum = "3.0"
        part_type = "-- VIDEO --"
        _url = url_box.get("1.0", END).split(sep="\n") # split() will seperate all strings containing a space or new line
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        [_url.remove(x) for x in _url if not x.startswith(('https://', 'http://'))]
        try:
            [_url.remove('') for i in range(len(_url))]
        except ValueError:
            pass
        print(_url)
        _url_iterator = iter(_url) # this will make an iterator object generator which will let us go through the list 1 by 1 each time I call next(_url_iterator)
        self.undo()
        video_ops.update(logger=MyLogger(),
                         progress_hooks=[self.my_hook])

        with yt.YoutubeDL(video_ops) as ydl:
            try:
                if quality_btn_var.get() != "NONE" \
                    and audio_btn_var.get() != "NONE":
                        part_type = '-- VIDEO --'

                if quality_btn_var.get() == "NONE" \
                    and audio_btn_var.get() != "NONE":
                        part_type = '-- AUDIO --'

                if quality_btn_var.get() != "NONE" \
                    and audio_btn_var.get() == "NONE":
                        part_type = '-- VIDEO --'

                if len(_url) < 1:
                    print("You must enter a URL")
                    self.short_quit_win()

                elif not _url[0].startswith(('https://', 'http://')):
                    print("You must enter a VALID URL")
                    self.short_quit_win()

                elif max_downloads == 0 or max_downloads == 00 or max_downloads == 000 or max_downloads == 0000 or max_downloads == 00000:
                    print("\n\n[info] Maximum number of downloaded files reached!")
                    print("[info] Maximum number of downloaded files reached!")
                    print("[info] Maximum number of downloaded files reached!\n\n")
                    self.quit_win()


                elif len(_url) == 1:
                    self.kill_button()
                    _url_holder = next(_url_iterator)
                    ydl.download([_url_holder])
                    if ext_btn_var.get() == "MP4" \
                            or ext_btn_var.get() == "WEBM"\
                            or ext_btn_var.get() == "FLV" \
                            or ext_btn_var.get() == "AVI":
                        t = threading.Event()
                        t.wait(1.5)
                        extract = ydl.extract_info(_url_holder, download=False)
                        title = extract['title']
                        for index, name in enumerate(title):
                            if name == '<':
                                title = title.replace(name, '_')
                            elif name == '>':
                                title = title.replace(name, '_')
                            elif name == ':':
                                title = title.replace(name, ' -')
                            elif name == '"':
                                title = title.replace(name, '_')
                            elif name == '/':
                                title = title.replace(name, '_')
                            elif name == '\\':
                                title = title.replace(name, '_')
                            elif name == '|':
                                title = title.replace(name, '_')
                            elif name == '?':
                                title = title.replace(name, '_')
                            elif name == '*':
                                title = title.replace(name, '_')

                        print(f'\nConverting MKV to {ext_btn_var.get()}... This may take a while!', f'Converting MKV to {ext_btn_var.get()}... This may take a while!\n',
                              sep='\n')
                        subprocess.call('ffmpeg' + ' -i "' + destination_var.get() + '/' + title + '".mkv' + ' -preset fast "'
                                        + destination_var.get() + '/' + title + '!"' + '.' + ext_btn_var.get().lower(), shell=True)
                        os.remove(destination_var.get() + '/' + title + '.mkv')
                        os.rename(
                            destination_var.get() + '/' + title + '!' + '.' + ext_btn_var.get().lower(),
                            destination_var.get() + '/' + title + '.' + ext_btn_var.get().lower()
                        )
                    if ext_btn_var.get() == "OGG":
                        t = threading.Event()
                        t.wait(1.5)
                        extract = ydl.extract_info(_url_holder, download=False)
                        title = extract['title']
                        for index, name in enumerate(title):
                            if name == '<':
                                title = title.replace(name, '_')
                            elif name == '>':
                                title = title.replace(name, '_')
                            elif name == ':':
                                title = title.replace(name, ' -')
                            elif name == '"':
                                title = title.replace(name, '_')
                            elif name == '/':
                                title = title.replace(name, '_')
                            elif name == '\\':
                                title = title.replace(name, '_')
                            elif name == '|':
                                title = title.replace(name, '_')
                            elif name == '?':
                                title = title.replace(name, '_')
                            elif name == '*':
                                title = title.replace(name, '_')
                        print(f'\nConverting MP3 to {ext_btn_var.get()}... This may take a while!', f'Converting MP3 to {ext_btn_var.get()}... This may take a while!\n',
                              sep='\n')
                        subprocess.call('ffmpeg' + ' -i "' + destination_var.get() + '/' + title + '".mp3' + ' -preset fast "'
                                        + destination_var.get() + '/' + title + '!"' + '.' + ext_btn_var.get().lower(), shell=True)
                        os.remove(destination_var.get() + '/' + title + '.mp3')
                        os.rename(
                            destination_var.get() + '/' + title + '!' + '.' + ext_btn_var.get().lower(),
                            destination_var.get() + '/' + title + '.' + ext_btn_var.get().lower()
                        )
                    t = threading.Event()
                    t.wait(1.5)

                elif len(_url) > 1:
                    self.kill_button()
                    print(f"There will be a {wait_time} second delay between each download.\nThis is changeable in Other Options.")
                    print(f"Max downloads: {max_downloads}\n")

                    for index, link in enumerate(_url, start=1): # going to loop through this code X amount of times and it will track the index which starts at 1
                        if index == max_downloads:               # which we use for tracking the download count.
                            print("\n\n[info] Maximum number of downloaded files reached!")
                            print("[info] Maximum number of downloaded files reached!")
                            print("[info] Maximum number of downloaded files reached!\n\n")
                            self.quit_win()
                        else:
                            _url_holder = next(_url_iterator)
                            if index >= 1:
                                self._delete_lines()
                                print("\n\nDownload [{}] starting\n".format(index))
                            else:
                                print("Download [{}] starting\n".format(index))
                            thread = threading.Event()
                            thread.wait(wait_time)
                            ydl.download([_url_holder])
                            if ext_btn_var.get() == "MP4"\
                                or ext_btn_var.get() == "WEBM"\
                                or ext_btn_var.get() == "FLV" \
                                or ext_btn_var.get() == "AVI":
                                    thread = threading.Event()
                                    thread.wait(1.5)
                                    extract = ydl.extract_info(_url_holder, download=False)
                                    title = extract['title']
                                    for indexx, name in enumerate(title):
                                        if name == '<':
                                            title = title.replace(name, '_')
                                        elif name == '>':
                                            title = title.replace(name, '_')
                                        elif name == ':':
                                            title = title.replace(name, ' -')
                                        elif name == '"':
                                            title = title.replace(name, '_')
                                        elif name == '/':
                                            title = title.replace(name, '_')
                                        elif name == '\\':
                                            title = title.replace(name, '_')
                                        elif name == '|':
                                            title = title.replace(name, '_')
                                        elif name == '?':
                                            title = title.replace(name, '_')
                                        elif name == '*':
                                            title = title.replace(name, '_')
                                    print(f'\nConverting MKV to {ext_btn_var.get()}... This may take a while!', f'Converting MKV to {ext_btn_var.get()}... This may take a while!\n',
                                          sep='\n')
                                    subprocess.call('ffmpeg' + ' -i "' + destination_var.get() + '/' + title + '".mkv' + ' -preset fast "'
                                                    + destination_var.get() + '/' + title + '!"' + '.' + ext_btn_var.get().lower(), shell=True)
                                    os.remove(destination_var.get() + '/' + title + '.mkv')
                                    os.rename(
                                        destination_var.get() + '/' + title + '!' + '.' + ext_btn_var.get().lower() ,
                                        destination_var.get() + '/' + title + '.' + ext_btn_var.get().lower()
                                    )
                            if ext_btn_var.get() == "OGG":
                                thread = threading.Event()
                                thread.wait(1.5)
                                extract = ydl.extract_info(_url_holder, download=False)
                                title = extract['title']
                                for indexx, name in enumerate(title):
                                    if name == '<':
                                        title = title.replace(name, '_')
                                    elif name == '>':
                                        title = title.replace(name, '_')
                                    elif name == ':':
                                        title = title.replace(name, ' -')
                                    elif name == '"':
                                        title = title.replace(name, '_')
                                    elif name == '/':
                                        title = title.replace(name, '_')
                                    elif name == '\\':
                                        title = title.replace(name, '_')
                                    elif name == '|':
                                        title = title.replace(name, '_')
                                    elif name == '?':
                                        title = title.replace(name, '_')
                                    elif name == '*':
                                        title = title.replace(name, '_')
                                print(f'\nConverting MP3 to {ext_btn_var.get()}... This may take a while!', f'Converting MP3 to {ext_btn_var.get()}... This may take a while!\n',
                                      sep='\n')
                                subprocess.call('ffmpeg' + ' -i "' + destination_var.get() + '/' + title + '".mp3' + ' -preset fast "'
                                                + destination_var.get() + '/' + title + '!"' + '.' + ext_btn_var.get().lower(), shell=True)
                                os.remove(destination_var.get() + '/' + title + '.mp3')
                                os.rename(
                                    destination_var.get() + '/' + title + '!' + '.' + ext_btn_var.get().lower(),
                                    destination_var.get() + '/' + title + '.' + ext_btn_var.get().lower()
                                )
                            print("\nDownload [{}] completed\n".format(index))
                            thread = threading.Event()
                            thread.wait(0.5)
                            if quality_btn_var.get() != "NONE" \
                                and audio_btn_var.get() != "NONE":
                                    part_type = '-- VIDEO --'
                                    floatnum = "3.0"

                            elif quality_btn_var.get() == "NONE" \
                                and audio_btn_var.get() != "NONE":
                                    part_type = '-- AUDIO --'
                                    floatnum = "3.0"

                            elif quality_btn_var.get() != "NONE" \
                                and audio_btn_var.get() == "NONE":
                                    part_type = '-- VIDEO --'
                                    floatnum = "3.0"

                    self.quit_win()

            except Exception as exc:
                sys.stdout = sys.__stdout__
                sys.stderr = sys.__stderr__
                logger.exception(msg='\n{} was unable to convert to {} due to no available formats otherwise an unknown error.\n'
                           .format(_url_holder, video_ops.get('merge_output_format')))
                t = threading.Event()
                t.wait(1)
                self.undo()
                print("error: %s" % exc)
                t.wait(1.75)

                try:
                    if len(_url) == 1:
                        self.kill_button()
                        _url_holder = next(_url_iterator)
                        ydl.download([_url_holder])
                        if ext_btn_var.get() == "MP4" \
                                or ext_btn_var.get() == "WEBM"\
                                or ext_btn_var.get() == "FLV" \
                                or ext_btn_var.get() == "AVI":
                            t = threading.Event()
                            t.wait(1.5)
                            extract = ydl.extract_info(_url_holder, download=False)
                            title = extract['title']
                            for index, name in enumerate(title):
                                if name == '<':
                                    title = title.replace(name, '_')
                                elif name == '>':
                                    title = title.replace(name, '_')
                                elif name == ':':
                                    title = title.replace(name, ' -')
                                elif name == '"':
                                    title = title.replace(name, '_')
                                elif name == '/':
                                    title = title.replace(name, '_')
                                elif name == '\\':
                                    title = title.replace(name, '_')
                                elif name == '|':
                                    title = title.replace(name, '_')
                                elif name == '?':
                                    title = title.replace(name, '_')
                                elif name == '*':
                                    title = title.replace(name, '_')

                            print(f'\nConverting MKV to {ext_btn_var.get()}... This may take a while!', f'Converting MKV to {ext_btn_var.get()}... This may take a while!\n',
                                  sep='\n')
                            subprocess.call('ffmpeg' + ' -i "' + destination_var.get() + '/' + title + '".mkv' + ' -preset fast "'
                                            + destination_var.get() + '/' + title + '!"' + '.' + ext_btn_var.get().lower(), shell=True)
                            os.remove(destination_var.get() + '/' + title + '.mkv')
                            os.rename(
                                destination_var.get() + '/' + title + '!' + '.' + ext_btn_var.get().lower(),
                                destination_var.get() + '/' + title + '.' + ext_btn_var.get().lower()
                            )
                        if ext_btn_var.get() == "OGG":
                            t = threading.Event()
                            t.wait(1.5)
                            extract = ydl.extract_info(_url_holder, download=False)
                            title = extract['title']
                            for index, name in enumerate(title):
                                if name == '<':
                                    title = title.replace(name, '_')
                                elif name == '>':
                                    title = title.replace(name, '_')
                                elif name == ':':
                                    title = title.replace(name, ' -')
                                elif name == '"':
                                    title = title.replace(name, '_')
                                elif name == '/':
                                    title = title.replace(name, '_')
                                elif name == '\\':
                                    title = title.replace(name, '_')
                                elif name == '|':
                                    title = title.replace(name, '_')
                                elif name == '?':
                                    title = title.replace(name, '_')
                                elif name == '*':
                                    title = title.replace(name, '_')
                            print(f'\nConverting MP3 to {ext_btn_var.get()}... This may take a while!', f'Converting MP3 to {ext_btn_var.get()}... This may take a while!\n',
                                  sep='\n')
                            subprocess.call('ffmpeg' + ' -i "' + destination_var.get() + '/' + title + '".mp3' + ' -preset fast "'
                                            + destination_var.get() + '/' + title + '!"' + '.' + ext_btn_var.get().lower(), shell=True)
                            os.remove(destination_var.get() + '/' + title + '.mp3')
                            os.rename(
                                destination_var.get() + '/' + title + '!' + '.' + ext_btn_var.get().lower(),
                                destination_var.get() + '/' + title + '.' + ext_btn_var.get().lower()
                            )
                        t = threading.Event()
                        t.wait(1.5)

                    elif len(_url) > 1:
                        self.kill_button()
                        print(f"There will be a {wait_time} second delay between each download.\nThis is changeable in Other Options.")
                        print(f"Max downloads: {max_downloads}\n")

                        for index, link in enumerate(_url, start=1): # going to loop through this code X amount of times and it will track the index which starts at 1
                            if index == max_downloads:               # which we use for tracking the download count.
                                print("\n\n[info] Maximum number of downloaded files reached!")
                                print("[info] Maximum number of downloaded files reached!")
                                print("[info] Maximum number of downloaded files reached!\n\n")
                                self.quit_win()
                            else:
                                _url_holder = next(_url_iterator)
                                if index >= 1:
                                    self._delete_lines()
                                    print("\n\nDownload [{}] starting\n".format(index))
                                else:
                                    print("Download [{}] starting\n".format(index))
                                thread = threading.Event()
                                thread.wait(wait_time)
                                ydl.download([_url_holder])
                                if ext_btn_var.get() == "MP4"\
                                    or ext_btn_var.get() == "WEBM"\
                                    or ext_btn_var.get() == "FLV" \
                                    or ext_btn_var.get() == "AVI":
                                        thread = threading.Event()
                                        thread.wait(1.5)
                                        extract = ydl.extract_info(_url_holder, download=False)
                                        title = extract['title']
                                        for indexx, name in enumerate(title):
                                            if name == '<':
                                                title = title.replace(name, '_')
                                            elif name == '>':
                                                title = title.replace(name, '_')
                                            elif name == ':':
                                                title = title.replace(name, ' -')
                                            elif name == '"':
                                                title = title.replace(name, '_')
                                            elif name == '/':
                                                title = title.replace(name, '_')
                                            elif name == '\\':
                                                title = title.replace(name, '_')
                                            elif name == '|':
                                                title = title.replace(name, '_')
                                            elif name == '?':
                                                title = title.replace(name, '_')
                                            elif name == '*':
                                                title = title.replace(name, '_')
                                        print(f'\nConverting MKV to {ext_btn_var.get()}... This may take a while!', f'Converting MKV to {ext_btn_var.get()}... This may take a while!\n',
                                              sep='\n')
                                        subprocess.call('ffmpeg' + ' -i "' + destination_var.get() + '/' + title + '".mkv' + ' -preset fast "'
                                                        + destination_var.get() + '/' + title + '!"' + '.' + ext_btn_var.get().lower(), shell=True)
                                        os.remove(destination_var.get() + '/' + title + '.mkv')
                                        os.rename(
                                            destination_var.get() + '/' + title + '!' + '.' + ext_btn_var.get().lower() ,
                                            destination_var.get() + '/' + title + '.' + ext_btn_var.get().lower()
                                        )
                                if ext_btn_var.get() == "OGG":
                                    thread = threading.Event()
                                    thread.wait(1.5)
                                    extract = ydl.extract_info(_url_holder, download=False)
                                    title = extract['title']
                                    for indexx, name in enumerate(title):
                                        if name == '<':
                                            title = title.replace(name, '_')
                                        elif name == '>':
                                            title = title.replace(name, '_')
                                        elif name == ':':
                                            title = title.replace(name, ' -')
                                        elif name == '"':
                                            title = title.replace(name, '_')
                                        elif name == '/':
                                            title = title.replace(name, '_')
                                        elif name == '\\':
                                            title = title.replace(name, '_')
                                        elif name == '|':
                                            title = title.replace(name, '_')
                                        elif name == '?':
                                            title = title.replace(name, '_')
                                        elif name == '*':
                                            title = title.replace(name, '_')
                                    print(f'\nConverting MP3 to {ext_btn_var.get()}... This may take a while!', f'Converting MP3 to {ext_btn_var.get()}... This may take a while!\n',
                                          sep='\n')
                                    subprocess.call('ffmpeg' + ' -i "' + destination_var.get() + '/' + title + '".mp3' + ' -preset fast "'
                                                    + destination_var.get() + '/' + title + '!"' + '.' + ext_btn_var.get().lower(), shell=True)
                                    os.remove(destination_var.get() + '/' + title + '.mp3')
                                    os.rename(
                                        destination_var.get() + '/' + title + '!' + '.' + ext_btn_var.get().lower(),
                                        destination_var.get() + '/' + title + '.' + ext_btn_var.get().lower()
                                    )
                                print("\nDownload [{}] completed\n".format(index))
                                thread = threading.Event()
                                thread.wait(0.5)
                                if quality_btn_var.get() != "NONE" \
                                    and audio_btn_var.get() != "NONE":
                                        part_type = '-- VIDEO --'
                                        floatnum = "3.0"

                                elif quality_btn_var.get() == "NONE" \
                                    and audio_btn_var.get() != "NONE":
                                        part_type = '-- AUDIO --'
                                        floatnum = "3.0"

                                elif quality_btn_var.get() != "NONE" \
                                    and audio_btn_var.get() == "NONE":
                                        part_type = '-- VIDEO --'
                                        floatnum = "3.0"

                        self.quit_win()
                except Exception as exc:
                    sys.stdout = sys.__stdout__
                    sys.stderr = sys.__stderr__
                    logger.exception(msg='\nAn error occured and error has been logged.\n{} failed due to an error: {}\n\n'.format(_url_holder, exc))
                    self.quit_win()

                finally:
                    print("\nDownload COMPLETE!\n")
                    self.quit_win()

            finally:
                if len(_url) < 1:
                    pass
                elif not _url[0].startswith(('https://', 'http://', 'file://')):
                    pass
                else:
                    print("\nDownload COMPLETE!\n")
                    self.quit_win()

    def open_selenium(self):
        """
        A fun feature to use when your browsing youtube or other sites.
        """
        if self.win_count == 1:
            with open(setting.name_of_json) as f:
                data = json.load(f)

            for key, value in data.items():
                if key == 'settings':
                    for sel_name, sel_detail in value[1].items():
                        pass
            self.selenium_win = Toplevel()
            self.selenium_win.title("Youtube-DL GUI   |  v{}".format(__version__))
            self.selenium_win.iconbitmap('images/#app.ico')
            self.selenium_win.resizable(False, False)
            self.selenium_win.configure(bg='#cbdbfc', bd=5)
            self.selenium_win.geometry("450x300")
            self.selenium_win.protocol("WM_DELETE_WINDOW", lambda: self.reset_countV3(self.selenium_win))
            self.win_count = 2

            def add_label(win, text, bg=None, fg="black", x=None, y=None):
                label_adder = Label(win, text=text, fg=fg, bg=bg)
                label_adder.place(x=x, y=y)

            def add_border(win, height, width, bg=None, bd=None, text=None, font=None, labelanchor=None, relief=None, x=None, y=None):
                border_adder = LabelFrame(win, height=height, width=width, bg=bg, bd=bd, text=text if text is not None else "",
                                          font=font if font is not None else "TkDefaultFont", labelanchor=labelanchor, relief=relief)
                border_adder.place(x=x, y=y)

            # It just looks better like this, thought i'd have a play around with this way! Turned out fine.

            add_border(self.selenium_win, 260, 440, '#cbdbfc', 2, None, None, N, SOLID, -2, 0)
            add_label(self.selenium_win, "Before you do anything, please note that you must set:", '#cbdbfc', x=1, y=3)
            add_label(self.selenium_win, "- Your Preferred Browser - In 'File' tab then 'Settings'", '#cbdbfc', x=1, y=33)
            add_label(self.selenium_win, "- WebDriver Location (e.g geckodriver.exe for Firefox) - In 'File' tab then 'Settings'", '#cbdbfc', x=1, y=63)
            add_label(self.selenium_win, "- If you don't have a WebDriver, click the 'Tools' tab and click 'Install WebDriver'!", '#cbdbfc', x=1, y=93)
            add_label(self.selenium_win, "Execute = Grab all URLs from selenium that are downloadable.", '#cbdbfc', fg="#80200f", x=1, y=180)
            add_label(self.selenium_win, "Open = Open Selenium.", '#cbdbfc', fg="#80200f", x=1, y=200)
            add_label(self.selenium_win, "Close - Close down this window.", '#cbdbfc', fg="#80200f", x=1, y=220)
            def open_selenium_thread():
                def open_selenium_function():
                    try:
                        open_sel.configure(state=DISABLED)
                        if sel_detail['browser'] == 'Firefox':
                            if sel_detail['profile'] != "":
                                if sel_detail['path'] != "":
                                    self._profile = webdriver.FirefoxProfile(sel_detail['profile'])
                                    self._driver = webdriver.Firefox(executable_path=PATH, firefox_profile=self._profile)
                                else:
                                    self._profile = webdriver.FirefoxProfile(sel_detail['profile'])
                                    self._driver = webdriver.Firefox(firefox_profile=self._profile)
                            else:
                                if sel_detail['path'] != "":
                                    self._driver = webdriver.Firefox(executable_path=PATH)
                                else:
                                    self._driver = webdriver.Firefox()
                        if sel_detail['browser'] == 'Chrome':
                            if sel_detail['path'] != "":
                                self._driver = webdriver.Chrome(executable_path=PATH)
                            else:
                                self._driver = webdriver.Chrome()
                        if sel_detail['browser'] == 'Safari':
                            if sel_detail['path'] != "":
                                self._driver = webdriver.Safari(executable_path=PATH)
                            else:
                                self._driver = webdriver.Safari()
                        if sel_detail['browser'] == 'Opera':
                            if sel_detail['path'] != "":
                                self._driver = webdriver.Opera(executable_path=PATH)
                            else:
                                self._driver = webdriver.Opera()
                        if sel_detail['browser'] == 'Edge':
                            if sel_detail['path'] != "":
                                self._driver = webdriver.Edge(executable_path=PATH)
                            else:
                                self._driver = webdriver.Edge()
                        if sel_detail['browser'] == 'Internet Explorer':
                            if sel_detail['path'] != "":
                                self._driver = webdriver.Ie(executable_path=PATH)
                            else:
                                self._driver = webdriver.Ie()
                        self._driver.get(sel_detail['link'])
                        self._driver.maximize_window()
                    except Exception as exc:
                        logger.exception("ERROR: An error occured while opening selenium: %s" % exc)
                sel_thread = threading.Timer(0.2, open_selenium_function)
                sel_thread.start()

            def execute_urls_function():
                open_sel.configure(state=NORMAL)
                download_call.on_get_urls()

            style1.configure('selenium.TButton', width=10)

            execute = ttk.Button(self.selenium_win, text="Execute", style="selenium.TButton", command=execute_urls_function)
            execute.place(x=200, y=265)

            open_sel = ttk.Button(self.selenium_win, text="Open", style="selenium.TButton", state=NORMAL, command=open_selenium_thread)
            open_sel.place(x=280, y=265)

            cancel = ttk.Button(self.selenium_win, text="Cancel", style="selenium.TButton", command=lambda: self.reset_countV3(self.selenium_win))
            cancel.place(x=360, y=265)

    def get_urls(self):
        try:
            self._index = 0
            self._driver.switch_to.window(self._driver.window_handles[self._index])
            for i in range(len(self._driver.window_handles)):
                if str(self._driver.current_url).startswith(tuple(all_extractors.pack_extractors)):
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

    # Threading

    def on_new_win(self):
        new_win_thread = threading.Thread(target=self.new_win)
        new_win_thread.start()

    def on_window(self):
        video_ops.update(no_color=True)
        window_thread = threading.Thread(target=self.window)
        window_thread.start()

    def on_download(self):
        download_thread = threading.Thread(target=self.download)
        download_thread.start()

    def on_selenium(self):
        selenium_thread = threading.Thread(target=self.open_selenium)
        selenium_thread.start()

    def on_get_urls(self):
        get_urls_thread = threading.Thread(target=self.get_urls)
        get_urls_thread.start()


class MyLogger:

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
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        logger.exception(msg="ERROR : {}".format(msg))
        download_call.undo()


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

# Settings-related
init_settings()
auto_fill()
auto_fill_and_click_thread()
check()
set_path()

mainloop()
