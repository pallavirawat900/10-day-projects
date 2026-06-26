import tkinter as tk
from tkinter import messagebox
import qrcode
from PIL import Image,ImageTk       #import image for image processing and imagetk for displaying images in tkinter

def generate_qr():
    global qr_label
    filename = file_Entry.get().strip()
    data = data_Entry.get().strip()
    
    if not filename and not data:
        messagebox.showerror("Error","Filename and data must required")
        return
    
    qr_img = qrcode.make(data)      #generate qr code from data
    qr_img.save(f"{ filename}.png")
    
    img = qr_img.resize((180,180))
    img_tk = ImageTk.PhotoImage(img)        #convert image for tkinter display
    
    qr_label.config(image = img_tk, text ="")
    qr_label.image = img_tk         #keep image refrence
    
    messagebox.showinfo("success",f"Your qr code has been saved as{filename}.png")
    
root = tk.Tk()
root.title("Qr-code Generator")
root.geometry("600x540")
root.configure(bg="white")

title_label = tk.Label(
    root,
    text = "QR-Code Generator",
    font = ('Helvetice',26,"bold"),
    bg = 'white',
    fg ="black"  
)
title_label.pack(pady=20)

input_frame =tk.Frame(root,bg='white')
input_frame.pack(pady=10)

tk.Label(input_frame,
    text = "Filename:",
    font = ("Helvetice",14),
    bg = "white"
).grid(row=0,column=10,padx=0,pady=10,sticky="e")

file_Entry = tk.Entry(
    input_frame,
    font =("Helvetica",14),
    width=25
)
file_Entry.grid(row=0,column=1)

tk.Label(input_frame,
    text = "Qr-data:",
    font = ("Helvetice",14),
    bg = "white"
).grid(row=1,column=10,padx=0,pady=10,sticky="e")

data_Entry = tk.Entry(
    input_frame,
    font =("Helvetica",14),
    width=25
)
data_Entry.grid(row=1,column=1)

generate_btn = tk.Button(
    root,text="Generate",font=("Helvetica",22),
        fg="green",activebackground="#0FA00C",
        activeforeground="white",width=20,command = generate_qr)
generate_btn.pack(pady=20)

qr_frame =tk.Frame(
    root,bg='white',width=260, height =200
)
qr_frame.pack(pady=10)
qr_frame.pack_propagate(False)

qr_label =tk.Label(
    qr_frame,text ="QR-CODE WILL APPEAR HERE",
    font =("HElvetica",12),
    bg="white",
    fg='black')
qr_label.pack(expand=True)

root.mainloop()