from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
import easygui as eg
import webbrowser
import threading as t
import os
import sys
import linecache
import subprocess
import idlelib.colorizer as ic
import idlelib.percolator as ip
import idlelib.autocomplete as iac
from tkterminal import Terminal
import re
from tkinter import font as tkfont
import pyglet


cdg = ic.ColorDelegator()


filename = None
file = None

class LineNumbers(Text):
    def __init__(self, master, self_widget, **kwargs):
        super().__init__(master, **kwargs)
 
        self.self_widget = self_widget
        self.self_widget.bind('<KeyRelease>', self.on_key_release)
        self.self_widget.bind('<KeyPress>', self.on_key_release)
 
        self.insert(1.0, '1')
        self.configure(state='disabled')
 
    def on_key_release(self, event=None):
        p, q = self.self_widget.index("@0,0").split('.')
        p = int(p)
        final_index = str(self.self_widget.index(END))
        num_of_lines = final_index.split('.')[0]
        line_numbers_string = "\n".join(str(p + no) for no in range(int(num_of_lines) - 1))
        width = len(str(num_of_lines))
 
        self.configure(state='normal', width=width)
        self.delete(1.0, END)
        self.insert(1.0, line_numbers_string)
        self.configure(state='disabled')

def openfile():
    global file, filename
    filename = eg.fileopenbox("Open your file", "Save as...", filetypes=[["*.py", "*.pyw", "*.pyc", "Python Files"], ["pyproject.toml", "setup.cfg", "setup.py", "Setup Files"]])
    file = open(filename, "w")
    editor_box.delete(1.0, END)
    editor_box.insert(1.0, open(filename).read())
    

def save():
    global file, filename
    if filename:
        file.write(editor_box.get("1.0", "end-1c"))
    else:
        saveas()

def saveas():
    global file, filename
    filename = eg.filesavebox("Save your file", "Save as...", filetypes=[["*.py", "*.pyw", "*.pyc", "Python Files"], ["pyproject.toml", "setup.cfg", "setup.py", "Setup Files"]])
    try:
        file = open(filename, "w")
        file.write(editor_box.get("1.0", "end-1c"))
    except:
        pass

def run_py():
    try:
        exec(editor_box.get("1.0", "end-1c"))
    except Exception as e:
        showwarning("Error", ReturnException(e))
def run(event=None):
    save()
    thread = t.Thread(target=lambda:run_py(), daemon=True)
    thread.start()
    

def showongithub():
    webbrowser.open("https://github.com/TheRealPenguin12/pynit")

def reportissue():
    issue_type = eg.choicebox("Which best identifies your issue", "Issue", ["bug", "enhancement", "feature request"])
    issue_labels = eg.multchoicebox("Which labels best identify your issue", "Issue", ["bug", "documentation", "duplicate", "enhancement", "good first issue", "help wanted", "invalid", "question", "wontfix"])
    issue_body = eg.codebox(f"Please enter your issue body. Markdown is supported.\n\nIssue type: {issue_type}\nIssue labels: " + str(issue_labels).replace("'", "").replace("[", "").replace("]", ""), "Issue")
    webbrowser.open(f"https://github.com/TheRealPenguin12/Editt/issues/new?title={issue_type}&body={issue_body}&labels=" + str(issue_labels).replace("'", "").replace("[", "").replace("]", "").replace(", ", ","))


root = Tk()


root.geometry("800x700")
root.title("__pynit__")
style = Style(root)
root.resizable(False, False)

editor_box = ScrolledText(root, height=30, wrap="word", undo=True)

l = LineNumbers(root, editor_box, width=1, height=30)

l.pack(side=LEFT, anchor="nw")

editor_box.pack(fill="x")

editor_box.focus_set()

ip.Percolator(editor_box).insertfilter(cdg)

acomplete = iac.AutoComplete()


tabs = Notebook(root)
tabs.pack(pady=0, expand=True, fill="x", anchor="w")

console = Frame(tabs)
terminal = Frame(tabs)

console.pack(fill='both', expand=True)
terminal.pack(fill='both', expand=True)

tabs.add(console, text='Console')
tabs.add(terminal, text='Terminal')


console_box = Text(console, height=15, state=DISABLED)

console_box.pack(fill="x", anchor="e")

ansi_font_format = {1: 'bold', 3: 'italic', 4: 'underline', 9: 'overstrike'}
ansi_font_reset = {21: 'bold', 23: 'italic', 24: 'underline', 29: 'overstrike'}
console_box.tag_configure('bold', font=('', 9, 'bold'))
console_box.tag_configure('italic', font=('', 9, 'italic'))
console_box.tag_configure('underline', underline=True)
console_box.tag_configure('overstrike', overstrike=True)
ansi_color_fg = {39: 'foreground default'}
ansi_color_bg = {49: 'background default'}
console_box.tag_configure('foreground default', foreground=console_box["fg"])
console_box.tag_configure('background default', background=console_box["bg"])
ansi_colors_dark = ['black', 'red', 'green', 'yellow', 'royal blue', 'magenta', 'cyan', 'light gray']
ansi_colors_light = ['dark gray', 'tomato', 'light green', 'light goldenrod', 'light blue', 'pink', 'light cyan', 'white']

