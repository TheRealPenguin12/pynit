from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *
from ttkthemes import ThemedTk
import easygui as eg
import webbrowser
import os

def showongithub():
    webbrowser.open("https://github.com/TheRealPenguin12/Editt")
def reportissue():
    issue_type = eg.choicebox("Which best identifies your issue", "Issue", ["bug", "enhancement", "feature request"])
    issue_labels = eg.multchoicebox("Which labels best identify your issue", "Issue", ["bug", "documentation", "duplicate", "enhancement", "good first issue", "help wanted", "invalid", "question", "wontfix"])
    issue_body = eg.codebox(f"Please enter your issue body. Markdown is supported.\n\nIssue type: {issue_type}\nIssue labels: " + str(issue_labels).replace("'", "").replace("[", "").replace("]", ""), "Issue")
    webbrowser.open(f"https://github.com/TheRealPenguin12/Editt/issues/new?title={issue_type}&body={issue_body}&labels=" + str(issue_labels).replace("'", "").replace("[", "").replace("]", "").replace(", ", ","))
root = ThemedTk(theme="arc")


root.geometry("500x400")
root.title("Editt")
style = Style(root)
style.theme_use("default")
root.resizable(False, False)


menubar = Menu(root)

file = Menu(menubar, tearoff=0)

file.add_command(label="New")  
file.add_command(label="Open")  
file.add_command(label="Save")  
file.add_command(label="Save as")    
file.add_separator()  
file.add_command(label="Exit", command=root.destroy)

menubar.add_cascade(label="File", menu=file)

_help = Menu(menubar, tearoff=0)  
_help.add_command(label="About", command=lambda:showinfo(title="Editt", message="Version: 0.0.1\nCode Source: main.py"))
_help.add_command(label="Github", command=showongithub)
_help.add_command(label="Report Issue", command=reportissue)
menubar.add_cascade(label="Help", menu=_help) 

root.config(menu=menubar)


root.mainloop()
