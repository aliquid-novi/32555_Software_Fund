# GUI application - Login window


import tkinter as tk

root = tk.Tk()
root.geometry("300x300")
root.title("University Application (GUI System)")
root.configure(bg='#113445')
root.resizable(False,False)

selectButton = tk.Button(root,text='Login', bg='#EEEEEE', fg='#000000'
                         , font='Callibri 12 bold')

selectButton.pack(padx=8, pady=8, side='bottom')

root.mainloop()

