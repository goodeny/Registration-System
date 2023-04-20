from system import System
from tkinter import *
from tkinter import ttk
import threading
import json
import os
from datetime import datetime

class App:
    def __init__(self):
        self.window = Tk()
        self.center_screen(800,500)
        self.window.resizable(0,0)
        self.window.title("Software")
        #label to inputs and labels
        self.label_inputs = Label(self.window)
        self.label_inputs.grid(row=0, column=1)
        self.label_name = Label(self.label_inputs,text="Name")
        self.label_name.grid(row=0, column=0, pady=10)

        self.entry_name = Entry(self.label_inputs, width=50)
        self.entry_name.grid(row=0, column=1, pady=10)

        self.label_second_name = Label(self.label_inputs,text="Second Name")
        self.label_second_name.grid(row=1, column=0, pady=10)

        self.entry_second_name = Entry(self.label_inputs, width=50)
        self.entry_second_name.grid(row=1, column=1, pady=10)

        #label buttons
        self.label_buttons = Label(self.window)
        self.label_buttons.grid(row=2, column=1)

        self.button_name = Button(self.label_buttons, text="Add",width=10, height=2, command=lambda: threading.Thread(target=self.add_user()).start())
        self.button_name.grid(row=2, column=0, padx=10,pady=30)

        self.button_delete = Button(self.label_buttons, text="Delete",width=10, height=2, command=lambda: threading.Thread(target=self.delete_user()).start())
        self.button_delete.grid(row=2, column=1,padx=10,pady=30)

        self.button_edit = Button(self.label_buttons, text="Edit",width=10, height=2, command=lambda: threading.Thread(self.edit_user()))
        self.button_edit.grid(row=2, column=2,padx=10,pady=30)

        self.tree = ttk.Treeview(self.window, columns=("ID","Name","Second Name"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Second Name", text="Second Name")
        self.tree.column("ID", width=200)
        self.tree.column("Name", width=200)
        self.tree.column("Second Name", width=200)
        self.tree.grid(row=3, column=1, padx=90, pady=10)

        self.button_logs = Button(self.window, text="Open logs", command=lambda: threading.Thread(target=self.open_logs()).start())
        self.button_logs.grid(row=4, column=1, pady=10)

        self.update_list()

        self.window.mainloop()

    def center_screen(self, w, h):
        width = w
        height = h

        s_w = self.window.winfo_screenwidth()
        s_h = self.window.winfo_screenheight()

        x = (s_w - width)//2
        y = (s_h - height)//2
        return self.window.geometry(f"{width}x{height}+{x}+{y}")

    def add_user(self):
        c_time = self.current_time()
        s = System()
        name = self.entry_name.get()
        second_name = self.entry_second_name.get()
        print(name)
        print(second_name)
        s.insert(0, name, second_name)
        self.update_list()
        with open("logs/logs.txt", "a") as f:
            f.writelines(f"[{c_time}] User was add: Name: {name} Second_name: {second_name}\n")
        f.close()

    def update_list(self):
        c_time = self.current_time()
        self.tree.delete(*self.tree.get_children())
        s = System()
        data = s.get_all_users()
        for i in data:
            self.tree.insert("", "end", values=(i[0], i[1], i[2]))
            print(f"id: {i[0]} Name: {i[1]} Second name: {i[2]} ")
        with open("logs/logs.txt", "a") as f:
            f.writelines(f"[{c_time}] List was updated successfuly!\n")
        f.close()

    def delete_user(self):
        c_time = self.current_time()
        s = System()
        data = s.get_all_users()
        selected_items = self.tree.selection()
        for i in selected_items:
            item = self.tree.item(i, "values")
            for j in data:
                if int(item[0]) == j[0]:
                    s.delete_user(j[0])
                    with open("logs/logs.txt", "a") as f:
                        f.writelines(f"[{c_time}] User: {j} was deleted successfuly!\n")
                    f.close()
        self.update_list()
        

    def edit_user(self):
        c_time = self.current_time()
        s = System()
        l = s.load()
        name = self.entry_name.get()
        second_name = self.entry_second_name.get()
        selected_items = self.tree.selection()
        for i in selected_items:
            item = self.tree.item(i, "values")
            for j in l['data']:
                if int(item[0]) == j[0]:
                    j[1] = name
                    j[2] = second_name
                    with open("data.json", "w") as f:
                        json.dump(l, f)
                    print(f"{item} was edit to {j}")
                    with open("logs/logs.txt", "a") as f:
                        f.writelines(f"[{c_time}] User: ID: {item[0]} Name: {item[1]} Second name: {j[1]} was edited to Name: Second name: {j[2]}!\n")
                    f.close()
        self.update_list()

    def open_logs(self):
        c_time = self.current_time()
        os.system("start logs/logs.txt")
        print(os.listdir())
        with open("logs/logs.txt", "a") as f:
            f.writelines(f"[{c_time}] Logs was opened!\n")
        f.close()

        
    def current_time(self):
        now = datetime.now()
        return now.strftime("%H:%M:%S")

if __name__ == "__main__":
    try:
        os.mkdir("logs")
        os.system("cd logs")

        with open("logs/logs.txt", "x") as f:
            pass
        f.close()

        os.system("cd..")

        with open("data.json", "x") as j:
            pass
        j.close()

        with open("data.json", "w")as y:
            y.write('{"data": []}')
        y.close()

    except:
        pass
    try:
        App()
    except:
        with open("data.json", "w")as y:
            y.write('{"data": []}')
        y.close()


