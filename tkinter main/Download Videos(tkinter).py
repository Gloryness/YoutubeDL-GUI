from __future__ import unicode_literals
from tkinter import *
from tkinter import messagebox, filedialog
import youtube_dl as yt
import colorama

# REMINDER ---- __func__

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
        global video_ops
        if quality_btn_var.get() == "NONE":
            pass

        else:
            index = len(quality_btn_var.get()) - 1
            video_ops.update(format='bestvideo[height<={}]'.format(quality_btn_var.get()[0:index]))
            cls._format = video_ops.get('format')
            print(cls._format, end="\n\n")
        print(video_ops, "VIDEO", sep="   ", end="\n\n")

    @classmethod
    def update_audio_dict(cls):
        global video_ops
        if audio_btn_var.get() == "NONE":
            video_ops.update(extractaudio=False)

        elif quality_btn_var.get() == "NONE":
            index = len(audio_btn_var.get()) - 1
            video_ops.update(zip(['format', 'extractaudio', 'audioformat'],
                                 ['bestaudio/best[height<={}]'.format(audio_btn_var.get()[0:index]), True, ext_btn_var.get().lower()]))
            cls._format = video_ops.get('format')
            print(cls._format, end="\n\n")
        print(video_ops, "AUDIO", sep="   ",  end="\n\n")

    @classmethod
    def update_both_dict(cls):
        global video_ops
        if quality_btn_var.get() != "NONE" \
            and audio_btn_var.get() != "NONE":
                index = len(audio_btn_var.get()) - 1
                video_ops.update(format=cls._format+'+bestaudio/best[height<={}]'.format(audio_btn_var.get()[0:index]))
                cls._format = video_ops.get('format')
                print(cls._format, end="\n\n")

        elif audio_btn_var.get() == "NONE" \
            and quality_btn_var.get() != "NONE":
                video_ops.update(format=cls._format+'+bestaudio/best[height<=360]')

        elif audio_btn_var.get() != "NONE" \
            and quality_btn_var.get() == "NONE":
                video_ops.update(postprocessors=[{
                    "key": 'FFmpegExtractAudio',
                    "preferredcodec": '{}'.format(ext_btn_var.get().lower())
                }])

        print(video_ops, "BOTH", sep="   ",  end="\n\n")

    @classmethod
    def update_ext_dict(cls):
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
    def update_format_btns():
        done_btn.configure(state=DISABLED, bd=1)
        quality_btn.configure(state=DISABLED)
        audio_btn.configure(state=DISABLED)
        ext_btn.configure(state=DISABLED)

    @staticmethod
    def after_done_btn():
        file_options_btn.configure(state=ACTIVE)
        download_options_btn.configure(state=ACTIVE)
        other_options_btn.configure(state=ACTIVE)
        second_done_btn.configure(state=ACTIVE, bd=2)

    @staticmethod
    def disable_options():
        file_options_btn.configure(state=DISABLED)
        download_options_btn.configure(state=DISABLED)
        other_options_btn.configure(state=DISABLED)
        second_done_btn.configure(state=DISABLED, bd=1)


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

def file_fix(win):
    win.destroy()
    global file_count
    file_count = 1

def download_fix(win):
    win.destroy()
    global download_count
    download_count = 1

def other_fix(win):
    win.destroy()
    global other_count
    other_count = 1

