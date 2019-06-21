import tkinter
import tkinter.messagebox
from tkinter import Frame, Label, Entry, Listbox, IntVar, Radiobutton, W,LEFT

from user.users import User
from view.voting import VotePage
from view.register import RegisterPage

class LoginPage(Frame):
    def __init__(self, master, blockchain=None, client=None):
        Frame.__init__(self, master)
        self.master = master
        self.blockchain = blockchain
        self.client = client
        self.user = None
        print('public key :' + str(self.client.public_key))
        # user id
        id_frame = Frame(self)
        id_frame.pack()
        id_label = Label(id_frame, text ='User ID')
        id_label.pack(side = LEFT)
        self.id_entry = Entry(id_frame, bd=5)
        self.id_entry.pack(side = LEFT)
        
        # year
        year_frame = Frame(self)
        year_frame.pack()
        self.year_var = IntVar()

        years = [('2007',2007),('2008',2008),('2009',2009),('2010',2010),('2011',2011)]
        for text, value in years:
            rb = Radiobutton(year_frame, text=text, variable=self.year_var, value=value, command = self.sel)
            rb.pack(anchor=W)

        self.label = Label(year_frame)
        self.label.pack()

        # password
        password_frame = Frame(self)
        password_frame.pack()
        password_label = Label(password_frame, text ='Password')
        password_label.pack(side = LEFT)
        self.password_entry = Entry(password_frame, bd=5)
        self.password_entry.pack(side = LEFT)
        
        # login button
        w = tkinter.Button(self, bg='Green', text='Login',command = self.login)
        w.pack() 

        # back to register button
        r = tkinter.Button(self, bg='blue', text='Register',
                        command = lambda: master.switch_frame(RegisterPage, self.blockchain, self.client))
        r.pack(side = LEFT) 

    def sel(self):
        selection = 'You selected the year '+str(self.year_var.get())
        self.label.config(text = selection)

    def login(self):
        self.user = User()
        id_ = self.id_entry.get()
        year = int(self.year_var.get())
        print(year)
        print(type(year))
        print('public key :' + str(self.client.public_key))
        password = self.password_entry.get()
        if self.user.login_student(id_, year, password):
            tkinter.messagebox.showinfo('Login', 'you are login.')
            """Destroys current frame and replaces it with a new one."""
            self.master.switch_frame(VotePage, self.blockchain, self.client, self.user)            
        else:
            tkinter.messagebox.showerror('Error', 'Login failed.')
    def to_register_page(self):
        """Destroys current frame and replaces it with a new one."""
        self.master.switch_frame(RegisterPage, self.blockchain, self.client)