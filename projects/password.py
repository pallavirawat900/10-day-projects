import tkinter as tk    #it use to create GUI
from tkinter import ttk ,messagebox
import random
import string       # help to generate password
import json         # handle saving and loading the password
import base64       #use simple encrption and decryption

print("program start")
class passwordmanager:                        #main class
    def __init__(self,master):                #application initialize karne ke liye
        print("init called")                  #check karne ke liye ki constructor run hua  ki nhi
        self.master = master                  #store window reference 
        self.master.title("Password Generator and Manager")
        self.master.geometry("400x500")
        self.master.configure(bg = "#0B0208")
        
        self.notebook =ttk.Notebook(self.master)                #tab container create karne ke liye
        self.notebook.pack(expand= True, fill="both", padx=5 ,pady=5)      #notebook ko window mai display karne ke liye
        
        self.generator_frame = ttk.Frame(self.notebook)              #password generator tab frame
        self.manager_frame = ttk.Frame(self.notebook)                #password manager tab frame
        
        self.notebook.add(self.generator_frame , text = "Generator") #add generator frame
        self.notebook.add(self.manager_frame , text = "Manager")     #add manager frame
        
        self.setup_generator()              #generator tab ka ui banane wala function
        self.setup_manager()
        self.load_password()                #phale sesave password ko load karega
        
    def setup_generator(self):
        self.length_var = tk.StringVar(value="12")          #default password length
        self.uppercase_var = tk.BooleanVar(value=True)      #defalut uppcase value on
        self.lowercase_var = tk.BooleanVar(value=True)
        self.numbers_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=False)       #default value off
        self.password_var = tk.StringVar()             #store generate password
            
        ttk.Label(self.generator_frame, text="Password Length:").pack(pady=5)       #length label display
        ttk.Entry(self.generator_frame, textvariable=self.length_var, width=5).pack()      #length input box    
        ttk.Checkbutton(self.generator_frame, text="Uppercase", variable= self.uppercase_var).pack()
        ttk.Checkbutton(self.generator_frame, text="Lowercase", variable =self.lowercase_var).pack()
        ttk.Checkbutton(self.generator_frame, text="Numbers", variable =self.numbers_var).pack()
        ttk.Checkbutton(self.generator_frame, text="Symbols", variable =self.symbols_var).pack()
            
        tk.Button(self.generator_frame, text="Generate Password",command=self.generate_password, bg="green",fg="green").pack(pady=10)  #password generate karne ke liye button
        ttk.Entry(self.generator_frame, textvariable=self.password_var, state="readonly",width=30).pack()      #display generate password
        ttk.Button(self.generator_frame, text="Copy to Clipboard", command= self.copy_to_clipboard_clear).pack(pady=10) #password copy karne ke liye
            
    def setup_manager(self):
        self.service_var = tk.StringVar()       #service name store karne ke liye
        self.username_var = tk.StringVar()
        self.password_man_var = tk.StringVar()
                
        tk.Label(self.manager_frame, text="service:").pack(pady=5)      #sevice text display karega
        ttk.Entry(self.manager_frame, textvariable=self.service_var, width=30).pack()   #service input box   
                
        ttk.Label(self.manager_frame, text="Username:").pack(pady=5)   
        ttk.Entry(self.manager_frame, textvariable=self.username_var, width=30).pack()
                
        ttk.Label(self.manager_frame, text="Password;").pack(pady=5) 
        ttk.Entry(self.manager_frame, textvariable=self.password_man_var, width=30, show="*").pack()  
                
        ttk.Button(self.manager_frame, text='Save Password', command=self.save_password).pack(pady=10)

        self.password_tree = ttk.Treeview(self.manager_frame, columns=("Service", "Username"),show="headings")  #create password table
        self.password_tree.heading("Service", text="Service")
        self.password_tree.heading("Username",text="Username")
        self.password_tree.pack(pady=10)
        self.password_tree.bind("<Double-1>", self.on_tree_double_click)    #double click per password show hoga
            
    def generate_password(self):
                
        length = int(self.length_var.get())     #get password length
        characters=" "  #initialize character pool
        if self.uppercase_var.get():        #check uppercase option
            characters +=string.ascii_uppercase
        if self.lowercase_var.get():
            characters +=string.ascii_lowercase
        if self.numbers_var.get():
            characters +=string.digits
        if self.symbols_var.get():
            characters +=string.punctuation
                
        if not characters:
            self.password_var.set("Please select at least one characters type")
        else:
            password = ''.join(random.choice(characters) for _ in range(length))    #create random password
            self.password_var.set(password)
                    
    def copy_to_clipboard_clear(self):
                
        self.master.clipboard_clear()           #phale jo clip board per data h usko clear kar dega
        self.master.clipboard_append(self.password_var.get())
        self.master.update()
                
    def save_password(self):
        service = self.service_var.get()
        username = self.username_var.get()
        password = self.password_var.get()
                
        if service and username and password:
            encrypted_password = self.encrypt(password)        #password ko direct save nhi karna(encrypt password)
            self.passwords[service] = {"username": username, "password": encrypted_password}    #service ke name se data save hoga
            
            self.update_password_tree()     #update password table
            messagebox.showinfo("success", "all fields are required")
            self.service_var.set("")        #clear sevice box
            self.username_var.set("")
            self.password_var.set("")
        else:
            messagebox.showerror("Error","all fields are required")
                
    def load_password(self):        #load save password
        try:        
            with open("passwords.json","r") as f:   #open json file 
                self.password = json.load(f)      #read file and load password
                        
        except FileNotFoundError:
            self.passwords ={}      #create empty dictionary
        self.update_password_tree()     #refresh password table
                
    def update_password_tree(self):
        for item in self.password_tree.get_children():      #get all rows in table
            self.password_tree.delete(item)         #clear old row
        for service, data in self.passwords.items():        #saved password ko ak ak se check karo
            self.password_tree.insert("","end",values = (service, data["username"]))    #add row in table
                    
    def on_tree_double_click(self,event):           #handle double click
        item = self.password_tree.selection()[0]    #get selected row
        service = self.password_tree.item(item, "values")[0]    #get selected service name
        username = self.passwords[service]["username"]
        encrypted_password = self.passwords[service]["password"]
        password = self.decrypt(encrypted_password)         #decrypt passsword
        messagebox.showinfo("password", f"service: {service}\nUsername: {username}\n password:{password}")  #show password detail     
                
    def encrypt (self, password):       #password ko encoding form mai print kata h(encrypt password)
        return base64.b64encode(password.encode()).decode()         #convert stribg into bytes(return encrypted password)
            
    def decrypt (self, encrypted_password):         #decrypt password
        return base64.b64decode(encrypted_password.encode()).decode()           #decrypted password
                    
                        
if __name__ == "__main__" :
    root = tk.Tk()
    app = passwordmanager(root)
    root.mainloop()          
                    