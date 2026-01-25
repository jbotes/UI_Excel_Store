# based on some ideas from https://www.youtube.com/watch?v=ibXT3SbfkOc&list=WL&index=59

import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as tb

class FormMain:

    def __init__(self):
        self.build_controls()
        self.refresh_tree()
        self.form_main.mainloop()

    def refresh_tree(self):
        self.tree.delete(*self.tree.get_children())
        for record in [["FSP1", "James", "Werner","28 Feb 2025"],["FSP2", "James", "werner","29 feb 2025"]]:
            self.tree.insert("",tk.END,values=record)

    def build_controls(self):
        self.form_main = tb.Window(themename="superhero") #tk.Tk()
        self.form_main.title("BDE FSP Allocations Form")
        
        #create the controls
        frame_top_left = tk.Frame(self.form_main, relief="solid", borderwidth=2)
        button_edit = tk.Button(frame_top_left, text='Edit', width=10)
        #button_delete = tk.Button(frame_top_left, text='Delete', width=10)
        themes = ['cosmo','flatly', 'sandstone']
        frame_top_right = tk.Frame(self.form_main)  # Create frame first
        self.combo_theme = ttk.Combobox(frame_top_right, values=themes)  # Then create combobox

        column_ids = ['FSPName', 'CurrentBDE','NewBDE','ChangeDate']
        self.tree = ttk.Treeview(self.form_main, columns=column_ids, show="headings")
        for col in column_ids:
            self.tree.heading(column=col, text=col, anchor="w")  # No comma, anchor is inside the parentheses
        
        #Position controls
        frame_top_left.grid(row=1, column=1)
        button_edit.grid(row=1, column=1)
        #button_delete.grid(row=1, column=2)
        frame_top_right.grid(row=1, column=2,sticky='e')
        self.combo_theme.grid(row=1,column=1)

        self.tree.grid(row=2, column=2)  # Also changed column to 1 so it aligns with the frame

        

form = FormMain()