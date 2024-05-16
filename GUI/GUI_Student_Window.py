### GUI Student Window

import tkinter as tk

class StudentView(tk.Toplevel):
    def __init__(self, master, info ) -> None:
        super().__init__(master=master)
        self.title('Student Report')
        self.geometry('300x600')
        x = master.winfo_x()
        y = master.winfo_y()
        self.geometry("+%d+%d"%(x+300,y))
        self.configure(bg='#121212')
        self.resizable(False, False)
        label = tk.Label(self, text = info, fg = '#FFFFFF',
                         font='Arial 12 bold', borderwidth=2, relief='solid')
        label.place(relx=0.5,rely=0.5,anchor='center')
        closeButton = tk.Button(self,text='Close',bg='#3C4A82', fg='#FFFFFF',
                                font='Arial 12 bold', borderwidth=2, relief='solid')
        closeButton.pack(oadx=5,pady=20,side='bottom')

        root.mainloop()