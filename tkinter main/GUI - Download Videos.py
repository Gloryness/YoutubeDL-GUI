from __future__ import unicode_literals

from tkinter import *
from tkinter import messagebox, filedialog, scrolledtext

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import youtube_dl as yt

import colorama # optional but is recommended
import math
import time
import subprocess
import os

PATH = 'C:/Users/Gloryness/geckodriver.exe' # changeable

root = Tk()
root.title("Download Videos via Python by Gloryness")
root.iconbitmap('C:/Users/Gloryness/AppData/Local/atom/app.ico')
root.resizable(False, False)
root.configure(bg='#cbdbfc', bd=5)
root.geometry("550x450")

label1 = Label(root, text="Destination -", bg="#cbdbfc")
label1.grid(row=0, column=0)

destination_var = StringVar()

destination = Entry(root, width=77, state=DISABLED, relief=SOLID, textvariable=destination_var)
destination.grid(row=0, column=1, padx=0, pady=0)

def browse():
    """
    For setting the destination for the download.
    """
    global video_ops
    destination.configure(state=NORMAL)
    get_directory = filedialog.askdirectory(initialdir="R:/Downloaded Videos", title="Destination")
    destination.delete(0, END)
    destination.insert(0, get_directory)

    video_ops.update(outtmpl='{}/%(title)s'.format(destination_var.get()))
    destination.configure(state=DISABLED)
    print(video_ops, end="\n\n")

###########################################################################

browse_btn = Button(root, text="Browse", bd=2, relief=SOLID, underline=1, command=browse)
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
    "720p",
    "480p",
    "360p",
    "NONE"
]

quality_btn_var = StringVar()
quality_btn_var.set(quality_btn_options[0])

quality_label = Label(root, text="Quality", bg="#cbdbfc", font="Cooper 15")
quality_label.place(x=65, y=71)

quality_btn = OptionMenu(root, quality_btn_var, *quality_btn_options)
quality_btn.place(x=50, y=98, width=90)

###########################################################################

