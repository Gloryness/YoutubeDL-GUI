import threading
from tkinter import *
from tkinter import ttk

count = 1
def reset(win):
    global count
    count = 1
    win.destroy()

class Help:
    def __init__(self, version):
        self.version = version

        global count
        if count == 1:
            self.help_win = Toplevel()
            self.help_win.title('Help  |  YoutubeDL GUI  |   v{}'.format(self.version))
            self.help_win.iconbitmap('images/#app.ico')
            self.help_win.resizable(False, False)
            self.help_win.configure(bg='#cbdbfc', bd=5)
            self.help_win.geometry("500x300")
            self.help_win.protocol('WM_DELETE_WINDOW', lambda: reset(self.help_win))

            exit_btn = ttk.Button(self.help_win, text="Exit", style="some.TButton", command=lambda: reset(self.help_win))
            exit_btn.place(x=410, y=2)
            count = 2

    # threading
    def ffmpeg_thread(self):
        thread = threading.Thread(target=self.ffmpeg_help)
        thread.start()

    def detect_urls_thread(self):
        thread = threading.Thread(target=self.detect_urls_help)
        thread.start()

    def downloading_videos_thread(self):
        thread = threading.Thread(target=self.downloading_videos_help)
        thread.start()

    def other_issues_thread(self):
        thread = threading.Thread(target=self.other_issues)
        thread.start()

    def add_label(self, win, text, bg=None, fg="black", x=None, y=None, font=None):
        label_adder = Label(win, text=text, fg=fg, bg=bg, font=font if font is not None else "TkDefaultFont")
        label_adder.place(x=x, y=y)

    def ffmpeg_help(self):
        self.add_label(self.help_win, "FFmpeg - Help", '#cbdbfc', x=190, y=3, font="Cooper 11")
        self.add_label(self.help_win, "If you have not already read the How-To on github, then it's all explained here:", '#cbdbfc', x=5, y=40)

        self.add_label(self.help_win, "If you've tried downloading a video, and got an error based on files that couldnt merge"
                                      "\nor too high quality then that means you have not installed FFmpeg.", '#cbdbfc', x=5, y=80)

        self.add_label(self.help_win, "To install FFmpeg, simply go to the 'Tools' tab of this GUI and click 'Install FFmpeg'.", '#cbdbfc', x=5, y=127)

        self.add_label(self.help_win, "After that, I recommend choosing the latest version and your architecture"
                                      "\n and then choose 'Static' for linking which should be automatic.", '#cbdbfc', x=5, y=160)

        self.add_label(self.help_win, "Once installed, find the folder that contains 'ffmpeg.exe', 'ffplay.exe' or 'ffprobe.exe'"
                                      "\nand then set that folder as your System Environmental Variable.", '#cbdbfc', x=5, y=210)

        self.add_label(self.help_win, "Then you should be done! If you have any issues, Google may have a better answer.", '#cbdbfc', x=5, y=270)

    def detect_urls_help(self):
        self.add_label(self.help_win, "Selenium - Help", '#cbdbfc', x=190, y=3, font="Cooper 11")

    def downloading_videos_help(self):
        self.add_label(self.help_win, "Downloading Videos - Help", '#cbdbfc', x=160, y=3, font="Cooper 11")

    def other_issues(self):
        self.add_label(self.help_win, "Other Issues - Help", '#cbdbfc', x=180, y=3, font="Cooper 11")