from tkinter import *
from tkinter import ttk
import threading
import os
from PIL import Image, ImageTk
import youtube_dl as yt

def my_hook(d):
    global status, merged

    if kill_event.is_set():
        print("\nTerminated")
        delthread = threading.Timer(3.0, lambda: os.remove(d['tmpfilename']))
        delthread.start()
        raise ConnectionAbortedError

    if pause_event.is_set():
        print("\nPaused")
        raise ConnectionAbortedError

    if d['status'] == 'finished':
        if merged:
            status = 'Finished'
            update_dict()

        else:
            status = 'Post Processing'
            merged = True
            update_dict()

        treeview.item(row, text=meta['title'])
        treeview.set(row, 'ext', f'.{meta["ext"].lower()}')
        treeview.set(row, 'size', d['_total_bytes_str'])
        treeview.set(row, 'percent', '100.0%')
        treeview.set(row, 'eta', '0:00')
        treeview.set(row, 'speed', 'N/A')
        treeview.set(row, 'status', status)
        thread_event = threading.Event()
        thread_event.wait(1.50)

    if d['status'] == 'downloading':
        if status != 'Downloading':
            status = 'Downloading'
            update_dict()
        treeview.item(row, text=meta['title'])
        treeview.set(row, 'ext', f'.{meta["ext"].lower()}')
        treeview.set(row, 'size', d['_total_bytes_str'])
        treeview.set(row, 'percent', d['_percent_str'])
        treeview.set(row, 'eta', d['_eta_str'])
        treeview.set(row, 'speed', d['_speed_str'])
        treeview.set(row, 'status', status)

    if d['status'] == 'error':
        if status != 'Error':
            status = 'Error'
            update_dict()
        treeview.item(row, text=meta['title'])
        treeview.set(row, 'ext', f'.{meta["ext"].lower()}')
        treeview.set(row, 'size', '-')
        treeview.set(row, 'percent', '-')
        treeview.set(row, 'eta', '-')
        treeview.set(row, 'speed', '-')
        treeview.set(row, 'status', status)


class MyLogger:

    @staticmethod
    def debug(msg):
        thread_event = threading.Event()
        thread_event.wait(0.25)

    @staticmethod
    def warning(msg):
        if msg == "ERROR: unable to download video data: ":
            pass
        else:
            global status
            if status != 'Error':
                status = 'Error'
                update_dict()
            treeview.item(row, text=meta['title'])
            treeview.set(row, 'ext', f'.{meta["ext"].lower()}')
            treeview.set(row, 'size', '-')
            treeview.set(row, 'percent', '-')
            treeview.set(row, 'eta', '-')
            treeview.set(row, 'speed', '-')
            treeview.set(row, 'status', status)
            print(msg)

    @staticmethod
    def error(msg):
        if msg == "ERROR: unable to download video data: ":
            pass
        else:
            global status
            if status != 'Error':
                status = 'Error'
                update_dict()
            treeview.item(row, text=meta['title'])
            treeview.set(row, 'ext', f'.{meta["ext"].lower()}')
            treeview.set(row, 'size', '-')
            treeview.set(row, 'percent', '-')
            treeview.set(row, 'eta', '-')
            treeview.set(row, 'speed', '-')
            treeview.set(row, 'status', status)
            print(msg)

root = Tk()
root.title("Learning Tkinter - TreeView")
root.configure(bg='#ededed', bd=5)
root.geometry("1000x280")
root.minsize(1000, 280) # can set the minimum size
root.maxsize(1000, 560) # can set the maximum size

def resize(event):
    try:
        height = root.winfo_height()
        terminate_btn.place(x=920, y=height-50)
        pause_btn.place(x=500, y=height-50)
    except:
        pass

root.bind("<Configure>", resize)

treeview = ttk.Treeview(root)
treeview.grid(padx=29)

treeview.config(height=10)

treeview.config(columns=('ext', 'size', 'percent', 'eta', 'speed', 'status'))
treeview.column('#0', width=280, anchor=W)
treeview.column('ext', width=100, anchor=W)
treeview.column('size', width=100, anchor=W)
treeview.column('percent', width=100, anchor=W)
treeview.column('eta', width=100, anchor=W)
treeview.column('speed', width=100, anchor=W)
treeview.column('status', width=150, anchor=W)

treeview.heading('#0', text="Title", anchor=W)
treeview.heading('ext', text="Extension", anchor=W)
treeview.heading('size', text="Size", anchor=W)
treeview.heading('percent', text="Percent", anchor=W)
treeview.heading('eta', text="ETA", anchor=W)
treeview.heading('speed', text="Speed", anchor=W)
treeview.heading('status', text="Status", anchor=W)

