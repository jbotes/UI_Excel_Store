# based on some ideas from https://www.youtube.com/watch?v=ibXT3SbfkOc&list=WL&index=59

import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as tb
import Data_layer 

class FormMain:

    def __init__(self):
        self.data_manager = Data_layer.DataLayer()
        self.build_controls()
        self.refresh_tree()
        self.form_main.mainloop()

    def refresh_tree(self):
        self.tree.delete(*self.tree.get_children())
        for record in self.data_manager.get_FSP_data():
            self.tree.insert("", tk.END, values=record)
        #for record in [["FSP1", "James", "Werner","28 Feb 2025"],["FSP2", "James", "werner","29 feb 2025"]]:
        #    self.tree.insert("",tk.END,values=record)

    
    def delete_click(self):
        #print("delete")
        self.delete_record()
        self.refresh_tree()
    
    def delete_record(self):
        selection = self.tree.focus()
        if not selection:
            messagebox.showerror(message="No item was selected for deletion try again by selecting an item.")
        row_index = self.tree.index(selection) + 1# we will give this to our data layer
        print(row_index)
        self.data_manager.delete_FSP_record(row_index=row_index)
    
    def edit_click(self):
        print('edit')
        self.refresh_tree()

    def save_click(self):
        print('save or add')
        self.refresh_tree()

    def build_controls(self):
        self.form_main = tb.Window(themename="superhero") #tk.Tk()
        self.style = tb.Style()
        self.form_main.title("BDE FSP Allocations Form")
        
        #create the controls
        frame_top_left = tk.Frame(self.form_main, relief="solid", borderwidth=2)
        button_edit = tk.Button(frame_top_left, text='Edit', width=10, command=self.edit_click)
        button_delete = tk.Button(frame_top_left, text='Delete', width=10, command=self.delete_click)

        #button_delete = tk.Button(frame_top_left, text='Delete', width=10)
        themes = ['cosmo','flatly', 'sandstone']

        frame_top_right = tk.Frame(self.form_main)  # Create frame first
        self.combo_theme = ttk.Combobox(frame_top_right, values=themes)  # Then create combobox

        #column_ids = ['FSPName', 'CurrentBDE','NewBDE','ChangeDate']
        headings = self.data_manager.get_header()
        self.tree = ttk.Treeview(self.form_main, columns=headings, show="headings")
        for col in headings:
            self.tree.heading(column=col, text=col, anchor="w")  # No comma, anchor is inside the parentheses
        
        # Data Controls
        frame_centre_left = tk.Frame(self.form_main, relief="solid", borderwidth=1)
        self.label_heading = tk.Label(frame_centre_left, text="FSP BDE Alloaction Details")
        self.label_FSP_Name = tk.Label(frame_centre_left, text="FSP Names")
        self.entry_FSP_Name = tk.Entry(frame_centre_left)
        self.label_Current_BDE = tk.Label(frame_centre_left, text="Current BDE")
        self.entry_Current_BDE = tk.Entry(frame_centre_left)
        # self.entry_FSP_Name = tk.Entry(frame_centre_left)
        self.label_ChangeDate = tk.Label(frame_centre_left, text="Change BDE Date")
        self.entry_BDE_ChangeDate = tk.Entry(frame_centre_left)
        self.button_add = tb.Button(frame_centre_left, text="Add", command=self.save_click, width=10, bootstyle="light")

        #Position controls
        frame_top_left.grid(row=1, column=1)

        button_edit.grid(row=1, column=1)
        button_delete.grid(row=1, column=2)

        #button_delete.grid(row=1, column=2)
        frame_top_right.grid(row=1, column=2,sticky='e')
        self.combo_theme.grid(row=1,column=1)

        self.tree.grid(row=2, column=2)  # Also changed column to 1 so it aligns with the frame

        frame_centre_left.grid(row=2,column=1)
        self.label_heading.grid(row=2, column=1)
        self.label_FSP_Name.grid(row=3,column=1)
        self.entry_FSP_Name.grid(row=3,column=2)
        self.label_Current_BDE.grid(row=4,column=1)
        self.entry_Current_BDE.grid(row=4,column=2)
        self.label_ChangeDate.grid(row=5,column=1)
        self.entry_BDE_ChangeDate.grid(row=5,column=2)
        self.button_add.grid(row=7, column=1)

        

form = FormMain()