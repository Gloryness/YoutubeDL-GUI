from tkinter import *
from tkinter import ttk, filedialog, messagebox

import threading
import json
import os

def reset_settings_window(win, download_btn, done_btn, _stabalize, apply_btn):
    _stabalize[0] = 1
    _stabalize[1] = 1
    _stabalize[2] = 1
    _stabalize[3] = 1
    state = str(done_btn['state'])
    if state == 'disabled':
        download_btn.configure(state=ACTIVE)
    setting = SettingsWindow()
    setting.hold_variables(apply_btn, win)

class SettingsWindow(object):
    """
    * Settings Window
    """
    def __init__(self, version=None, download_btn=None, done_btn=None, stabalize=None): # we need these from the main file.
        self.version = version
        self.download_btn = download_btn
        self.done_btn = done_btn
        self._stabalize = stabalize
        self._title = 'Settings   |   Gloryness  |  v{}'.format(self.version)
        self._icon = 'images/#app.ico'
        self._size = '550x370'

    def on_settings(self):
        thread = threading.Thread(target=self.settings)
        thread.start()

    def update_apply_button(self):
        self.apply_btn.configure(state=NORMAL)
        self.restore_settings.configure(state=NORMAL)

    def update_apply_button_with_event(self, event):
        self.apply_btn.configure(state=NORMAL)
        self.restore_settings.configure(state=NORMAL)
        if str(self.selenium_tab['state']) == 'disabled':
            with open(self.name_of_json) as f:
                self.data = json.load(f)

            for key, value in self.data.items():
                if key == 'settings_sync':
                    for self.sync_sel_name, self.sync_sel_detail in value[1].items():
                        pass
                if browser_var.get() == 'Firefox':
                    ##

                    Y_CORD1 = 180
                    Y_CORD2 = 200
                    Y_CORD3 = 196

                    self.browser_profile_label.place(x=15, y=Y_CORD1)
                    self.browser_profile_entry.place(x=15, y=Y_CORD2)
                    self.browser_profile_button.place(x=292, y=Y_CORD3)

                    ##

                    Y_CORD1 = 250
                    Y_CORD2 = 270

                    self.which_link_label.place(x=15, y=Y_CORD1)
                    self.which_link_entry.place(x=15, y=Y_CORD2)
                else:
                    self.browser_profile_label.place_forget()
                    self.browser_profile_entry.place_forget()
                    self.browser_profile_button.place_forget()

                    ##

                    Y_CORD1 = 180
                    Y_CORD2 = 200

                    self.which_link_label.place(x=15, y=Y_CORD1)
                    self.which_link_entry.place(x=15, y=Y_CORD2)


    # general

    def update_general_dropdowns(self):
        self.update_apply_button()
        if auto_fill_formats_var.get():
            self.quality_dropdown.configure(state=NORMAL)
            self.audio_dropdown.configure(state=NORMAL)
            self.ext_dropdown.configure(state=NORMAL)
            self.click_dropdown.configure(state=NORMAL)
        elif not auto_fill_formats_var.get():
            self.quality_dropdown.configure(state=DISABLED)
            self.audio_dropdown.configure(state=DISABLED)
            self.ext_dropdown.configure(state=DISABLED)
            self.click_dropdown.configure(state=DISABLED)

    def browse_initialdir(self):
        self.update_apply_button()
        if len(initialdir_var.get()) <= 2:
            browse = filedialog.askdirectory(initialdir='C:/', parent=self.settings_win)
            self.initialdir_entry.configure(state=NORMAL)
            self.initialdir_entry.delete(0, END)
            self.initialdir_entry.insert(0, browse)
            self.initialdir_entry.configure(state=DISABLED)
        else:
            browse = filedialog.askdirectory(initialdir=initialdir_var.get(), parent=self.settings_win)
            self.initialdir_entry.configure(state=NORMAL)
            self.initialdir_entry.delete(0, END)
            self.initialdir_entry.insert(0, browse)
            self.initialdir_entry.configure(state=DISABLED)

    def destination_autofill(self):
        self.update_apply_button()
        if len(auto_fill_destination_var.get()) <= 2:
            browse = filedialog.askdirectory(initialdir='C:/', parent=self.settings_win)
            self.auto_fill_destination_entry.configure(state=NORMAL)
            self.auto_fill_destination_entry.delete(0, END)
            self.auto_fill_destination_entry.insert(0, browse)
            self.auto_fill_destination_entry.configure(state=DISABLED)
        else:
            browse = filedialog.askdirectory(initialdir=auto_fill_destination_var.get(), parent=self.settings_win)
            self.auto_fill_destination_entry.configure(state=NORMAL)
            self.auto_fill_destination_entry.delete(0, END)
            self.auto_fill_destination_entry.insert(0, browse)
            self.auto_fill_destination_entry.configure(state=DISABLED)

    # selenium

    def browse_for_path(self):
        self.update_apply_button()
        with open(self.name_of_json) as f:
            data = json.load(f)

        for key, value in data.items():
            if key == 'settings':
                for general_name, general_detail in value[0].items():
                    pass
        if len(browser_path_var.get()) <= 2:
            browse = filedialog.askopenfilename(initialdir=general_detail['initialdir'], title="Select WebDriver",
                                                filetypes=(("executable files", "*.exe"), ("all files", "*.*")), parent=self.settings_win)
            self.browser_path_entry.configure(state=NORMAL)
            self.browser_path_entry.delete(0, END)
            self.browser_path_entry.insert(0, browse)
            self.browser_path_entry.configure(state=DISABLED)
        else:
            browse = filedialog.askopenfilename(initialdir=browser_path_var.get(), title="Select WebDriver",
                                                filetypes=(("executable files", "*.exe"), ("all files", "*.*")), parent=self.settings_win)
            self.browser_path_entry.configure(state=NORMAL)
            self.browser_path_entry.delete(0, END)
            self.browser_path_entry.insert(0, browse)
            self.browser_path_entry.configure(state=DISABLED)

    def browse_for_profile(self):
        self.update_apply_button()
        messagebox.showwarning("!!! BE AWARE !!!",
                               "Please note that if you are going to put your default profile here, please don't as it could cause harm.\n\n"
                                "To be safe, just create a new profile and copy everything from the default into the new one to be safe of no corruption.",
                                parent=self.settings_win)
        with open(self.name_of_json) as f:
            data = json.load(f)

        for key, value in data.items():
            if key == 'settings':
                for general_name, general_detail in value[0].items():
                    pass
        if len(browser_profile_var.get()) <= 2:

            browse = filedialog.askdirectory(initialdir=general_detail['initialdir'], title="Select Profile", parent=self.settings_win)
            self.browser_profile_entry.configure(state=NORMAL)
            self.browser_profile_entry.delete(0, END)
            self.browser_profile_entry.insert(0, browse)
            self.browser_profile_entry.configure(state=DISABLED)
        else:
            browse = filedialog.askdirectory(initialdir=browser_profile_var.get(), title="Select Profile", parent=self.settings_win)
            self.browser_profile_entry.configure(state=NORMAL)
            self.browser_profile_entry.delete(0, END)
            self.browser_profile_entry.insert(0, browse)
            self.browser_profile_entry.configure(state=DISABLED)
            
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
                self.browser_profile_label.destroy()
                self.browser_profile_entry.destroy()
                self.browser_profile_button.destroy()
                self.which_link_label.destroy()
                self.which_link_entry.destroy()

            elif str(self.config_tab['state']) == 'disabled':
                # config
                self.name_of_json_label.destroy()
                self.name_of_json_entry.destroy()
                self.dont_save_file_options_check.destroy()
                self.dont_save_download_options_check.destroy()
                self.dont_save_other_options_check.destroy()
        except:
            pass

    def general_settings(self):
        global initialdir_var, remove_done_messagebox_var, auto_fill_destination_var, \
            remove_editformats_messagebox_var, auto_fill_formats_var, quality_dropdown_var, audio_dropdown_var, ext_dropdown_var, click_dropdown_var
        json_ = JsonWorker(self.general_tab, self.selenium_tab, self.config_tab)
        json_.work()
        self.delete_wigits()
        self.selenium_tab.config(state=NORMAL)
        self.general_tab.config(state=DISABLED)
        self.config_tab.config(state=NORMAL)
        self.restore_settings.configure(text="Restore General Settings")

        with open(self.name_of_json) as f:
            self.data = json.load(f)

        for key, value in self.data.items():
            if key == 'settings':
                for self.general_name, self.general_detail in value[0].items():
                    pass
                for self.sel_name, self.sel_detail in value[1].items():
                    pass
                for self.config_name, self.config_detail in value[2].items():
                    pass
            elif key == 'settings_sync':
                for self.sync_general_name, self.sync_general_detail in value[0].items():
                    pass
                for self.sync_sel_name, self.sync_sel_detail in value[1].items():
                    pass
                for self.sync_config_name, self.sync_config_detail in value[2].items():
                    pass

        self.initialdir_label = Label(self.settings_win, text="When you click \"Browse\", open this folder for your initial directory:", bg='#cbdbfc')
        self.initialdir_label.place(x=4, y=40)

        initialdir_var = StringVar()
        self.initialdir_entry = Entry(self.settings_win, width=45, state=DISABLED, relief=SOLID, textvariable=initialdir_var)
        self.initialdir_entry.place(x=4, y=62)

        if len(initialdir_var.get()) <= 1:
            self.initialdir_entry.configure(state=NORMAL)
            self.initialdir_entry.delete(0, END)
            self.initialdir_entry.insert(0, self.sync_general_detail['initialdir'])
            self.initialdir_entry.configure(state=DISABLED)

        self.initialdir_button = ttk.Button(self.settings_win, text="Set InitialDir", style='option5_5.TButton', state=NORMAL, command=self.browse_initialdir)
        self.initialdir_button.place(x=280, y=60)

        remove_done_messagebox_var = BooleanVar()
        self.remove_done_messagebox_check = ttk.Checkbutton(self.settings_win, text="Disable the messagebox after you click \"Done\".", style='option9.TCheckbutton',
                                                            onvalue=True, offvalue=False, variable=remove_done_messagebox_var, command=self.update_apply_button)
        self.remove_done_messagebox_check.place(x=4, y=100)
        remove_done_messagebox_var.set(self.sync_general_detail['disable_done_messagebox'])

        self.auto_fill_destination_lbl = Label(self.settings_win, text="On loading, auto-fill the \"Destination\" to a certain destination:", bg='#cbdbfc')
        self.auto_fill_destination_lbl.place(x=4, y=140)

        auto_fill_destination_var = StringVar()
        self.auto_fill_destination_entry = Entry(self.settings_win, width=45, state=DISABLED, relief=SOLID, textvariable=auto_fill_destination_var)
        self.auto_fill_destination_entry.place(x=4, y=162)

        if len(auto_fill_destination_var.get()) <= 1:
            self.auto_fill_destination_entry.configure(state=NORMAL)
            self.auto_fill_destination_entry.delete(0, END)
            self.auto_fill_destination_entry.insert(0, self.sync_general_detail['auto_fill_destination'])
            self.auto_fill_destination_entry.configure(state=DISABLED)

        self.auto_fill_destination_btn = ttk.Button(self.settings_win, text="Set Auto-Fill", style='option5_5.TButton', state=NORMAL, command=self.destination_autofill)
        self.auto_fill_destination_btn.place(x=280, y=160)

        remove_editformats_messagebox_var = BooleanVar()
        self.remove_editformats_messagebox_check = ttk.Checkbutton(self.settings_win, text="Disabled the messagebox after you click \"Edit Formats\".", style='option9.TCheckbutton',
                                                                   onvalue=True, offvalue=False, variable=remove_editformats_messagebox_var, command=self.update_apply_button)
        self.remove_editformats_messagebox_check.place(x=4, y=200)
        remove_editformats_messagebox_var.set(self.sync_general_detail['disabled_editformat_messagebox'])

        auto_fill_formats_var = BooleanVar()
        self.auto_fill_formats_check = ttk.Checkbutton(self.settings_win, text="On loading, auto-set all formats to chosen formats and auto-click \"Done\".", style='option9.TCheckbutton',
                                                                    onvalue=True, offvalue=False, variable=auto_fill_formats_var, command=self.update_general_dropdowns)
        self.auto_fill_formats_check.place(x=4, y=240)
        auto_fill_formats_var.set(self.sync_general_detail['auto_format_and_click'])

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

        quality_dropdown_var = StringVar()
        self.quality_dropdown = ttk.OptionMenu(self.settings_win, quality_dropdown_var, *quality_btn_options, command=self.update_apply_button_with_event)
        self.quality_dropdown.place(x=20, y=266, width=80)
        quality_dropdown_var.set(self.sync_general_detail['formats'][0])

        audio_dropdown_var = StringVar()
        self.audio_dropdown = ttk.OptionMenu(self.settings_win, audio_dropdown_var, *audio_btn_options, command=self.update_apply_button_with_event)
        self.audio_dropdown.place(x=120, y=266, width=80)
        audio_dropdown_var.set(self.sync_general_detail['formats'][1])

        ext_dropdown_var = StringVar()
        self.ext_dropdown = ttk.OptionMenu(self.settings_win, ext_dropdown_var, *ext_btn_options, command=self.update_apply_button_with_event)
        self.ext_dropdown.place(x=220, y=266, width=80)
        ext_dropdown_var.set(self.sync_general_detail['formats'][2])

        click_dropdown_var = StringVar()
        self.click_dropdown = ttk.OptionMenu(self.settings_win, click_dropdown_var, *click_btn_options, command=self.update_apply_button_with_event)
        self.click_dropdown.place(x=320, y=266, width=130)
        click_dropdown_var.set(self.sync_general_detail['formats'][3])

        if auto_fill_formats_var.get():
            self.quality_dropdown.configure(state=NORMAL)
            self.audio_dropdown.configure(state=NORMAL)
            self.ext_dropdown.configure(state=NORMAL)
            self.click_dropdown.configure(state=NORMAL)

        elif not auto_fill_formats_var.get():
            self.quality_dropdown.configure(state=DISABLED)
            self.audio_dropdown.configure(state=DISABLED)
            self.ext_dropdown.configure(state=DISABLED)
            self.click_dropdown.configure(state=DISABLED)

    def selenium_settings(self):
        global browser_var, browser_path_var, browser_profile_var, which_link_var
        json_ = JsonWorker(self.general_tab, self.selenium_tab, self.config_tab)
        json_.work()
        self.delete_wigits()
        self.selenium_tab.config(state=DISABLED)
        self.general_tab.config(state=NORMAL)
        self.config_tab.config(state=NORMAL)
        self.restore_settings.configure(text="Restore Selenium Settings")

        with open(self.name_of_json) as f:
            self.data = json.load(f)

        for key, value in self.data.items():
            if key == 'settings':
                for self.general_name, self.general_detail in value[0].items():
                    pass
                for self.sel_name, self.sel_detail in value[1].items():
                    pass
                for self.config_name, self.config_detail in value[2].items():
                    pass
            elif key == 'settings_sync':
                for self.sync_general_name, self.sync_general_detail in value[0].items():
                    pass
                for self.sync_sel_name, self.sync_sel_detail in value[1].items():
                    pass
                for self.sync_config_name, self.sync_config_detail in value[2].items():
                    pass

        ##

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

        browser_var = StringVar()
        self.browser_list = ttk.OptionMenu(self.settings_win, browser_var, *self.browsers, command=self.update_apply_button_with_event)
        self.browser_list.place(x=15, y=65, width=120)

        browser_var.set(self.sync_sel_detail['browser'])

        ##

        self.browser_path_label = Label(self.settings_win, text="PATH directory for WebDriver: (REQUIRED)", bg='#cbdbfc')
        self.browser_path_label.place(x=15, y=110)

        browser_path_var = StringVar()
        self.browser_path_entry = Entry(self.settings_win, width=45, state=DISABLED, relief=SOLID, textvariable=browser_path_var)
        self.browser_path_entry.place(x=15, y=130)

        self.browser_path_button = ttk.Button(self.settings_win, text="Set PATH", style='option5_5.TButton', state=NORMAL, command=self.browse_for_path)
        self.browser_path_button.place(x=292, y=126)

        ##

        Y_CORD1 = 180
        Y_CORD2 = 200
        Y_CORD3 = 196

        self.browser_profile_label = Label(self.settings_win, text="PATH directory for Firefox Profile: (OPTIONAL)", bg='#cbdbfc')
        self.browser_profile_label.place(x=15, y=Y_CORD1)

        browser_profile_var = StringVar()
        self.browser_profile_entry = Entry(self.settings_win, width=45, state=DISABLED, relief=SOLID, textvariable=browser_profile_var)
        self.browser_profile_entry.place(x=15, y=Y_CORD2)

        self.browser_profile_button = ttk.Button(self.settings_win, text="Set PROFILE", style='option5_5.TButton', state=NORMAL, command=self.browse_for_profile)
        self.browser_profile_button.place(x=292, y=Y_CORD3)
        if self.sync_sel_detail['browser'] != 'Firefox':
            self.browser_profile_label.place_forget()
            self.browser_profile_entry.place_forget()
            self.browser_profile_button.place_forget()

        ##
        Y_CORD1 = 180
        Y_CORD2 = 200
        if self.sync_sel_detail['browser'] == 'Firefox':
            Y_CORD1 = 250
            Y_CORD2 = 270

        self.which_link_label = Label(self.settings_win, text="Enter which link to load when selenium is open: (default: https://www.youtube.com/)", bg='#cbdbfc')
        self.which_link_label.place(x=15, y=Y_CORD1)

        which_link_var = StringVar()
        self.which_link_entry = Entry(self.settings_win, width=45, state=NORMAL, relief=SOLID, textvariable=which_link_var)
        self.which_link_entry.place(x=15, y=Y_CORD2)
        self.which_link_entry.bind("<Key>", self.update_apply_button_with_event)

        ##

        if len(which_link_var.get()) <= 1:
            self.which_link_entry.delete(0, END)
            self.which_link_entry.insert(0, self.sync_sel_detail['link'])

        if len(browser_path_var.get()) <= 1:
            self.browser_path_entry.configure(state=NORMAL)
            self.browser_path_entry.delete(0, END)
            self.browser_path_entry.insert(0, self.sync_sel_detail['path'])
            self.browser_path_entry.configure(state=DISABLED)

        if len(browser_profile_var.get()) <= 1:
            self.browser_profile_entry.configure(state=NORMAL)
            self.browser_profile_entry.delete(0, END)
            self.browser_profile_entry.insert(0, self.sync_sel_detail['profile'])
            self.browser_profile_entry.configure(state=DISABLED)

    def configuration_settings(self):
        global name_of_json_var, dont_save_file_options_var, dont_save_download_options_var, dont_save_other_options_var
        json_ = JsonWorker(self.general_tab, self.selenium_tab, self.config_tab)
        json_.work()
        self.delete_wigits()
        self.selenium_tab.config(state=NORMAL)
        self.general_tab.config(state=NORMAL)
        self.config_tab.config(state=DISABLED)
        self.restore_settings.configure(text="Restore Config Settings")

        with open(self.name_of_json) as f:
            self.data = json.load(f)

        for key, value in self.data.items():
            if key == 'settings':
                for self.general_name, self.general_detail in value[0].items():
                    pass
                for self.sel_name, self.sel_detail in value[1].items():
                    pass
                for self.config_name, self.config_detail in value[2].items():
                    pass
            elif key == 'settings_sync':
                for self.sync_general_name, self.sync_general_detail in value[0].items():
                    pass
                for self.sync_sel_name, self.sync_sel_detail in value[1].items():
                    pass
                for self.sync_config_name, self.sync_config_detail in value[2].items():
                    pass

        self.name_of_json_label = Label(self.settings_win, text="Name of the .JSON file: (default: settings.json)", bg='#cbdbfc')
        self.name_of_json_label.place(x=15, y=40)

        name_of_json_var = StringVar()
        self.name_of_json_entry = Entry(self.settings_win, width=45, state=NORMAL, relief=SOLID, textvariable=name_of_json_var)
        self.name_of_json_entry.place(x=15, y=60)
        self.name_of_json_entry.bind("<Key>", self.update_apply_button_with_event)
        if len(name_of_json_var.get()) <= 1:
            self.name_of_json_entry.delete(0, END)
            self.name_of_json_entry.insert(0, self.sync_config_detail['name'])

        dont_save_file_options_var = BooleanVar()
        self.dont_save_file_options_check = ttk.Checkbutton(self.settings_win, text="Don't save File Options to .JSON", style='option9.TCheckbutton',
                                                                   onvalue=True, offvalue=False, variable=dont_save_file_options_var, command=self.update_apply_button)
        self.dont_save_file_options_check.place(x=15, y=110)
        dont_save_file_options_var.set(self.sync_config_detail['dont_save_file_options'])

        dont_save_download_options_var = BooleanVar()
        self.dont_save_download_options_check = ttk.Checkbutton(self.settings_win, text="Don't save Download Options to .JSON", style='option9.TCheckbutton',
                                                            onvalue=True, offvalue=False, variable=dont_save_download_options_var, command=self.update_apply_button)
        self.dont_save_download_options_check.place(x=15, y=140)
        dont_save_download_options_var.set(self.sync_config_detail['dont_save_download_options'])

        dont_save_other_options_var = BooleanVar()
        self.dont_save_other_options_check = ttk.Checkbutton(self.settings_win, text="Don't save Other Options to .JSON", style='option9.TCheckbutton',
                                                            onvalue=True, offvalue=False, variable=dont_save_other_options_var, command=self.update_apply_button)
        self.dont_save_other_options_check.place(x=15, y=170)
        dont_save_other_options_var.set(self.sync_config_detail['dont_save_other_options'])

    @property
    def name_of_json(self):
        with open('temp.json') as f:
            data = json.load(f)
        return data['name']

    def restore(self):
        if str(self.general_tab['state']) == 'disabled':
            self.initialdir_entry.configure(state=NORMAL)
            self.auto_fill_destination_entry.configure(state=NORMAL)
            self.initialdir_entry.delete(0, END)
            self.auto_fill_destination_entry.delete(0, END)
            remove_done_messagebox_var.set(False)
            auto_fill_destination_var.set('')
            remove_editformats_messagebox_var.set(False)
            auto_fill_formats_var.set(False)
            self.quality_dropdown.configure(state=NORMAL); self.audio_dropdown.configure(state=NORMAL); self.ext_dropdown.configure(state=NORMAL); self.click_dropdown.configure(state=NORMAL)
            quality_dropdown_var.set("1080p")
            audio_dropdown_var.set("1441k")
            ext_dropdown_var.set("MP4")
            click_dropdown_var.set("Auto-Click")
            self.quality_dropdown.configure(state=DISABLED); self.audio_dropdown.configure(state=DISABLED); self.ext_dropdown.configure(state=DISABLED); self.click_dropdown.configure(state=DISABLED)
            self.initialdir_entry.configure(state=DISABLED)
            self.auto_fill_destination_entry.configure(state=DISABLED)

        elif str(self.selenium_tab['state']) == 'disabled':
            browser_var.set('Firefox')
            self.browser_path_entry.configure(state=NORMAL)
            self.browser_path_entry.delete(0, END)
            self.browser_path_entry.configure(state=DISABLED)
            self.browser_profile_entry.configure(state=NORMAL)
            self.browser_profile_entry.delete(0, END)
            self.browser_profile_entry.configure(state=DISABLED)
            self.which_link_entry.delete(0, END)
            self.which_link_entry.insert(0, "https://www.youtube.com/")

        elif str(self.config_tab['state']) == 'disabled':
            self.name_of_json_entry.delete(0, END)
            self.name_of_json_entry.insert(0, 'settings.json')
            dont_save_file_options_var.set(False)
            dont_save_download_options_var.set(False)
            dont_save_other_options_var.set(False)

        self.apply_btn.configure(state=NORMAL)
        self.restore_settings.configure(state=DISABLED)

    def settings(self):
        if self._stabalize[3] == 1:
            self.download_btn.configure(state=DISABLED)
            self.settings_win = Toplevel()
            self.settings_win.title(self._title)
            self.settings_win.iconbitmap(self._icon)
            self.settings_win.resizable(False, False)
            self.settings_win.configure(bg='#cbdbfc', bd=5)
            self.settings_win.geometry(self._size)
            self.settings_win.protocol("WM_DELETE_WINDOW", lambda: reset_settings_window(self.settings_win, self.download_btn, self.done_btn, self._stabalize, self.apply_btn))

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

            self.general_tab = ttk.Button(self.settings_win, text="General Settings", style='option8.TButton', state=NORMAL, command=self.general_thread)
            self.general_tab.place(x=205, y=2)

            self.config_tab = ttk.Button(self.settings_win, text="Configuration Settings", style='option8.TButton', state=NORMAL, command=self.config_thread)
            self.config_tab.place(x=335, y=2)

            self.restore_settings = ttk.Button(self.settings_win, text="", style='option7.TButton', state=NORMAL, command=self.restore, width=25)
            self.restore_settings.place(x=1, y=335)

            self.apply_btn = ttk.Button(self.settings_win, text="Apply", state=DISABLED, style='option6.TButton', command=self.apply_settings)
            self.apply_btn.place(x=488, y=335)

            exit_btn = ttk.Button(self.settings_win, text="Exit", style='option6.TButton',
                                  command=lambda: reset_settings_window(self.settings_win, self.download_btn, self.done_btn, self._stabalize, self.apply_btn))
            exit_btn.place(x=418, y=335)

            self.general_settings()

            for index, var in enumerate(self._stabalize):
                self._stabalize[index] += 1
            print(self._stabalize)

    def hold_variables(self, apply_btn, win):
        with open(self.name_of_json) as f:
            self.data = json.load(f)
        for key, value in self.data.items():
            if key == 'settings':
                for self.general_name, self.general_detail in value[0].items():
                    pass
                for self.sel_name, self.sel_detail in value[1].items():
                    pass
                for self.config_name, self.config_detail in value[2].items():
                    pass
            elif key == 'settings_sync':
                for self.sync_general_name, self.sync_general_detail in value[0].items():
                    pass
                for self.sync_sel_name, self.sync_sel_detail in value[1].items():
                    pass
                for self.sync_config_name, self.sync_config_detail in value[2].items():
                    pass

        if str(apply_btn['state']) == 'normal':
            choice = messagebox.askyesno("???", "You have unsaved changed.\nAre you sure you want to Exit?", parent=win)
            if choice == 1:
                self.sync_general_detail['initialdir'] = self.general_detail['initialdir']
                self.sync_general_detail['disable_done_messagebox'] = self.general_detail['disable_done_messagebox']
                self.sync_general_detail['auto_fill_destination'] = self.general_detail['auto_fill_destination']
                self.sync_general_detail['disabled_editformat_messagebox'] = self.general_detail['disabled_editformat_messagebox']
                self.sync_general_detail['auto_format_and_click'] = self.general_detail['auto_format_and_click']
                self.sync_general_detail['formats'][0] = self.general_detail['formats'][0]
                self.sync_general_detail['formats'][1] = self.general_detail['formats'][1]
                self.sync_general_detail['formats'][2] = self.general_detail['formats'][2]
                self.sync_general_detail['formats'][3] = self.general_detail['formats'][3]
                self.sync_sel_detail['browser'] = self.sel_detail['browser']
                self.sync_sel_detail['path'] = self.sel_detail['path']
                self.sync_sel_detail['profile'] = self.sel_detail['profile']
                self.sync_sel_detail['link'] = self.sel_detail['link']
                self.sync_config_detail['name'] = self.config_detail['name']
                self.sync_config_detail['dont_save_file_options'] = self.config_detail['dont_save_file_options']
                self.sync_config_detail['dont_save_download_options'] = self.config_detail['dont_save_download_options']
                self.sync_config_detail['dont_save_other_options'] = self.config_detail['dont_save_other_options']

                with open('settings.json', 'w') as f:
                    json.dump(self.data, f, indent=3)
                win.destroy()
            else:
                pass
        else:
            win.destroy()

    def apply_settings(self):
        with open(self.name_of_json) as f:
            self.data = json.load(f)
        with open('temp.json') as d:
            other_data = json.load(d)

        for key, value in self.data.items():
            if key == 'settings':
                for self.general_name, self.general_detail in value[0].items():
                    pass
                for self.sel_name, self.sel_detail in value[1].items():
                    pass
                for self.config_name, self.config_detail in value[2].items():
                    pass
            elif key == 'settings_sync':
                for self.sync_general_name, self.sync_general_detail in value[0].items():
                    pass
                for self.sync_sel_name, self.sync_sel_detail in value[1].items():
                    pass
                for self.sync_config_name, self.sync_config_detail in value[2].items():
                    pass

        # the if statements will make it so if you make a change but dont switch tab, then it will instead save it here
        if str(self.general_tab['state']) == 'disabled':
            self.sync_general_detail['initialdir'] = initialdir_var.get()
            self.sync_general_detail['disable_done_messagebox'] = remove_done_messagebox_var.get()
            self.sync_general_detail['auto_fill_destination'] = auto_fill_destination_var.get()
            self.sync_general_detail['disabled_editformat_messagebox'] = remove_editformats_messagebox_var.get()
            self.sync_general_detail['auto_format_and_click'] = auto_fill_formats_var.get()
            self.sync_general_detail['formats'][0] = quality_dropdown_var.get()
            self.sync_general_detail['formats'][1] = audio_dropdown_var.get()
            self.sync_general_detail['formats'][2] = ext_dropdown_var.get()
            self.sync_general_detail['formats'][3] = click_dropdown_var.get()
        elif str(self.selenium_tab['state']) == 'disabled':
            self.sync_sel_detail['browser'] = browser_var.get()
            self.sync_sel_detail['path'] = browser_path_var.get()
            self.sync_sel_detail['profile'] = browser_profile_var.get()
            self.sync_sel_detail['link'] = which_link_var.get()
        elif str(self.config_tab['state']) == 'disabled':
            self.sync_config_detail['name'] = name_of_json_var.get()
            self.sync_config_detail['dont_save_file_options'] = dont_save_file_options_var.get()
            self.sync_config_detail['dont_save_download_options'] = dont_save_download_options_var.get()
            self.sync_config_detail['dont_save_other_options'] = dont_save_other_options_var.get()

        if self.sync_config_detail['name'].endswith('.json'):
            # saving it to the actual settings dict
            self.general_detail['initialdir'] = self.sync_general_detail['initialdir']
            self.general_detail['disable_done_messagebox'] = self.sync_general_detail['disable_done_messagebox']
            self.general_detail['auto_fill_destination'] = self.sync_general_detail['auto_fill_destination']
            self.general_detail['disabled_editformat_messagebox'] = self.sync_general_detail['disabled_editformat_messagebox']
            self.general_detail['auto_format_and_click'] = self.sync_general_detail['auto_format_and_click']
            self.general_detail['formats'][0] = self.sync_general_detail['formats'][0]
            self.general_detail['formats'][1] = self.sync_general_detail['formats'][1]
            self.general_detail['formats'][2] = self.sync_general_detail['formats'][2]
            self.general_detail['formats'][3] = self.sync_general_detail['formats'][3]
            self.sel_detail['browser'] = self.sync_sel_detail['browser']
            self.sel_detail['path'] = self.sync_sel_detail['path']
            self.sel_detail['profile'] = self.sync_sel_detail['profile']
            self.sel_detail['link'] = self.sync_sel_detail['link']
            self.config_detail['name'] = self.sync_config_detail['name']
            self.config_detail['dont_save_file_options'] = self.sync_config_detail['dont_save_file_options']
            self.config_detail['dont_save_download_options'] = self.sync_config_detail['dont_save_download_options']
            self.config_detail['dont_save_other_options'] = self.sync_config_detail['dont_save_other_options']
            other_data.update(prev_name=other_data.get('name'))
            other_data.update(name=self.config_detail['name'])

            # saving to file
            with open(other_data.get('prev_name'), 'w') as f:
                json.dump(self.data, f, indent=3)
                f.close()

            with open('temp.json', 'w') as d:
                json.dump(other_data, d, indent=3)
                d.close()

            # renaming the file if necessary
            if other_data.get('prev_name') and other_data.get('name') != 'settings.json':
                os.rename(other_data.get('prev_name'), other_data.get('name'))

            self.apply_btn.configure(state=DISABLED)
        else:
            messagebox.showwarning("???", "JSON filename must end with '.json'", parent=self.settings_win)

