# based on some ideas from https://www.youtube.com/watch?v=ibXT3SbfkOc&list=WL&index=59

import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as tb
import Data_layer 

class FormMain:

    def __init__(self):
        self.data_manager = Data_layer.DataLayer()
        self.edit_item_id = None
        self.build_controls()
        self.refresh_tree()
        self.set_mode("add")
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
        selection = self.tree.selection()
        if not selection:
            messagebox.showerror(message="No item selected")
            return
        self.edit_item_id = selection[0]
        self.set_mode('edit')
        self.edit_record()
        # self.refresh_tree()
    
    def edit_record(self):
        self.empty_controls()
        record = self.tree.item(self.edit_item_id, "values")
        self.fill_controls_from_tree(record)
        #selection = self.tree.selection() #self.tree.focus()
        #if not selection:
        #    messagebox.showerror(message="No item selected. Please select an item")
        #    return
        #item_id = selection[0]
        #self.fill_controls_from_tree(self.tree.item(item_id, 'values'))
    
    def empty_controls(self):
        self.entry_FSP_Name.delete(0,tk.END)
        self.entry_Current_BDE.delete(0,tk.END)
        self.entry_BDE_ChangeDate.delete(0,tk.END)
    
    def fill_controls_from_tree(self, record):
        self.entry_FSP_Name.insert(0,record[0])
        self.entry_Current_BDE.insert(0,record[1])
        self.entry_BDE_ChangeDate.insert(0,record[3])     

    def save_click(self):
        try:
            print('save or add')
            self.save_record()
            self.empty_controls()
            self.set_mode("add")
            self.refresh_tree()
        except RuntimeError as e:
            messagebox.showerror(message=str(e))


    def save_record(self):
        try:
            if self.mode == 'add':
                self.data_manager.add_FSP_record(self.get_data_from_controls())
            else:
                if not self.edit_item_id:
                    messagebox.showerror(message='Edit State Lost')
                    return
                
                row_index = self.tree.index(self.edit_item_id)
                self.data_manager.update_FSP_record_by_index(row_index=row_index,record=self.get_data_from_controls())
                self.edit_item_id = None 

        except RuntimeError as e:
            messagebox.showerror(message=str(e))

    def get_data_from_controls(self):
        return [
            self.entry_FSP_Name.get(),
            self.entry_Current_BDE.get(),
            self.entry_Current_BDE.get(),
            self.entry_BDE_ChangeDate.get()
        ]
    
    def set_mode(self, mode):
        self.mode = mode
        self.button_add.config(text='Update' if mode == 'edit' else 'insert')

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