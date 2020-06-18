import threading
import webbrowser
from tkinter import *
from tkinter import ttk
from tkinter.font import *
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
            self.help_win = Tk()
            self.help_win.title('Help  |  YoutubeDL GUI  |   v{}'.format(self.version))
            self.help_win.iconbitmap('images/#app.ico')
            self.help_win.resizable(False, False)
            self.help_win.configure(bg='#cbdbfc', bd=5)
            self.help_win.geometry("500x300")
            self.help_win.protocol('WM_DELETE_WINDOW', lambda: reset(self.help_win))

            self.f = Font(family='TkDefaultFont', size=13, weight=BOLD)

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

    def add_label(self, win, text, bg="#ffffff", fg="black", x=1, y=1, font=None, bind=(False, None, None), bind1=(False, None), bind2=(False, None)):
        label_adder = Label(win, text=text, fg=fg, bg=bg, font=font if font is not None else "TkDefaultFont")
        label_adder.place(x=x, y=y)
        if bind[0]:
            label_adder.bind(bind[1], bind[2])
        if bind1[0]:
            label_adder.bind(bind1[1], lambda event: label_adder.config(bg="#859fd4"))
        if bind2[0]:
            label_adder.bind(bind2[1], lambda event: label_adder.config(bg="#cbdbfc"))

    def ffmpeg_help(self):
        self.add_label(self.help_win, "FFmpeg - Help", '#cbdbfc', x=190, y=3, font=self.f)
        self.add_label(self.help_win, "If you have not already read the How-To on github, then it's all explained here:", '#cbdbfc', x=5, y=40)

        self.add_label(self.help_win, "If you've tried downloading a video, and got an error based on files that couldnt merge"
                                      "\nor too high quality then that means you have not installed FFmpeg.", '#cbdbfc', x=5, y=80)

        self.add_label(self.help_win, "To install FFmpeg, simply go to the 'Tools' tab of this GUI and click 'Install FFmpeg'.", '#cbdbfc', x=5, y=127)

        self.add_label(self.help_win, "After that, I recommend choosing the latest version and your architecture"
                                      "\n and then choose 'Static' for linking which should be automatic.", '#cbdbfc', x=5, y=160)

        self.add_label(self.help_win, "Once installed, find the folder that contains 'ffmpeg.exe', 'ffplay.exe' or 'ffprobe.exe'"
                                      "\nand then set that folder as your System Environmental Variable.", '#cbdbfc', x=5, y=210)

        f = Font(family="TkDefaultFont", size=8, weight=BOLD)
        self.add_label(self.help_win, "(Control Panel>System>Advanced System Settings>Environmental Variables>Path>Edit)", '#cbdbfc', x=-3, y=245, font=f)

        self.add_label(self.help_win, "Then you should be done! If you have any issues, Google may have a better answer.", '#cbdbfc', x=5, y=270)

    def detect_urls_help(self):
        self.add_label(self.help_win, "Selenium - Help", '#cbdbfc', x=190, y=3, font=self.f)
        self.add_label(self.help_win, "The option that is next to the download button looks very intimidating, doesn't it?", '#cbdbfc', x=5, y=27)
        self.add_label(self.help_win, "It uses the well-known python module 'Selenium' for webbrowser automation.", '#cbdbfc', x=5, y=47)
        self.add_label(self.help_win, "You can use it as a normal browser, and clicking 'Execute' to catch all downloadable URLs.", '#cbdbfc', x=5, y=67)
        self.add_label(self.help_win, "But how do you use it?", '#cbdbfc', x=5, y=90)
        f = Font(family="TkDefaultFont", size=8, weight=BOLD)
        self.add_label(self.help_win, "- Install a WebDriver for the browser you want to use.", '#cbdbfc', x=5, y=110, font=f)
        self.add_label(self.help_win, "- You can do this by going to the 'Tools' tab and choosing 'Install WebDriver'.", '#cbdbfc', x=5, y=140, font=f)
        self.add_label(self.help_win, "- Next, find that .exe file that you installed and place it anywhere on your machine.", '#cbdbfc', x=5, y=170, font=f)
        self.add_label(self.help_win, "- Then go to 'Settings' in the 'File' tab and in Selenium Settings set the PATH to the .exe!", '#cbdbfc', x=5, y=200, font=f)
        self.add_label(self.help_win, "- If your using the Firefox browser you can choose to link your Firefox profile (optional).", '#cbdbfc', x=5, y=230, font=f)
        self.add_label(self.help_win, "- Other than that, you're ready to go!", '#cbdbfc', x=5, y=260, font=f)

    def downloading_videos_help(self):
        self.add_label(self.help_win, "Downloading Videos - Help", '#cbdbfc', x=140, y=3, font=self.f)
        self.add_label(self.help_win, "Looks like you need help with Downloading Videos. I got you covered!", '#cbdbfc', x=5, y=30)
        self.add_label(self.help_win, "Here are some common issues:", '#cbdbfc', x=5, y=50)
        f = Font(family="TkDefaultFont", size=8, weight=BOLD)
        self.add_label(self.help_win, "- Blocked Websites", '#cbdbfc', x=5, y=70, font=f)
        self.add_label(self.help_win, "- Bad Network", '#cbdbfc', x=5, y=90, font=f)
        self.add_label(self.help_win, "- Checked downloading.log or not?", '#cbdbfc', x=5, y=110, font=f)
        self.add_label(self.help_win, "- Has FFmpeg or something simallur been installed?", '#cbdbfc', x=5, y=130, font=f)
        self.add_label(self.help_win, "- Is FFmpeg a System Environmental Variable?", '#cbdbfc', x=5, y=150, font=f)
        self.add_label(self.help_win, "- Is the video available in your country?", '#cbdbfc', x=5, y=170, font=f)
        self.add_label(self.help_win, "If none of them options help, consider searching up the problem.", '#cbdbfc', x=5, y=200)
        self.add_label(self.help_win, "If still nothing, go to Other Options and check 'Print various debugging info' and then", '#cbdbfc', x=5, y=240)
        self.add_label(self.help_win, "download the video again and screenshot it and make an issue on ", '#cbdbfc', x=5, y=260)
        self.add_label(self.help_win, "GitHub.", '#cbdbfc', "blue", x=356, y=260,
                       bind=(True, "<Button-1>", lambda event: webbrowser.open('https://github.com/Gloryness/YoutubeDL-GUI/issues')), bind1=(True, "<Enter>"), bind2=(True, "<Leave>"))





    def other_issues(self):
        f = Font(family="TkDefaultFont", size=10, weight=BOLD)
        self.add_label(self.help_win, "Other Issues - Help", '#cbdbfc', x=180, y=3, font=self.f)
        self.add_label(self.help_win, "If you need any other help, then feel free to create an Issue on github.", '#cbdbfc', x=25, y=120, font=f)
        self.add_label(self.help_win, "A response usually comes within the day.", '#cbdbfc', x=100, y=140, font=f)

        self.add_label(self.help_win, ">> Github Link <<", '#cbdbfc', "blue", x=170, y=200, font=f,
                       bind=(True, "<Button-1>", lambda event: webbrowser.open('https://github.com/Gloryness/YoutubeDL-GUI/issues')), bind1=(True, "<Enter>"), bind2=(True, "<Leave>"))

t = Help('1.0.0')
t.other_issues()
mainloop()