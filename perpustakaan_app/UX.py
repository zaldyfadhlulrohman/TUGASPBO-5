import tkinter as tk
from tkinter import messagebox
from db import connect
from dashboard import Dashboard  

def apply_theme(root):
    style = ttk.Style(root)
    try: style.theme_use('clam')
    except: pass
    primary = '#0b74de'; muted = "#f6f4fb"; surface = '#ffffff'; fg = '#1b1b1b'
    style.configure('TFrame', background=muted)
    style.configure('Card.TFrame', background=surface, relief='flat')
    style.configure('TLabel', background=muted, foreground=fg)
    style.configure('Header.TLabel', font=('Inter', 14, 'bold'), background=primary, foreground='white')
    style.configure('TButton', font=('Inter', 10), padding=6)
    style.configure('Primary.TButton', background=primary, foreground='white')
    style.configure('Danger.TButton', foreground='white', background='#e54d42')
    style.configure('Treeview', background='white', fieldbackground='white', foreground='#111111')
    style.configure('Treeview.Heading', font=('Inter', 10, 'bold'))
