from tkinter import *
from tkinter import ttk
import threading

def reset_settings_window(win, download_btn, done_btn, _stabalize):
    _stabalize[0] = 1
    _stabalize[1] = 1
    _stabalize[2] = 1
    _stabalize[3] = 1
    state = str(done_btn['state'])
    if state == 'disabled':
        download_btn.configure(state=ACTIVE)
    win.destroy()

class SettingsWindow(object):
    """
    * Settings Window
    """
    def __init__(self, version, download_btn, done_btn, stabalize): # we need these from the main file.
        self.version = version
        self.download_btn = download_btn
        self.done_btn = done_btn
        self._stabalize = stabalize
        self._title = 'Youtube-DL GUI   |   Gloryness  |  v{}'.format(self.version)
        self._icon = 'images/#app.ico'
        self._size = '550x370'
        self.apply_btn = None
        self.settings_win = None

    def on_settings(self):
        thread = threading.Thread(target=self.settings)
        thread.start()

    def settings(self):
        if self._stabalize[3] == 1:
            self.download_btn.configure(state=DISABLED)
            self.settings_win = Toplevel()
            self.settings_win.title(self._title)
            self.settings_win.iconbitmap(self._icon)
            self.settings_win.resizable(False, False)
            self.settings_win.configure(bg='#cbdbfc', bd=5)
            self.settings_win.geometry(self._size)
            self.settings_win.protocol("WM_DELETE_WINDOW", lambda: reset_settings_window(self.settings_win, self.download_btn, self.done_btn, self._stabalize))

            border = LabelFrame(self.settings_win, height=368.5, width=549.5, bg='#cbdbfc', bd=4, font="Cooper 18", labelanchor=N, relief=SOLID)
            border.place(x=-5, y=-4)

            style = ttk.Style()
            style.configure('option.TButton', background='black', width=7)

            exit_btn = ttk.Button(self.settings_win, text="Exit", style='option.TButton',
                                  command=lambda: reset_settings_window(self.settings_win, self.download_btn, self.done_btn, self._stabalize))
            exit_btn.place(x=418, y=335)

            self.apply_btn = ttk.Button(self.settings_win, text="Apply", state=DISABLED, style='option.TButton', command=self.apply_settings)
            self.apply_btn.place(x=488, y=335)


            index = 0
            for i in range(4):
                self._stabalize[index] += 1
                index += 1
            index = 0
            print(self._stabalize)

    def apply_settings(self):
        pass