class OptionWindows(object):

    @staticmethod
    def file_options_window():
        global file_count
        if file_count == 1:
            global file_win, file_label
            file_win = Toplevel()
            file_win.title("Download Videos via Python by Gloryness")
            file_win.iconbitmap('C:/Users/Gloryness/AppData/Local/atom/app.ico')
            file_win.resizable(False, False)
            file_win.configure(bg='#cbdbfc', bd=5)
            file_win.geometry("600x450")
            file_win.protocol("WM_DELETE_WINDOW", lambda: file_fix(file_win))

            file_label = Label(file_win, text="Filesystem Options", bg='#cbdbfc', font="Cooper 18")
            file_label.place(x=180, y=3)

            file_count += 1
        else:
            pass

    @staticmethod
    def download_options_window():
        global download_count
        if download_count == 1:
            global download_win, download_label
            download_win = Toplevel()
            download_win.title("Download Videos via Python by Gloryness")
            download_win.iconbitmap('C:/Users/Gloryness/AppData/Local/atom/app.ico')
            download_win.resizable(False, False)
            download_win.configure(bg='#cbdbfc', bd=5)
            download_win.geometry("600x450")
            download_win.protocol("WM_DELETE_WINDOW", lambda: download_fix(download_win))

            download_label = Label(download_win, text="Downlaod Options", bg='#cbdbfc', font="Cooper 18")
            download_label.place(x=186, y=3)

            download_count += 1
        else:
            pass

    @staticmethod
    def other_options_window():
        global other_count
        if other_count == 1:
            global other_win, other_label
            other_win = Toplevel()
            other_win.title("Download Videos via Python by Gloryness")
            other_win.iconbitmap('C:/Users/Gloryness/AppData/Local/atom/app.ico')
            other_win.resizable(False, False)
            other_win.configure(bg='#cbdbfc', bd=5)
            other_win.geometry("600x450")
            other_win.protocol("WM_DELETE_WINDOW", lambda: other_fix(other_win))

            other_label = Label(other_win, text="Other Options", bg='#cbdbfc', font="Cooper 18")
            other_label.place(x=215, y=3)

            other_count += 1
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

def done():
    with yt.YoutubeDL(video_ops) as ydl:
        try:
            if ext_btn_var.get() == "WAV":
                raise yt.utils.DownloadError("<<<<<<<<<<<<<<>>>>>>>>>>>>>")
            ydl.download(['https://www.youtube.com/watch?v=LOQe63mBxWc'])
        except yt.utils.DownloadError:
            print(colorama.Fore.RED + "Sorry, but we could not download the requested format {}!\nThe video will be merged into a more suitable format instead."
                  .format(ext_btn_var.get().lower()) + colorama.Fore.RESET)

            if quality_btn_var.get() != "NONE" \
                and audio_btn_var.get() != "NONE":
                    video_ops.update(merge_output_format='mkv', outtmpl=destination_var.get() + '/%(title)s.%(ext)s')
                    with yt.YoutubeDL(video_ops) as ytd:
                        ytd.download(['https://www.youtube.com/watch?v=LOQe63mBxWc'])

            elif quality_btn_var.get() == "NONE" \
                and audio_btn_var.get() != "NONE":
                    if ext_btn_var.get() == ext_btn_options[1]:
                        video_ops.update(postprocessors=[{
                            "key": 'FFmpegExtractAudio',
                            "preferredcodec": 'mp3'
                            }], outtmpl=destination_var.get() + '/%(title)s.%(ext)s')
                        with yt.YoutubeDL(video_ops) as ytd:
                            try:
                                ytd.download(['https://www.youtube.com/watch?v=LOQe63mBxWc'])
                            except yt.utils.DownloadError:
                                video_ops.update(postprocessors=[{
                                    "key": 'FFmpegExtractAudio',
                                    "preferredcodec": 'wav'
                                }], outtmpl=destination_var.get() + '/%(title)s.%(ext)s.%(id)s)')
                                with yt.YoutubeDL(video_ops) as ytk:
                                    try:
                                        ytk.download(['https://www.youtube.com/watch?v=LOQe63mBxWc'])
                                    except yt.utils.DownloadError:
                                        pass

                    elif ext_btn_var.get() == ext_btn_options[4]:
                        video_ops.update(postprocessors=[{
                            "key": 'FFmpegExtractAudio',
                            "preferredcodec": 'wav'
                        }], outtmpl=destination_var.get() + '/%(title)s.%(ext)s')
                        with yt.YoutubeDL(video_ops) as ytd:
                            try:
                                ytd.download(['https://www.youtube.com/watch?v=LOQe63mBxWc'])
                            except yt.utils.DownloadError:
                                video_ops.update(postprocessors=[{
                                    "key": 'FFmpegExtractAudio',
                                    "preferredcodec": 'mp3'
                                }], outtmpl=destination_var.get() + '/%(title)s.%(ext)s.%(id)s)')
                                with yt.YoutubeDL(video_ops) as ytk:
                                    try:
                                        ytk.download(['https://www.youtube.com/watch?v=LOQe63mBxWc'])
                                    except yt.utils.DownloadError:
                                        pass

second_done_btn = Button(root, text="Done", bd=1, relief=SOLID, padx=25, state=DISABLED, command=done)
second_done_btn.place(x=220, y=314)

## Videos
video_ops = {
}

## URLs
URLS = [
]

mainloop()