# noinspection PyUnresolvedReferences
class JsonWorker(SettingsWindow):

    def __init__(self, general, selenium, config, version=None, download_btn=None, done_btn=None, stabalize=None):
        SettingsWindow.__init__(self, version, download_btn, done_btn, stabalize)
        self.general = general
        self.selenium = selenium
        self.config = config

        with open(self.name_of_json) as f:
            self.data = json.load(f)

        for key, value in self.data.items():
            if key == 'settings':
                for self.general_name, self.general_detail in value[0].items():
                    pass
                for self.sel_name, self.sel_detail in value[1].items():
                    pass
                for self.config_name, self.config_detail in value[2].items():
                    pass
            elif key == 'settings_sync':
                for self.sync_general_name, self.sync_general_detail in value[0].items():
                    pass
                for self.sync_sel_name, self.sync_sel_detail in value[1].items():
                    pass
                for self.sync_config_name, self.sync_config_detail in value[2].items():
                    pass

    def work(self):
        if str(self.general['state']) == 'disabled':
            self.work_general()
        if str(self.selenium['state']) == 'disabled':
            self.work_selenium()
        if str(self.config['state']) == 'disabled':
            self.work_config()

        # saving to file
        with open(self.name_of_json, 'w') as f:
            json.dump(self.data, f, indent=3)

    def work_general(self):
        if initialdir_var.get() != self.sync_general_detail['initialdir']:
            self.sync_general_detail['initialdir'] = initialdir_var.get()

        if remove_done_messagebox_var.get() != self.sync_general_detail['disable_done_messagebox']:
            self.sync_general_detail['disable_done_messagebox'] = remove_done_messagebox_var.get()

        if auto_fill_destination_var.get() != self.sync_general_detail['auto_fill_destination']:
            self.sync_general_detail['auto_fill_destination'] = auto_fill_destination_var.get()

        if remove_editformats_messagebox_var.get() != self.sync_general_detail['disabled_editformat_messagebox']:
            self.sync_general_detail['disabled_editformat_messagebox'] = remove_editformats_messagebox_var.get()

        if auto_fill_formats_var.get() != self.sync_general_detail['auto_format_and_click']:
            self.sync_general_detail['auto_format_and_click'] = auto_fill_formats_var.get()

        if auto_fill_formats_var.get():
            if quality_dropdown_var.get() != self.sync_general_detail['formats'][0]:
                self.sync_general_detail['formats'][0] = quality_dropdown_var.get()

            if audio_dropdown_var.get() != self.sync_general_detail['formats'][1]:
                self.sync_general_detail['formats'][1] = audio_dropdown_var.get()

            if ext_dropdown_var.get() != self.sync_general_detail['formats'][2]:
                self.sync_general_detail['formats'][2] = ext_dropdown_var.get()

            if click_dropdown_var.get() != self.sync_general_detail['formats'][3]:
                self.sync_general_detail['formats'][3] = click_dropdown_var.get()

    def work_selenium(self):
        if browser_var.get() != self.sync_sel_detail['browser']:
            self.sync_sel_detail['browser'] = browser_var.get()

        if browser_path_var.get() != self.sync_sel_detail['path']:
            self.sync_sel_detail['path'] = browser_path_var.get()

        if self.sync_sel_detail['browser'] == 'Firefox':
            if browser_profile_var.get() != self.sync_sel_detail['profile']:
                self.sync_sel_detail['profile'] = browser_profile_var.get()

        if which_link_var.get() != self.sync_sel_detail['link']:
            self.sync_sel_detail['link'] = which_link_var.get()

    def work_config(self):
        if name_of_json_var.get() != self.sync_config_detail['name']:
            self.sync_config_detail['name'] = name_of_json_var.get()

        if dont_save_file_options_var.get() != self.sync_config_detail['dont_save_file_options']:
            self.sync_config_detail['dont_save_file_options'] = dont_save_file_options_var.get()

        if dont_save_download_options_var.get() != self.sync_config_detail['dont_save_download_options']:
            self.sync_config_detail['dont_save_download_options'] = dont_save_download_options_var.get()

        if dont_save_other_options_var.get() != self.sync_config_detail['dont_save_other_options']:
            self.sync_config_detail['dont_save_other_options'] = dont_save_other_options_var.get()