status = 'Queued'
row = 'URL1'
merged = False
rows = ['URL1']

row_dict = {
    "URL1": status
}

treeview.insert("", '0', row, text="-")
treeview.set(row, 'ext', '-')
treeview.set(row, 'size', '-')
treeview.set(row, 'percent', '0.0%')
treeview.set(row, 'eta', '-')
treeview.set(row, 'speed', '-')
treeview.set(row, 'status', status)

count = 1
def callback(event):
    global count
    def remove(i):
        treeview.selection_remove(i)
    def assign():
        global count
        count = 1
    if count == 1:
        count = 2
        for i in row_dict:
            if row_dict.get(i) == 'Terminated':
                remove(i)
            if row_dict.get(i) == 'Queued':
                remove(i)
        thread = threading.Timer(0.2, assign) # using threading to stop this function from looping
        thread.start()

def update_dict():
    row_dict.update(URL1=status)
    print(row_dict)

def pause_thread():
    def pause():
        if treeview.selection() == ():
            pass
        else:
            global resume_btn, resume_img, status

            status = 'Paused'
            update_dict()
            treeview.set(row, 'status', status)
            pause_btn.destroy()
            resume_img = ImageTk.PhotoImage(Image.open('images/#resume_32px.png'))
            resume_btn = ttk.Button(root, image=resume_img, command=resume_thread)
            resume_btn.place(x=500, y=root.winfo_height()-50)

            pause_event.set()

    pause_thread = threading.Thread(target=pause)
    pause_thread.start()

def resume_thread():
    def resume():
        if treeview.selection() == ():
            pass
        else:
            global pause_btn, pause_img, status

            status = 'Resuming'
            update_dict()
            treeview.set(row, 'status', status)
            resume_btn.destroy()
            pause_img = ImageTk.PhotoImage(Image.open('images/#pause_32px.png'))
            pause_btn = ttk.Button(root, image=pause_img, command=pause_thread)
            pause_btn.place(x=500, y=root.winfo_height()-50)

            resume_event.set()

            if resume_event.is_set():
                pause_event.clear()
                resume_event.clear()
                download_ytdl()

    resume_thread = threading.Thread(target=resume)
    resume_thread.start()

def terminate_thread():
    def terminate():
        if treeview.selection() == ():
            pass
        else:
            global status

            status = 'Terminated'
            treeview.item(row, text='TERMINATED')
            treeview.set(row, 'ext', f'N/A')
            treeview.set(row, 'size', 'N/A')
            treeview.set(row, 'percent', '0.0%')
            treeview.set(row, 'eta', '0:00')
            treeview.set(row, 'speed', 'N/A')
            treeview.set(row, 'status', status)
            update_dict()
            treeview.selection_remove(row)

            kill_event.set()

    terminate_thread = threading.Thread(target=terminate)
    terminate_thread.start()

treeview.bind("<<TreeviewSelect>>", callback)

treeview.config(selectmode='browse') # allow 1 at a time to be selected

terminate_img = ImageTk.PhotoImage(Image.open('images/#stop_32px.png'))
terminate_btn = ttk.Button(root, image=terminate_img, command=terminate_thread)
terminate_btn.place(x=920, y=230)

pause_img = ImageTk.PhotoImage(Image.open('images/#pause_32px.png'))
pause_btn = ttk.Button(root, image=pause_img, command=pause_thread)
pause_btn.place(x=500, y=230)

pause_event = threading.Event()
resume_event = threading.Event()
kill_event = threading.Event()

video_ops = {
    'outtmpl': 'R:/Downloaded Videos/%(title)s.%(ext)s',
    'format': 'bestvideo[height<=360,width<=640]+bestaudio/best[abr<=1441]',
    'ext': 'mkv',
    'merge_output_format': 'mkv',
    'quiet': True,
    'progress_hooks': [my_hook],
    'logger': MyLogger()
}

link = 'https://www.youtube.com/watch?v=QglaLzo_aPk'

def download_ytdl():
    with yt.YoutubeDL(video_ops) as ydl:
        global meta, status

        if status == 'Queued':
            meta = ydl.extract_info(link, download=False)

            status = 'Pre Processing'
            update_dict()
            treeview.item(row, text=link)
            treeview.set(row, 'status', status)

            thread_event = threading.Event()
            thread_event.wait(1.00)

        try:
            ydl.download([link])
        except yt.utils.DownloadError as exc:
            if status == 'Terminated':
                kill_event.clear()

yt_thread = threading.Timer(5.0, download_ytdl)
yt_thread.start()

mainloop()