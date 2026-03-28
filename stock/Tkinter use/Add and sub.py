import tkinter as tk
root = tk.Tk()
root.title("Share trading app")
root.geometry("300x200")
tk.Label(root,text="Result show ").pack()

entry1 = tk.Entry(root)
entry1.pack()
entry2 = tk.Entry(root)
entry2.pack()

entry1.bind("<Return>", lambda event: entry2.focus())

label = tk.Label(root,text="")
label.pack()
def add():
    num1 = int(entry1.get())
    num2 = int(entry2.get())
    result = num1+num2    
    label.config(text = result)
def sub():
    num1 = int(entry1.get())
    num2 = int(entry2.get())
    result = num1-num2
    label.config(text=result)
frame = tk.Frame(root)
frame.pack()    
tk.Button(frame,text="Sub",command=sub).pack(side="left")
tk.Button(frame,text="add",command=add).pack(side="right")
root.mainloop()