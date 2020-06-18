import os
import threading
import subprocess

try:
    subprocess.call(f'TASKKILL /IM "Youtube-DL GUI.exe" /F')
except:
    quit()

try:
    with open('Youtube-DL GUI_update.exe') as f:
        f.close()
except:
    quit()

def delete_old_exe():
    os.remove('Youtube-DL GUI.exe')
    thread = threading.Timer(0.5, rename_new_exe)
    thread.start()

def rename_new_exe():
    os.rename('Youtube-DL GUI_update.exe', 'Youtube-DL GUI.exe')
    thread = threading.Timer(1.5, start_up_new_exe)

def start_up_new_exe():
    subprocess.call('"Youtube-DL GUI".exe')

thread = threading.Timer(1.0, delete_old_exe)
thread.start()
