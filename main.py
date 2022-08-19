from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from ttkthemes import ThemedTk
import easygui as eg
import webbrowser
import threading as t
import os
import sys
import linecache
import subprocess

filename = None
file = None

class LineNumbers(Text):
    def __init__(self, master, text_widget, **kwargs):
        super().__init__(master, **kwargs)
 
        self.text_widget = text_widget
        self.text_widget.bind('<KeyRelease>', self.on_key_release)
        self.text_widget.bind('<KeyPress>', self.on_key_release)
 
        self.insert(1.0, '1')
        self.configure(state='disabled')
 
    def on_key_release(self, event=None):
        p, q = self.text_widget.index("@0,0").split('.')
        p = int(p)
        final_index = str(self.text_widget.index(END))
        num_of_lines = final_index.split('.')[0]
        line_numbers_string = "\n".join(str(p + no) for no in range(int(num_of_lines) - 1))
        width = len(str(num_of_lines))
 
        self.configure(state='normal', width=width)
        self.delete(1.0, END)
        self.insert(1.0, line_numbers_string)
        self.configure(state='disabled')

def ReturnException(e):
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print(f"Editt: { filename.split('/')[len(filename.split('/')) - 1] }: Error: {e}")
    return '{}: {}'.format(e, filename)

def reload():
    pass
def save():
    global file, filename
    if filename:
        file.write(editor_box.get("1.0", "end-1c"))
    else:
        saveas()

def saveas():
    global file, filename
    filename = eg.filesavebox("Save your file", "Save as...", default="untitled.py", filetypes=[["*.py", "*.pyw", "*.pyc", "Python Files"], ["pyproject.toml", "setup.cfg", "setup.py", "Setup Files"]])
    try:
        file = open(filename, "w")
        file.write(editor_box.get("1.0", "end-1c"))
    except:
        saveas()

def run_py():
    print(f"Editt: main.py: Run { filename.split('/')[len(filename.split('/')) - 1] }")
    try:
        exec(editor_box.get("1.0", "end-1c"))
    except Exception as e:
        showwarning("Error", ReturnException(e))
def run(event):
    save()
    thread = t.Thread(target=lambda:run_py(), daemon=True)
    thread.start()

def showongithub():
    webbrowser.open("https://github.com/TheRealPenguin12/Editt")

def reportissue():
    issue_type = eg.choicebox("Which best identifies your issue", "Issue", ["bug", "enhancement", "feature request"])
    issue_labels = eg.multchoicebox("Which labels best identify your issue", "Issue", ["bug", "documentation", "duplicate", "enhancement", "good first issue", "help wanted", "invalid", "question", "wontfix"])
    issue_body = eg.codebox(f"Please enter your issue body. Markdown is supported.\n\nIssue type: {issue_type}\nIssue labels: " + str(issue_labels).replace("'", "").replace("[", "").replace("]", ""), "Issue")
    webbrowser.open(f"https://github.com/TheRealPenguin12/Editt/issues/new?title={issue_type}&body={issue_body}&labels=" + str(issue_labels).replace("'", "").replace("[", "").replace("]", "").replace(", ", ","))


root = ThemedTk(theme="arc")


root.geometry("800x700")
root.title("Editt")
style = Style(root)
style.theme_use("default")
root.resizable(False, False)




menubar = Menu(root)

file = Menu(menubar, tearoff=0)

file.add_command(label="New", underline=0)  
file.add_command(label="Open", underline=0)  
file.add_command(label="Save", underline=0, command=save)  
file.add_command(label="Save as", underline=2, command=saveas)    
file.add_separator()  
file.add_command(label="Exit", command=root.destroy, underline=1)

menubar.add_cascade(label="File", menu=file, underline=0)

_help = Menu(menubar, tearoff=0)  
_help.add_command(label="About", command=lambda:showinfo(title="Editt", message="Version: 0.0.1\nCode Source: main.py"), underline=0)
_help.add_command(label="Github", command=showongithub, underline=0)
_help.add_command(label="Report Issue", command=reportissue, underline=0)
menubar.add_cascade(label="Help", menu=_help, underline=0) 

root.config(menu=menubar)


editor_box = ScrolledText(root, height=30, wrap="word", undo=True)

l = LineNumbers(root, editor_box, width=1, height=30)

l.pack(side=LEFT, anchor="nw")

editor_box.pack(fill="x")


console_box = ScrolledText(root, height=15, state=DISABLED)

console_box.pack(fill="x")

class Log(object):
    def __init__(self):
        self.log = console_box

    def write(self, msg):
        self.log.config(state=NORMAL)
        self.log.insert(END, msg)
        self.log.config(state=DISABLED)


editor_box.bind("<F5>", run)

sys.stdout = Log()

try:
    root.mainloop()
except:
    quit()
