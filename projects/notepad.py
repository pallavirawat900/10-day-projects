import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog,colorchooser
import tkinter.font as tkfont

root = tk.Tk()
root.geometry('600x600')
root.title("NOTEPAD")
root.configure(bg="#EFDAF0")

title_label = ctk.CTkLabel(root,text="NOTEPAD",font=("arial",18,"bold")
    ,text_color="#021828")
title_label.pack(pady=10,padx=10)

input_frame =tk.Frame(root,bg="white",padx=10,pady=10,bd=2)
input_frame.pack(padx=15,pady=15,fill="both")

note_label =  ctk.CTkLabel(input_frame,text="NOTE: MENU BAR IN THE TOP OF THE SCREEN (Mac style)",
    font=("bold",20),text_color="#100F0F")
note_label.pack(side="left",anchor="w",padx=10)

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)


text_area = tk.Text(root,font=("arial",23),wrap="word",undo=True)
scroll_bar =tk.Scrollbar(root)
scroll_bar.config(command=text_area.yview)
text_area.config(yscrollcommand=scroll_bar.set)


def new_file():
    text_area.delete("1.0",tk.END)
    
def open_file():      # Create a function to open a text file  
    file_path = filedialog.askopenfilename(filetypes=[("Text Files","*.txt"),
        ("All Files","*.*")])       # Show only .txt files by default
    if file_path:
        with open (file_path,"r") as file:      # Open the selected file in read mode
            content = file.read()
        text_area.delete("1.0",tk.END)
        text_area.insert(tk.END,content)
        
def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
        filetypes=[("Text Files","*.txt"),("All Files","*.*")])   
    
    if file_path:
        with open(file_path,"w") as file:
            content = text_area.get("1.0",tk.END)
            file.write(content)
            

file_menu = tk.Menu(menu_bar,tearoff=0)
menu_bar.add_cascade(label="File",menu=file_menu)
file_menu.add_command(label="New",command=new_file)
file_menu.add_command(label="Open",command=open_file)
file_menu.add_command(label="Save",command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit",command=root.quit)

def undo_text():
    try:
        text_area.edit_undo()
    except tk.TclError:
        pass
    

def copy_text():
    text_area.event_generate("<<Copy>>")
    
def cut_text():
    text_area.event_generate("<<Cut>>") 
    
def paste_text():
    text_area.event_generate("<<Paste>>") 
    
      

edit_menu = tk.Menu(menu_bar,tearoff=0)
menu_bar.add_cascade(label="Edit",menu=edit_menu)
edit_menu.add_command(label="Undo",command=undo_text)
edit_menu.add_command(label="Copy",command=copy_text)
edit_menu.add_command(label="Cut",command=cut_text)
edit_menu.add_command(label="Paste",command=paste_text)

def change_font():
    new_font = tkfont.Font(family="Arial",size=25)
    text_area.configure(font = new_font)
def word_wrap():
    text_area.config(wrap="word")
    
current_color = "black"    
def text_color():
    global current_color
    color = colorchooser.askcolor()[1]
    
    if color:
        current_color = color
        
def type_color(event):
    global current_color
    
    text_area.tag_config(current_color,foreground=current_color)  
    text_area.insert("insert",event.char,current_color)   
    return "break"   

text_area.bind("<Key>", type_color)

format_menu = tk.Menu(menu_bar,tearoff=0)
menu_bar.add_cascade(label="Format",menu=format_menu)
format_menu.add_command(label="Font",command=change_font)
format_menu.add_command(label="Word Wrap",command=word_wrap)
format_menu.add_command(label="Text Color",command=text_color)


status_frame = tk.Frame(root,bg="#E5E5E5",height =30)
status_frame.pack(fill="x",side="bottom")

word_label = tk.Label(status_frame,text="words: 0")
word_label.pack(side="left",padx=10)

line_label = tk.Label(status_frame,text="Lines: 1")
line_label.pack(side="left",padx=10)

char_label = tk.Label(status_frame, text="characters: 0")
char_label.pack(side="right",padx=10)

def update_state(event=None):
    text = text_area.get("1.0","end-1c")
    
    words = len(text.split())
    lines = int(text_area.index("insert").split(".")[0])
    chars = len(text)
    
    word_label.config(text=f"Words:{words}")
    line_label.config(text=f"Lines:{lines}")
    char_label.config(text=f"Charachters:{chars}")
    
text_area.bind("<KeyRelease>",update_state)


scroll_bar.pack(side="right",fill="y")
text_area.pack(fill="both",expand=True,padx=15,pady=15)



def backspace(event):
    text_area.delete("insert-1c")
    return "break"

text_area.bind("<BackSpace>",backspace)

try:
    with open("history.text","r") as file:
        text_area.insert("1.0",file.read())
except FileNotFoundError:
    pass
        

def save_history():
    with open("history.text","w") as file:
        file.write(text_area.get("1.0",tk.END))             

def on_close():
    save_history()
    root.destroy()
root.protocol("WM_DELETE_WINDOW",on_close)
root.mainloop()
