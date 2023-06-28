from tkinter import *
from tkinter import ttk

top = Tk()
def calculate(*args):
    try:
        value = float(feet.get())
        meters.set(int(0.3048 * value * 10000.0 + 0.5)/10000.0)
    except ValueError:
        pass

root = Tk()
root.title("Feet to Meters")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
top.mainloop()

import tkinter as tk
from tkinter import filedialog

filetypes = (
    ('Text files', '*.TXT'),
    ('All files', '*.*'),
)

# open-file dialog
root = tk.Tk()
filename = tk.filedialog.askopenfilename(
    title='Select a file...',
    filetypes=filetypes,
)
root.destroy()
print(filename)

# save-as dialog
root = tk.Tk()
filename = tk.filedialog.asksaveasfilename(
    title='Save as...',
    filetypes=filetypes,
    defaultextension='.txt'
)
root.destroy()
print(filename)
# filename == 'path/to/myfilename.txt' if you type 'myfilename'
# filename == 'path/to/myfilename.abc' if you type 'myfilename.abc'

