import os
import threading
import subprocess

subprocess.call(f'TASKKILL /IM "Youtube-DL GUI.exe" /F')

def delete_old_exe():
    os.remove('Youtube-DL GUI.exe')
    thread = threading.Timer(0.5, rename_new_exe)
    thread.start()

def rename_new_exe():
    os.rename('Youtube-DL GUI_update.exe', 'Youtube-DL GUI.exe')

thread = threading.Timer(1.0, delete_old_exe)
thread.start()