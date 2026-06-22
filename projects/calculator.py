import tkinter as tk
reset_display = False

def click(event):
    global reset_display
    
    
    current = entry.get()
    button_text = event.widget["text"]
    
    if button_text =='C':
        entry.delete(0,tk.END)
        entry.insert(tk.END,'0')
        reset_display = False
        
    elif button_text == '=':
        try:
            expression = current.replace('%','/100')
            result = eval(expression)
            entry.delete (0,tk.END)
            entry.insert (tk.END, str(result))
            reset_display = True
            return
        except Exception:
            entry.delete (0,tk.END)
            entry.insert (tk.END,"error!")
            return
            reset_display = True
            
    else:
        if reset_display:
            entry.delete(0,tk.END)
            current =""
            reset_display = False
            
            
        if current == '0':
            current= ""
            
        # Avoid 2 consecutive operators
        operators = "+-/*%"

        if current and current[-1] in operators and button_text in operators:
            current = current[:-1]
        
        
        #avoid starting an expression with certain operators 
        if current == "" and button_text in "*/%":
            return
        
        #finally update the entry widget
        entry .delete(0,tk.END)   
        entry.insert(tk.END, current+ button_text)
        

root = tk.Tk()     #main window
print("window started")
root.title("Simple calculator")
root.geometry("300x400")
root.resizable(False,False)
root.configure(bg="#F0F0F0")

#Entry widget
entry = tk.Entry(root, bd=6 ,font=('Arial',20), justify='right',width=17 , bg="#aeede4")
entry.pack(pady=6)


#button frame
btnframe = tk.Frame(root)
btnframe.pack(padx=9,pady= 9)

#calculator button
buttons = [['C', '(', ')', '/'],
           ['7', '8', '9', '*'],
           ['4', '5', '6', '-'],
           ['1', '2', '3', '+'],
           ['.', '0', '%', '=']]

for i in range(len(buttons)):
    for j in range(len(buttons[i])):
        btn = tk.Button(btnframe, text=buttons[i][j], 
                         font= ("Arial",16), width=2, height=1)

        btn.grid(row=i, column= j, padx=9, pady=9)
        btn.bind('<Button-1>', click)
        
        
        
        
        
root.mainloop()