for i, (col_dark, col_light) in enumerate(zip(ansi_colors_dark, ansi_colors_light)):
    ansi_color_fg[30 + i] = 'foreground ' + col_dark
    ansi_color_fg[90 + i] = 'foreground ' + col_light
    ansi_color_bg[40 + i] = 'background ' + col_dark
    ansi_color_bg[100 + i] = 'background ' + col_light
    console_box.tag_configure('foreground ' + col_dark, foreground=col_dark)
    console_box.tag_configure('background ' + col_dark, background=col_dark)
    console_box.tag_configure('foreground ' + col_light, foreground=col_light)
    console_box.tag_configure('background ' + col_light, background=col_light)
ansi_regexp = re.compile(r"\x1b\[((\d+;)*\d+)m")

def insert_ansi(txt, index="insert"):
    first_line, first_char = map(int, str(console_box.index(index)).split("."))
    if index == "end":
        first_line -= 1

    lines = txt.splitlines()
    if not lines:
        return
    console_box.insert(index, ansi_regexp.sub('', txt))
    opened_tags = {}

    def apply_formatting(code, code_index):
        if code == 0:
            for tag, start in opened_tags.items():
                console_box.tag_add(tag, start, code_index)
            opened_tags.clear()
        elif code in ansi_font_format:
            tag = ansi_font_format[code]
            opened_tags[tag] = code_index
        elif code in ansi_font_reset:
            tag = ansi_font_reset[code]
            if tag in opened_tags:
                console_box.tag_add(tag, opened_tags[tag], code_index)
                opened_tags.remove(tag)
        elif code in ansi_color_fg:
            for tag in tuple(opened_tags):
                if tag.startswith('foreground'):
                    console_box.tag_add(tag, opened_tags[tag], code_index)
                    opened_tags.remove(tag)
            opened_tags[ansi_color_fg[code]] = code_index
        elif code in ansi_color_bg:
            for tag in tuple(opened_tags):
                if tag.startswith('background'):
                    console_box.tag_add(tag, opened_tags[tag], code_index)
                    opened_tags.remove(tag)
            opened_tags[ansi_color_bg[code]] = code_index

    def find_ansi(line_txt, line_nb, char_offset):
        delta = -char_offset
        for match in ansi_regexp.finditer(line_txt):
            codes = [int(c) for c in match.groups()[0].split(';')]
            start, end = match.span()
            for code in codes:
                apply_formatting(code, "{}.{}".format(line_nb, start - delta))
            delta += end - start
    find_ansi(lines[0], first_line, first_char)
    for line_nb, line in enumerate(lines[1:], first_line + 1):
        find_ansi(line, line_nb, 0)
    for tag, start in opened_tags.items():
        console_box.tag_add(tag, start, "end")

class Log(object):
    def __init__(self):
        self.log = console_box

    def write(self, msg):
        console_box.config(state=NORMAL)
        insert_ansi(msg, END)
        console_box.config(state=DISABLED)


editor_box.bind("<F5>", run)

def OnArrow(event):
    widget = event.widget
    l.yview_moveto(widget.yview()[0])
    l.mark_set("insert", widget.index("insert"))

editor_box.bind("<KeyRelease-Up>", OnArrow)
editor_box.bind("<KeyRelease-Down>", OnArrow)
editor_box.bind("<KeyRelease-Up>", OnArrow)
editor_box.bind("<KeyRelease-Down>", OnArrow)

sys.stdout = Log()

menubar = Menu(root)

menubar.add_command(label="Run", command=run)
menubar.add_command(label="Paste", command=lambda:editor_box.insert(END, root.clipboard_get()))


file = Menu(menubar, tearoff=0)

file.add_command(label="New", command=saveas)  
file.add_command(label="Open", command=openfile)  
file.add_command(label="Save", command=save)  
file.add_command(label="Save as", command=saveas)    
file.add_separator()  
file.add_command(label="Exit", command=root.destroy)

menubar.add_cascade(label="File", menu=file)

_help = Menu(menubar, tearoff=0)  
_help.add_command(label="About", command=lambda:showinfo(title="__pynit__", message="Version: 0.0.1\nCode Source: main.py"))
_help.add_command(label="Github", command=showongithub)
_help.add_command(label="Report Issue", command=reportissue)
menubar.add_cascade(label="Help", menu=_help) 

root.config(menu=menubar)

terminal = Terminal(terminal, pady=5, padx=5, background="black", foreground="white", insertbackground="white")
terminal.shell = True
terminal.pack(expand=True, fill='both')

l.bindtags((str(l), str(root), "all"))

try:
    root.mainloop()
except:
    quit()