audio_btn_options = [
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

audio_btn = OptionMenu(root, audio_btn_var, *audio_btn_options)
audio_btn.place(x=220, y=98, width=90)

###########################################################################

ext_btn_options = [
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

ext_btn = OptionMenu(root, ext_btn_var, *ext_btn_options)
ext_btn.place(x=400, y=98, width=90)

###########################################################################

class Updates(object):
    _format = None

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
                video_ops.update(ext='{}'.format(ext_btn_var.get().lower()), merge_output_format='{}'.format(ext_btn_var.get().lower()))

        elif quality_btn_var.get() == "NONE" \
            and audio_btn_var.get() != "NONE":
                video_ops.update(ext='{}'.format(ext_btn_var.get().lower()), merge_output_format='{}'.format(ext_btn_var.get().lower()))

        elif audio_btn_var.get() == "NONE" \
            and quality_btn_var.get() != "NONE":
                video_ops.update(ext='{}'.format(ext_btn_var.get().lower()), merge_output_format='{}'.format(ext_btn_var.get().lower()))

        print(video_ops, "EXT", sep="   ", end="\n\n")

    @staticmethod
    def clear_url_box():
        url_box.delete("0.0", END)

    @staticmethod
    def update_format_btns():
        done_btn.configure(state=DISABLED, bd=1)
        quality_btn.configure(state=DISABLED)
        audio_btn.configure(state=DISABLED)
        ext_btn.configure(state=DISABLED)

    @staticmethod
    def edit_format_btns():
        confirm = messagebox.askquestion("Are You Sure?", "Would you like to edit your video formats?")
        if confirm == "yes":
            done_btn.configure(state=ACTIVE, bd=2)
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
        detect_btn.configure(state=ACTIVE, bd=2)
        download_btn.configure(state=ACTIVE, bd=2)
        edit_format.configure(state=ACTIVE, bd=2)
        url_box.configure(state=NORMAL, bd=4)
        clear_btn.configure(state=ACTIVE, bd=1)

    @staticmethod
    def disable_options():
        file_options_btn.configure(state=DISABLED)
        download_options_btn.configure(state=DISABLED)
        other_options_btn.configure(state=DISABLED)
        url_box.configure(state=DISABLED, bd=2)
        clear_btn.configure(state=DISABLED, bd=1)
        detect_btn.configure(state=DISABLED, bd=1)
        edit_format.configure(state=DISABLED, bd=1)
        download_btn.configure(state=DISABLED, bd=1)


do = Updates()

###########################################################################

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
                    do.update_video_dict()
                    do.update_audio_dict()
                    do.update_both_dict()
                    do.update_ext_dict()
                    do.update_format_btns()
                    do.after_done_btn()

        elif quality_btn_var.get() != "NONE" \
            and audio_btn_var.get() == "NONE":
                if ext_btn_var.get() == "MP3" \
                    or ext_btn_var.get() == "WAV":
                    none_types3 = messagebox.showerror("?????", f"Sorry, but {ext_btn_var.get()} is not a supported file-type for videos.")
                else:
                    do.update_video_dict()
                    do.update_audio_dict()
                    do.update_both_dict()
                    do.update_ext_dict()
                    do.update_format_btns()
                    do.after_done_btn()

        else:
            do.update_video_dict()
            do.update_audio_dict()
            do.update_both_dict()
            do.update_ext_dict()
            do.update_format_btns()
            do.after_done_btn()
    else:
        pass

done_btn = Button(root, text="Done", bd=2, relief=SOLID, padx=25, command=on_done_btn)
done_btn.place(x=220, y=154)

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

class OptionWindows(object):
    """
    * Filesystem Options
    * Download Options
    * Other Options
    """
    _stabalize = [file_count, download_count, other_count]
    _title = 'Download Videos via Python by Gloryness'
    _icon = 'C:/Users/Gloryness/AppData/Local/atom/app.ico'
    _size = '600x450'

    @classmethod
    def reset_variables(cls, win):
        win.destroy()
        cls._stabalize[0] = 1
        cls._stabalize[1] = 1
        cls._stabalize[2] = 1

    @classmethod
    def file_options_window(cls):
        if cls._stabalize[0] == 1:
            global file_win, file_label
            file_win = Toplevel()
            file_win.title(cls._title)
            file_win.iconbitmap(cls._icon)
            file_win.resizable(False, False)
            file_win.configure(bg='#cbdbfc', bd=5)
            file_win.geometry(cls._size)
            file_win.protocol("WM_DELETE_WINDOW", lambda: option.reset_variables(file_win))

            file_label = Label(file_win, text="Filesystem Options", bg='#cbdbfc', font="Cooper 18")
            file_label.place(x=180, y=3)

            index = 0
            for i in range(3):
                cls._stabalize[index] += 1
                index += 1
            index = 0
            print(cls._stabalize)
        else:
            pass

    @classmethod
    def download_options_window(cls):
        if cls._stabalize[2] == 1:
            global download_win, download_label
            download_win = Toplevel()
            download_win.title(cls._title)
            download_win.iconbitmap(cls._icon)
            download_win.resizable(False, False)
            download_win.configure(bg='#cbdbfc', bd=5)
            download_win.geometry(cls._size)
            download_win.protocol("WM_DELETE_WINDOW", lambda: option.reset_variables(download_win))

            download_label = Label(download_win, text="Downlaod Options", bg='#cbdbfc', font="Cooper 18")
            download_label.place(x=186, y=3)

            index = 0
            for i in range(3):
                cls._stabalize[index] += 1
                index += 1
            index = 0
            print(cls._stabalize)
        else:
            pass

    @classmethod
    def other_options_window(cls):
        if cls._stabalize[1] == 1:
            global other_win, other_label
            other_win = Toplevel()
            other_win.title(cls._title)
            other_win.iconbitmap(cls._icon)
            other_win.resizable(False, False)
            other_win.configure(bg='#cbdbfc', bd=5)
            other_win.geometry(cls._size)
            other_win.protocol("WM_DELETE_WINDOW", lambda: option.reset_variables(other_win))

            other_label = Label(other_win, text="Other Options", bg='#cbdbfc', font="Cooper 18")
            other_label.place(x=215, y=3)

            index = 0
            for i in range(3):
                cls._stabalize[index] += 1
                index += 1
            index = 0
            print(cls._stabalize)

        else:
            pass

option = OptionWindows()

### OPTION 1

file_option_label = Label(root, text="File Options", bg="#cbdbfc", font="Cooper 14")
file_option_label.place(x=42, y=221)

file_options_btn = Button(root, text="Click Me", state=DISABLED, command=option.file_options_window)
file_options_btn.place(x=50, y=248, width=90)

### OPTION 2

download_option_label = Label(root, text="Download Options", bg="#cbdbfc", font="Cooper 14")
download_option_label.place(x=184, y=221)

download_options_btn = Button(root, text="Click Me", state=DISABLED, command=option.download_options_window)
download_options_btn.place(x=220, y=248, width=90)

### OPTION 3

other_options_label = Label(root, text="Other Options", bg="#cbdbfc", font="Cooper 14")
other_options_label.place(x=380, y=221)

other_options_btn = Button(root, text="Click Me", state=DISABLED, command=option.other_options_window)
other_options_btn.place(x=400, y=248, width=90)

url_box = scrolledtext.ScrolledText(root, height=6, width=56, bd=2, state=DISABLED, font='Cooper 9')
url_box.place(x=5, y=340)

class DownloadConversion(object):

    def __init__(self):
        self._index = 0
        self._driver = None

    _downloadError = yt.utils.DownloadError
    _FFmpegPostProcessorError = yt.postprocessor.ffmpeg.FFmpegPostProcessorError

    @classmethod
    def download(cls):
        """
        Mainly handles the errors, aswell as the downloading.
        """
        _url = url_box.get("1.0", END).split()
        print(_url)
        with yt.YoutubeDL(video_ops) as ydl:
            try:

                if len(_url) < 1:
                    print(colorama.Fore.RED + "You must enter a URL" + colorama.Fore.RESET)
                    url_box.delete("1.0", END)
                    url_box.insert("1.0", "You must enter a URL")

                elif not _url[0].startswith('https://'):
                    print(colorama.Fore.RED + "You must enter a VALID URL" + colorama.Fore.RESET)
                    url_box.delete("1.0", END)
                    url_box.insert("1.0", "You must enter a VALID URL")

                elif ext_btn_var.get() == "WAV":
                    raise cls._downloadError("without this, will cause a bug - unknown why.")

                elif len(_url) == 1:
                    if quality_btn_var.get() != "NONE" \
                        and audio_btn_var.get() == "NONE":
                            ydl.download([_url[0]])
                            extract = ydl.extract_info(_url[0], download=False)
                            time.sleep(1)
                            subprocess.call('ffmpeg' + ' -i "' + destination_var.get() + '/' + extract['title'] + '".' + ext_btn_var.get().lower() + ' -an -y -preset fast "'
                                            + destination_var.get() + '/' + extract['title'] + 'V2"' + '.' + ext_btn_var.get().lower(), shell=False)
                            os.remove(destination_var.get() + '/' + extract['title'] + '.' + extract['ext'])

                    else:
                        ydl.download([_url[0]])
                elif len(_url) > 1:
                    if quality_btn_var.get() != "NONE" \
                        and audio_btn_var.get() == "NONE":
                        index = 0
                        for i in range(len(list(_url))):
                            ydl.download([_url[index]])
                            extract = ydl.extract_info(_url[0], download=False)
                            time.sleep(1)
                            subprocess.call('ffmpeg' + ' -i "' + destination_var.get() + '/' + extract['title'] + '".' + ext_btn_var.get().lower() + ' -an -y -preset fast "'
                                            + destination_var.get() + '/' + extract['title'] + 'V2"' + '.' + ext_btn_var.get().lower(), shell=False)
                            _url.pop(index)
                            os.remove(destination_var.get() + '/' + extract['title'] + '.' + extract['ext'])
                    else:
                        index = 0
                        for i in range(len(list(_url))):
                            ydl.download([_url[index]])
                            _url.pop(index)

            except cls._downloadError or cls._FFmpegPostProcessorError:

                print(colorama.Fore.RED + "Sorry, but we could not download the requested format {}!\nThe video will be merged into a more suitable format instead. Such as MKV."
                      .format(ext_btn_var.get().lower()) + colorama.Fore.RESET)

                if quality_btn_var.get() != "NONE" \
                    and audio_btn_var.get() != "NONE":
                        video_ops.update(merge_output_format='mkv', outtmpl=destination_var.get() + '/%(title)s.%(ext)s', ext='{}'.format(ext_btn_var.get().lower()))
                        with yt.YoutubeDL(video_ops) as ytd:
                            try:
                                if len(_url) == 1:
                                    ytd.download([_url[0]])
                                if len(_url) > 1:
                                    for i in range(len(list(_url))):
                                        ytd.download([_url[index]])
                                        _url.pop(index)

                            except cls._downloadError or cls._FFmpegPostProcessorError:
                                video_ops.pop('merge_output_format')
                                video_ops.update(nooverwrites=False, ext='{}'.format(ext_btn_var.get().lower()))
                                with yt.YoutubeDL(video_ops) as ytk:
                                    try:
                                        if len(_url) == 1:
                                            ytd.download([_url[0]])
                                        if len(_url) > 1:
                                            for i in range(len(list(_url))):
                                                ytd.download([_url[index]])
                                                _url.pop(index)
                                    except Exception as exc:
                                        print(colorama.Fore.RED + "There was an error: %s" % exc + colorama.Fore.RESET)

                                    finally:
                                        print(colorama.Fore.GREEN + "Download COMPLETE!" + colorama.Fore.RESET)
                            finally:
                                print(colorama.Fore.GREEN + "Download COMPLETE!" + colorama.Fore.RESET)

                elif quality_btn_var.get() == "NONE" \
                    and audio_btn_var.get() != "NONE":
                        if ext_btn_var.get() == ext_btn_options[1]:
                            video_ops.update(postprocessors=[{
                                "key": 'FFmpegExtractAudio',
                                "preferredcodec": 'mp3'
                                }], outtmpl=destination_var.get() + '/%(title)s.%(ext)s', ext='{}'.format(ext_btn_var.get().lower()))
                            with yt.YoutubeDL(video_ops) as ytd:
                                try:
                                    if len(_url) == 1:
                                        ytd.download([_url[0]])
                                    if len(_url) > 1:
                                        for i in range(len(list(_url))):
                                            ytd.download([_url[index]])
                                            _url.pop(index)
                                except cls._downloadError or cls._FFmpegPostProcessorError:
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
                                                    ytk.download([_url[index]])
                                                    _url.pop(index)
                                        except Exception as exc:
                                            print(colorama.Fore.RED + "There was an error: %s" % exc + colorama.Fore.RESET)

                                        finally:
                                            print(colorama.Fore.GREEN + "Download COMPLETE!" + colorama.Fore.RESET)
                                finally:
                                    print(colorama.Fore.GREEN + "Download COMPLETE!" + colorama.Fore.RESET)

                        elif ext_btn_var.get() == ext_btn_options[4]:
                            video_ops.update(postprocessors=[{
                                "key": 'FFmpegExtractAudio',
                                "preferredcodec": 'wav'
                            }], outtmpl=destination_var.get() + '/%(title)s.%(ext)s', ext='{}'.format(ext_btn_var.get().lower()))
                            with yt.YoutubeDL(video_ops) as ytd:
                                try:
                                    if len(_url) == 1:
                                        ytd.download([_url[0]])
                                    if len(_url) > 1:
                                        for i in range(len(list(_url))):
                                            ytd.download([_url[index]])
                                            _url.pop(index)
                                except cls._downloadError or cls._FFmpegPostProcessorError:
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
                                                    ytk.download([_url[index]])
                                                    _url.pop(index)
                                        except Exception as exc:
                                            print(colorama.Fore.RED + "There was an error: %s" % exc + colorama.Fore.RESET)

                                        finally:
                                            print(colorama.Fore.GREEN + "Download COMPLETE!" + colorama.Fore.RESET)
                                finally:
                                    print(colorama.Fore.GREEN + "Download COMPLETE!" + colorama.Fore.RESET)

                elif audio_btn_var.get() == "NONE" \
                    and quality_btn_var.get() != "NONE":
                        video_ops.update(merge_output_format='mkv', outtmpl=destination_var.get() + '/%(title)s.%(ext)s', ext='mkv')
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
                                        ytd.download([_url[index]])
                                        extract2 = ytd.extract_info(_url[0], download=False)
                                        time.sleep(1)
                                        subprocess.call('ffmpeg' + ' -i "' + destination_var.get() + '/' + extract2['title'] + '".mkv'
                                                        + ' -an -y -preset fast "'
                                                        + destination_var.get() + '/' + extract2['title'] + 'V2"' + '.mkv', shell=False)
                                        _url.pop(index)
                                        os.remove(destination_var.get() + '/' + extract2['title'] + '.mkv')

                            except cls._downloadError or cls._FFmpegPostProcessorError:
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
                                                ytk.download([_url[index]])
                                                video_ops.update(outtmpl=destination_var.get() + '/%(title)s.%(ext)s')
                                                extract3 = ytk.extract_info(_url[0], download=False)
                                                time.sleep(1)
                                                subprocess.call('ffmpeg' + ' -i "' + destination_var.get() + '/' + extract3['title'] + '.' + extract3['ext']
                                                    + '" -an -y -preset fast "'
                                                    + destination_var.get() + '/' + extract3['title'] + 'V2"' + '.' + extract3['ext'], shell=False)
                                                _url.pop(index)
                                                os.remove(destination_var.get() + '/' + extract3['title'] + '.' + extract3['ext']) # Delete the orignal file w/ sound

                                    except Exception as exc:
                                        print(colorama.Fore.RED + "There was an error: %s" % exc + colorama.Fore.RESET)

                                    finally:
                                        print(colorama.Fore.GREEN + "Download COMPLETE!" + colorama.Fore.RESET)
                            finally:
                                print(colorama.Fore.GREEN + "Download COMPLETE!" + colorama.Fore.RESET)
            finally:
                print(colorama.Fore.GREEN + "Download COMPLETE!" + colorama.Fore.RESET)


    def open_selenium(self):
        confirm = messagebox.askyesnocancel("Execute URLS / Open Selenium", "Would you like to OPEN Selenium / Execute URLS / Cancel"
                                            "\nYES - Open Browser via Selenium"
                                            "\nNO - Execute URLS from Selenium"
                                            "\nCANCEL - Cancel")
        if confirm is True:
            self._driver = webdriver.Firefox(executable_path=PATH) # changeable to your own browser
            self._driver.maximize_window()
        elif confirm is False:
            download_call.get_urls()
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
        except AttributeError:
            url_box.delete("1.0", END)
            url_box.insert("1.0", "Selenium is not open, therefore no URLS detected.")
        except WebDriverException:
            url_box.delete("1.0", END)
            url_box.insert("1.0", "Selenium is not open, therefore no URLS detected.")
        except Exception:
            url_box.delete("1.0", END)
            url_box.insert("1.0", "Selenium is not open, therefore no URLS detected.")

download_call = DownloadConversion()

download_btn = Button(root, text="Download", bd=1, relief=SOLID, padx=20, state=DISABLED, command=download_call.download)
download_btn.place(x=435, y=410)

edit_format = Button(root, text="Edit Formats", bd=1, relief=SOLID, padx=14, state=DISABLED, command=do.edit_format_btns)
edit_format.place(x=435, y=375)

detect_btn = Button(root, text="Detect URLS", bd=1, relief=SOLID, padx=16, state=DISABLED, command=download_call.open_selenium)
detect_btn.place(x=435, y=340)

clear_btn = Button(root, text="Clear", bd=1, relief=SOLID, padx=20, state=DISABLED, command=do.clear_url_box)
clear_btn.place(x=8, y=314)

detect_info_label = Label(root, text="(selenium-use-only)", bg='#cbdbfc', font='Cooper 10')
detect_info_label.place(x=425, y=318)

info = Label(root, text="Please Enter URLS (new line each)", bg='#cbdbfc', font='Cooper 10')
info.place(x=165, y=312)

## Videos
video_ops = {
}

mainloop()
