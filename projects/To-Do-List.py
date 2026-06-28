import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

root =tk.Tk()
root.title("TO DO LIST",)
root.geometry("500x600")
root.configure(bg="#B9DBF5")

title_label =tk.Label(root,text="📝To-Do-List",font=("Poppins",20,"bold"))
title_label.pack(pady=20)

input_frame = tk.Frame(root,bg="white",padx=10,pady=10,relief="ridge",bd=2)
input_frame.pack(padx=15,pady=15,fill="x")

entry_label = tk.Label(input_frame,text="👇🏼Enter your Tasks")
entry_label.grid(row=0)
entry_label.pack()
task_entry = tk.Entry(input_frame,font="Poppins",width=35)
task_entry.pack(pady=10)

button_frame = tk.Frame(input_frame,bg="white")
button_frame.pack()

task_frame = tk.Frame(root,bg="white",padx=15,pady=15,relief="ridge")
task_frame.pack(fill="both",expand=True,padx=20,pady=20)

task_list = tk.Listbox(task_frame,font=("Arial",20),height=10,highlightthickness=0)
task_list.pack(fill="both",expand=True)

def add_task():
    task = task_entry.get()
    task = "✗"+"   "+task
    if task !="":
        task_list.insert(tk.END,task)
        task_entry.delete(0,tk.END)
add_btn =ctk.CTkButton(button_frame,text="Add",fg_color="#25D918",
    hover_color="#1FAF14",text_color="white",width=80,command=add_task)
add_btn.pack()
add_btn.grid(row=0,column=0,padx=5)

def delete_tasks():
    selected = task_list.curselection()
    if selected:
        task_list.delete(selected[0])
delete_btn = ctk.CTkButton(button_frame,text="Delete",fg_color="#D70606",
    hover_color="#B00000",text_color="white",width=80,command=delete_tasks)
delete_btn.grid(row=0,column=1,padx=5)

def clear_task():
    return task_list.delete(0,tk.END)

clear_btn= ctk.CTkButton(button_frame,text="Clear",fg_color="#EA9E34",
    hover_color="#CC8400",text_color="white",width=80,command=clear_task)
clear_btn.grid(row=0,column=2,padx=5)

def complete_task():
    selected = task_list.curselection()
    if selected:
        task = task_list.get(selected[0])
        task = task.replace("✗","✔︎")

        task_list.delete(selected[0])
        task_list.insert(selected[0],task)
        
complete_btn = ctk.CTkButton(button_frame,text="Complete",fg_color="#5B7AAC",
    text_color="white",command=complete_task)
complete_btn.grid(row=0,column=3,padx=5)

root.mainloop()