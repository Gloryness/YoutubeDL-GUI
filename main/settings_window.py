from tkinter import *
from tkinter import ttk
from tkinter import filedialog
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
        self.settings_win = None

    def on_settings(self):
        thread = threading.Thread(target=self.settings)
        thread.start()

    def update_apply_button(self):
        self.apply_btn.configure(state=NORMAL)

    def update_apply_button_with_event(self, event):
        self.apply_btn.configure(state=NORMAL)

    # general

    def update_general_dropdowns(self):
        self.update_apply_button()
        if self.auto_fill_formats_var.get():
            self.quality_dropdown.configure(state=NORMAL)
            self.audio_dropdown.configure(state=NORMAL)
            self.ext_dropdown.configure(state=NORMAL)
            self.click_dropdown.configure(state=NORMAL)
        elif not self.auto_fill_formats_var.get():
            self.quality_dropdown.configure(state=DISABLED)
            self.audio_dropdown.configure(state=DISABLED)
            self.ext_dropdown.configure(state=DISABLED)
            self.click_dropdown.configure(state=DISABLED)

    def browse_initialdir(self):
        self.update_apply_button()
        if len(self.initialdir_var.get()) <= 2:
            browse = filedialog.askdirectory(initialdir='C:/', parent=self.settings_win)
            self.initialdir_entry.configure(state=NORMAL)
            self.initialdir_entry.delete(0, END)
            self.initialdir_entry.insert(0, browse)
            self.initialdir_entry.configure(state=DISABLED)
        else:
            browse = filedialog.askdirectory(initialdir=self.initialdir_var.get(), parent=self.settings_win)
            self.initialdir_entry.configure(state=NORMAL)
            self.initialdir_entry.delete(0, END)
            self.initialdir_entry.insert(0, browse)
            self.initialdir_entry.configure(state=DISABLED)

    def destination_autofill(self):
        self.update_apply_button()
        if len(self.auto_fill_destination_var.get()) <= 2:
            browse = filedialog.askdirectory(initialdir='C:/', parent=self.settings_win)
            self.auto_fill_destination_entry.configure(state=NORMAL)
            self.auto_fill_destination_entry.delete(0, END)
            self.auto_fill_destination_entry.insert(0, browse)
            self.auto_fill_destination_entry.configure(state=DISABLED)
        else:
            browse = filedialog.askdirectory(initialdir=self.auto_fill_destination_var.get(), parent=self.settings_win)
            self.auto_fill_destination_entry.configure(state=NORMAL)
            self.auto_fill_destination_entry.delete(0, END)
            self.auto_fill_destination_entry.insert(0, browse)
            self.auto_fill_destination_entry.configure(state=DISABLED)

    # selenium

    def browse_for_path(self):
        self.update_apply_button()
        if len(self.browser_path_var.get()) <= 2:
            browse = filedialog.askopenfilename(initialdir='C:/', title="Select WebDriver",
                                                filetypes=(("executable files", "*.exe"), ("all files", "*.*")), parent=self.settings_win)
            self.browser_path_entry.configure(state=NORMAL)
            self.browser_path_entry.delete(0, END)
            self.browser_path_entry.insert(0, browse)
            self.browser_path_entry.configure(state=DISABLED)
        else:
            browse = filedialog.askopenfilename(initialdir=self.browser_path_var.get(), title="Select WebDriver",
                                                filetypes=(("executable files", "*.exe"), ("all files", "*.*")), parent=self.settings_win)
            self.browser_path_entry.configure(state=NORMAL)
            self.browser_path_entry.delete(0, END)
            self.browser_path_entry.insert(0, browse)
            self.browser_path_entry.configure(state=DISABLED)
            
    # threading

    def general_thread(self):
        thread = threading.Thread(target=self.general_settings)
        thread.start()

    def selenium_thread(self):
        thread2 = threading.Thread(target=self.selenium_settings)
        thread2.start()

    def config_thread(self):
        thread3 = threading.Thread(target=self.configuration_settings)
        thread3.start()

    # settings

    def delete_wigits(self):
        try:
            if str(self.general_tab['state']) == 'disabled':
                # general
                self.initialdir_label.destroy()
                self.initialdir_entry.destroy()
                self.initialdir_button.destroy()
                self.remove_done_messagebox_check.destroy()
                self.auto_fill_destination_lbl.destroy()
                self.auto_fill_destination_entry.destroy()
                self.auto_fill_destination_btn.destroy()
                self.remove_editformats_messagebox_check.destroy()
                self.auto_fill_formats_check.destroy()
                self.quality_dropdown.destroy()
                self.audio_dropdown.destroy()
                self.ext_dropdown.destroy()
                self.click_dropdown.destroy()

            elif str(self.selenium_tab['state']) == 'disabled':
                # selenium
                self.browser_list_label.destroy()
                self.browser_list.destroy()
                self.browser_path_label.destroy()
                self.browser_path_entry.destroy()
                self.browser_path_button.destroy()
                self.which_link_label.destroy()
                self.which_link_entry.destroy()

            elif str(self.config_tab['state']) == 'disabled':
                # config
                self.name_of_json_label.destroy()
                self.name_of_json_entry.destroy()
                self.dont_save_file_options_check.destroy()
                self.dont_save_download_options_check.destroy()
                self.dont_save_other_options_check.destroy()
                self.dont_save_settings_check.destroy()
        except:
            pass

    def general_settings(self):
        self.delete_wigits()
        self.selenium_tab.config(state=NORMAL)
        self.general_tab.config(state=DISABLED)
        self.config_tab.config(state=NORMAL)
        self.restore_settings.configure(text="Restore General Settings")

        self.initialdir_label = Label(self.settings_win, text="When you click \"Browse\", open this folder for your initial directory:", bg='#cbdbfc')
        self.initialdir_label.place(x=4, y=40)

        self.initialdir_var = StringVar()
        self.initialdir_entry = Entry(self.settings_win, width=45, state=DISABLED, relief=SOLID, textvariable=self.initialdir_var)
        self.initialdir_entry.place(x=4, y=62)

        self.initialdir_button = ttk.Button(self.settings_win, text="Set InitialDir", style='option5_5.TButton', state=NORMAL, command=self.browse_initialdir)
        self.initialdir_button.place(x=280, y=60)

        self.remove_done_messagebox_var = BooleanVar()
        self.remove_done_messagebox_check = ttk.Checkbutton(self.settings_win, text="Disable the messagebox after you click \"Done\".", style='option9.TCheckbutton',
                                                            onvalue=True, offvalue=False, variable=self.remove_done_messagebox_var, command=self.update_apply_button)
        self.remove_done_messagebox_check.place(x=4, y=100)

        self.auto_fill_destination_lbl = Label(self.settings_win, text="On loading, auto-fill the \"Destination\" to a certain destination:", bg='#cbdbfc')
        self.auto_fill_destination_lbl.place(x=4, y=140)

        self.auto_fill_destination_var = StringVar()
        self.auto_fill_destination_entry = Entry(self.settings_win, width=45, state=DISABLED, relief=SOLID, textvariable=self.auto_fill_destination_var)
        self.auto_fill_destination_entry.place(x=4, y=162)

        self.auto_fill_destination_btn = ttk.Button(self.settings_win, text="Set Auto-Fill", style='option5_5.TButton', state=NORMAL, command=self.destination_autofill)
        self.auto_fill_destination_btn.place(x=280, y=160)

        self.remove_editformats_messagebox_var = BooleanVar()
        self.remove_editformats_messagebox_check = ttk.Checkbutton(self.settings_win, text="Disabled the messagebox after you click \"Edit Formats\".", style='option9.TCheckbutton',
                                                                   onvalue=True, offvalue=False, variable=self.remove_editformats_messagebox_var, command=self.update_apply_button)
        self.remove_editformats_messagebox_check.place(x=4, y=200)

        self.auto_fill_formats_var = BooleanVar()
        self.auto_fill_formats_check = ttk.Checkbutton(self.settings_win, text="On loading, auto-set all formats to chosen formats and auto-click \"Done\".", style='option9.TCheckbutton',
                                                                    onvalue=True, offvalue=False, variable=self.auto_fill_formats_var, command=self.update_general_dropdowns)
        self.auto_fill_formats_check.place(x=4, y=240)

        quality_btn_options = [
            "1080p",
            "1080p",
            "720p",
            "480p",
            "360p",
            "NONE"
        ]
        audio_btn_options = [
            "1441k",
            "1441k",
            "800k",
            "467k",
            "258k",
            "NONE"
        ]
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
        click_btn_options = [
            "Auto-Click",
            "Auto-Click",
            "Don't Auto-Click"
        ]

        self.quality_dropdown_var = StringVar()
        self.quality_dropdown = ttk.OptionMenu(self.settings_win, self.quality_dropdown_var, *quality_btn_options, command=self.update_apply_button_with_event)
        self.quality_dropdown.place(x=20, y=266, width=80)

        self.audio_dropdown_var = StringVar()
        self.audio_dropdown = ttk.OptionMenu(self.settings_win, self.audio_dropdown_var, *audio_btn_options, command=self.update_apply_button_with_event)
        self.audio_dropdown.place(x=120, y=266, width=80)

        self.ext_dropdown_var = StringVar()
        self.ext_dropdown = ttk.OptionMenu(self.settings_win, self.ext_dropdown_var, *ext_btn_options, command=self.update_apply_button_with_event)
        self.ext_dropdown.place(x=220, y=266, width=80)

        self.click_dropdown_var = StringVar()
        self.click_dropdown = ttk.OptionMenu(self.settings_win, self.click_dropdown_var, *click_btn_options, command=self.update_apply_button_with_event)
        self.click_dropdown.place(x=320, y=266, width=130)

        if self.auto_fill_formats_var.get():
            self.quality_dropdown.configure(state=NORMAL)
            self.audio_dropdown.configure(state=NORMAL)
            self.ext_dropdown.configure(state=NORMAL)
            self.click_dropdown.configure(state=NORMAL)

        elif not self.auto_fill_formats_var.get():
            self.quality_dropdown.configure(state=DISABLED)
            self.audio_dropdown.configure(state=DISABLED)
            self.ext_dropdown.configure(state=DISABLED)
            self.click_dropdown.configure(state=DISABLED)

    def selenium_settings(self):
        self.delete_wigits()
        self.selenium_tab.config(state=DISABLED)
        self.general_tab.config(state=NORMAL)
        self.config_tab.config(state=NORMAL)
        self.restore_settings.configure(text="Restore Selenium Settings")

        self.browser_list_label = Label(self.settings_win, text="Preferred Browser: (REQUIRED)", bg='#cbdbfc')
        self.browser_list_label.place(x=15, y=40)

        self.browsers = [
            'Firefox',
            'Firefox',
            'Chrome',
            'Safari',
            'Opera',
            'Edge',
            'Internet Explorer'
        ]

        self.browser_list_var = StringVar()
        self.browser_list = ttk.OptionMenu(self.settings_win, self.browser_list_var, *self.browsers, command=self.update_apply_button_with_event)
        self.browser_list.place(x=15, y=65, width=120)

        self.browser_list_var.set(self.browsers[1])

        self.browser_path_label = Label(self.settings_win, text="PATH directory for WebDriver: (REQUIRED)", bg='#cbdbfc')
        self.browser_path_label.place(x=15, y=120)

        self.browser_path_var = StringVar()
        self.browser_path_entry = Entry(self.settings_win, width=45, state=DISABLED, relief=SOLID, textvariable=self.browser_path_var)
        self.browser_path_entry.place(x=15, y=140)

        self.browser_path_button = ttk.Button(self.settings_win, text="Set PATH", style='option5_5.TButton', state=NORMAL, command=self.browse_for_path)
        self.browser_path_button.place(x=292, y=136)

        self.which_link_label = Label(self.settings_win, text="Enter which link to load when selenium is open: (default: https://www.youtube.com/)", bg='#cbdbfc')
        self.which_link_label.place(x=15, y=200)

        self.which_link_var = StringVar()
        self.which_link_entry = Entry(self.settings_win, width=45, state=NORMAL, relief=SOLID, textvariable=self.which_link_var)
        self.which_link_entry.place(x=15, y=220)
        self.which_link_entry.bind("<Key>", self.update_apply_button_with_event)
        if len(self.which_link_var.get()) <= 3:
            self.which_link_entry.delete(0, END)
            self.which_link_entry.insert(0, 'https://www.youtube.com/')

    def configuration_settings(self):
        self.delete_wigits()
        self.selenium_tab.config(state=NORMAL)
        self.general_tab.config(state=NORMAL)
        self.config_tab.config(state=DISABLED)
        self.restore_settings.configure(text="Restore Config Settings")

        self.name_of_json_label = Label(self.settings_win, text="Name of the .JSON file: (default: settings.json)", bg='#cbdbfc')
        self.name_of_json_label.place(x=15, y=40)

        self.name_of_json_var = StringVar()
        self.name_of_json_entry = Entry(self.settings_win, width=45, state=NORMAL, relief=SOLID, textvariable=self.name_of_json_var)
        self.name_of_json_entry.place(x=15, y=60)
        if len(self.name_of_json_var.get()) <= 0:
            self.name_of_json_entry.delete(0, END)
            self.name_of_json_entry.insert(0, 'settings')

        self.dont_save_file_options_var = BooleanVar()
        self.dont_save_file_options_check = ttk.Checkbutton(self.settings_win, text="Don't save File Options to .JSON", style='option9.TCheckbutton',
                                                                   onvalue=True, offvalue=False, variable=self.dont_save_file_options_var, command=self.update_apply_button)
        self.dont_save_file_options_check.place(x=15, y=110)

        self.dont_save_download_options_var = BooleanVar()
        self.dont_save_download_options_check = ttk.Checkbutton(self.settings_win, text="Don't save Download Options to .JSON", style='option9.TCheckbutton',
                                                            onvalue=True, offvalue=False, variable=self.dont_save_download_options_var, command=self.update_apply_button)
        self.dont_save_download_options_check.place(x=15, y=140)

        self.dont_save_other_options_var = BooleanVar()
        self.dont_save_other_options_check = ttk.Checkbutton(self.settings_win, text="Don't save Other Options to .JSON", style='option9.TCheckbutton',
                                                            onvalue=True, offvalue=False, variable=self.dont_save_other_options_var, command=self.update_apply_button)
        self.dont_save_other_options_check.place(x=15, y=170)

        self.dont_save_settings_var = BooleanVar()
        self.dont_save_settings_check = ttk.Checkbutton(self.settings_win, text="Don't save Settings to .JSON", style='option9.TCheckbutton',
                                                            onvalue=True, offvalue=False, variable=self.dont_save_settings_var, command=self.update_apply_button)
        self.dont_save_settings_check.place(x=15, y=200)

    def restore(self):
        if str(self.general_tab['state']) == 'disabled':
            pass

        elif str(self.selenium_tab['state']) == 'disabled':
            pass

        elif str(self.config_tab['state']) == 'disabled':
            pass

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

            def action(event):
                print(event.x, event.y)

            self.settings_win.bind("<Button-1>", action)

            border = LabelFrame(self.settings_win, height=368.5, width=549.5, bg='#cbdbfc', bd=4, font="Cooper 18", labelanchor=N, relief=SOLID)
            border.place(x=-5, y=-4)

            style21 = ttk.Style()
            style21.configure('option5_5.TButton', background='black', width=12)
            style21.configure('option6.TButton', background='black', width=7)
            style21.configure('option7.TButton', background='black', width=22)
            style21.configure('option8.TButton', background='black', width=20, borderwidth=1, focusthickness=3)
            style21.map('option8.TButton', background=[('active', '#d2d2d2')])
            style21.configure('option9.TCheckbutton', background='#cbdbfc')

            self.selenium_tab = ttk.Button(self.settings_win, text="Selenium Settings", style='option8.TButton', state=NORMAL, command=self.selenium_thread)
            self.selenium_tab.place(x=75, y=2)

            self.general_tab = ttk.Button(self.settings_win, text="General Settings", style='option8.TButton', state=DISABLED, command=self.general_thread)
            self.general_tab.place(x=205, y=2)

            self.config_tab = ttk.Button(self.settings_win, text="Configuration Settings", style='option8.TButton', state=NORMAL, command=self.config_thread)
            self.config_tab.place(x=335, y=2)

            self.restore_settings = ttk.Button(self.settings_win, text="", style='option7.TButton', state=NORMAL, command=self.restore, width=25)
            self.restore_settings.place(x=1, y=335)

            exit_btn = ttk.Button(self.settings_win, text="Exit", style='option6.TButton',
                                  command=lambda: reset_settings_window(self.settings_win, self.download_btn, self.done_btn, self._stabalize))
            exit_btn.place(x=418, y=335)

            self.apply_btn = ttk.Button(self.settings_win, text="Apply", state=DISABLED, style='option6.TButton', command=self.apply_settings)
            self.apply_btn.place(x=488, y=335)

            if str(self.general_tab['state']) == 'disabled':
                self.general_settings()

            elif str(self.selenium_tab['state']) == 'disabled':
                self.selenium_settings()

            elif str(self.config_tab['state']) == 'disabled':
                self.configuration_settings()


            for index, var in enumerate(self._stabalize):
                self._stabalize[index] += 1
            print(self._stabalize)

    def apply_settings(self):
        self.apply_btn.configure(state=DISABLED)
