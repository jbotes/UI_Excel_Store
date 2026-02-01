import tkinter as tk
from tkinter import ttk,messagebox
import ttkbootstrap as tb
import data_layer

class FormMain:

    def __init__(self):
        self.data_manager = data_layer.DataLayer()
        self.build_controls()
        self.refresh_tree()
        self.set_mode("add")
        self.form_main.mainloop()

    # Events
    def delete_click(self):
        self.delete_record()
        self.refresh_tree()

    def edit_click(self):
        self.set_mode("edit")
        self.edit_record()
        self.refresh_tree()

    def save_click(self):
        self.save_record()
        self.empty_controls()
        self.refresh_tree()

    def save_record(self):
        try:        
            if self.mode == "add":
                self.data_manager.add_record(self.get_data_from_controls())
                messagebox.showinfo(message="Record added")
            else:
                self.data_manager.update_record(self.get_data_from_controls())
                messagebox.showinfo(message="Record updated")
                self.set_mode("add")
        except RuntimeError as e:
            messagebox.showerror(message=str(e))




    def delete_record(self):
        selection = self.tree.focus()
        if not selection:
            messagebox.showerror("No selection","No item selected. Please select and try again")
            return
        
        row_index = self.tree.index(selection)
        self.data_manager.delete_record(row_index+1)
        
    def edit_record(self):
        selection = self.tree.focus()
        if not selection:
            messagebox.showerror("No selection","No item selected. Please select and try again")
            return
        self.empty_controls()
        self.fill_controls_from_tree(self.tree.item(selection,'values'))


        
    def get_data_from_controls(self):
        return [self.entry_first_name.get(),
                self.entry_last_name.get(),
                self.radio_job_status.get(),
                self.combo_departments.get()]

    def fill_controls_from_tree(self,record):
        self.entry_first_name.insert(0,record[0]) 
        self.entry_last_name.insert(0,record[1]) 
        self.radio_job_status.set(record[2]) 
        self.combo_departments.set(record[3]) 

    def theme_selected(self,event):
        self.style.theme_use(self.combo_theme.get())

    def set_mode(self,mode):
        self.mode = mode
        self.button_add.config(text="Update" if mode=="edit" else "Insert")


    def refresh_tree(self):
        self.tree.delete(*self.tree.get_children())
        for record in self.data_manager.get_data():
            self.tree.insert("",tk.END,values=record)

    def empty_controls(self):
        self.entry_first_name.delete(0,tk.END) 
        self.entry_last_name.delete(0,tk.END) 
        self.radio_job_status.set("Full-time") 
        self.combo_departments.set("")         

    def update_controls(self,parent):
        padx_button = 5
        pady_button = 5
        padx_control = 15
        pady_control = 15
        for child in self.walk_widgets(parent):
            if isinstance(child,(tk.Frame,ttk.Treeview)):
                child.grid_configure(padx=padx_control,pady=pady_control,sticky="nw")
            else:
                child.grid_configure(padx=padx_button,pady=pady_button,sticky="w")

    def walk_widgets(self,parent):
        widgets = []
        for child in parent.winfo_children():
            widgets.append(child)
            widgets.extend(self.walk_widgets(child))
        return widgets

    def build_controls(self):
        self.form_main = tb.Window(themename="superhero")
        self.style = tb.Style()
        self.form_main.title("Staff manager")

        frame_top_left = tk.Frame(self.form_main)
        button_edit = tk.Button(frame_top_left,text="Edit",width=10,command=self.edit_click)
        button_delete = tk.Button(frame_top_left,text="Delete",width=10,command=self.delete_click)

        themes = ["cosmo", "flatly", "sandstone",  "pulse", "united", "journal", "darkly","superhero"]
        frame_top_right  = tk.Frame(self.form_main)
        self.combo_theme = ttk.Combobox(frame_top_right,values=themes)
        self.combo_theme.set(self.style.theme.name)
        self.combo_theme.bind("<<ComboboxSelected>>",self.theme_selected)

        headings = self.data_manager.get_header()
        self.tree = ttk.Treeview(self.form_main,columns=headings,show="headings")
        for text in headings:
            self.tree.heading(column=text,text=text,anchor="w")

        # data controls
        frame_centre_left = tk.Frame(self.form_main,relief="solid",borderwidth=1)
        self.label_first_name = tk.Label(frame_centre_left,text="First name")
        self.entry_first_name = tk.Entry(frame_centre_left)
        self.label_last_name = tk.Label(frame_centre_left,text="Last name")
        self.entry_last_name = tk.Entry(frame_centre_left)    
        label_job_status = tk.Label(frame_centre_left,text="Job status")

        self.combo_departments = ttk.Combobox(frame_centre_left)     
        self.combo_departments.configure(values=self.data_manager.get_departments())  

        frame_job_status = tk.Frame(frame_centre_left)
        self.radio_job_status = tk.StringVar(value="Full-time") 
        radio_fulltime = tk.Radiobutton(frame_job_status,text="Full-time",value="Full-time",variable=self.radio_job_status)
        radio_parttime = tk.Radiobutton(frame_job_status,text="Part-time",value="Part-time",variable=self.radio_job_status)
        label_department = tk.Label(frame_centre_left,text="Department")

        self.button_add = tb.Button(frame_centre_left,text="Add",command=self.save_click,width=10,bootstyle="light") 

        # Position
        frame_top_left.grid(row=1,column=1)
        button_edit.grid(row=1,column=1)
        button_delete.grid(row=1,column=2)

        frame_top_right.grid(row=1,column=2)
        self.combo_theme.grid(row=1,column=1)

        self.tree.grid(row=2,column=2)

        frame_centre_left.grid(row=2,column=1)
        self.label_first_name.grid(row=2,column=1)
        self.entry_first_name.grid(row=2,column=2)
        self.label_last_name.grid(row=3,column=1)
        self.entry_last_name.grid(row=3,column=2)
        
        label_department.grid(row=6,column=1)
        self.combo_departments.grid(row=6,column=2)

        label_job_status.grid(row=7,column=1)
        frame_job_status.grid(row=7,column=2)
        radio_fulltime.grid(row=1,column=1)
        radio_parttime.grid(row=1,column=2)
        self.button_add.grid(row=8,column=1)

        self.update_controls(self.form_main)
        frame_top_right.grid_configure(row=1,column=2,sticky="e")

form = FormMain()