import tkinter as tk
from tkinter import ttk

class BorderedEntry(ttk.Entry):
    def __init__(self, root, *args, bordercolor, borderthickness=1,
                 background='#f0f0f0', foreground='black', **kwargs):
        super().__init__(root, *args, **kwargs)
        # Styles must have unique image, element, and style names to create
        # multiple instances. winfo_id() is good enough
        e_id = self.winfo_id()
        img_name = 'entryBorder{}'.format(e_id)
        element_name = 'bordercolor{}'.format(e_id)
        style_name = 'bcEntry{}.TEntry'.format(e_id)
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()
        self.img = tk.PhotoImage(img_name, width=width, height=height)
        self.img.put(bordercolor, to=(0, 0, width, height))
        self.img.put(background, to=(borderthickness, borderthickness, width -
                     borderthickness, height - borderthickness))

        style = ttk.Style()
        style.element_create(element_name, 'image', img_name, sticky='nsew',
                             border=borderthickness)
        style.layout(style_name,
                     [('Entry.{}'.format(element_name), {'children': [(
                      'Entry.padding', {'children': [(
                          'Entry.textarea', {'sticky': 'nsew'})],
                          'sticky': 'nsew'})], 'sticky': 'nsew'})])
        style.configure(style_name, background=background,
                        foreground=foreground)
        self.config(style=style_name)