import tkinter
import tkinter.messagebox
from tkinter import Frame, Label, Entry, Listbox, IntVar, Radiobutton, W,LEFT, Listbox, SINGLE, Spinbox

from user.users import User
from user.student import Student

class RegisterPage(Frame):
    def __init__(self, master, blockchain = None, client = None):
        Frame.__init__(self, master)

        self.blockchain = blockchain
        self.client = client

        # user id
        id_frame = Frame(self)
        id_frame.pack()
        id_label = Label(id_frame, text ='User ID')
        id_label.pack(side = LEFT)
        self.id_entry = Entry(id_frame, bd=5)
        self.id_entry.pack(side = LEFT)

        #first name
        fname_frame = Frame(self)
        fname_frame.pack()
        fname_label = Label(fname_frame, text ='First Name')
        fname_label.pack(side = LEFT)
        self.fname_entry = Entry(fname_frame, bd=5)
        self.fname_entry.pack(side = LEFT)

        #last name
        lname_frame = Frame(self)
        lname_frame.pack()
        lname_label = Label(lname_frame, text ='Last Name')
        lname_label.pack(side = LEFT)
        self.lname_entry = Entry(lname_frame, bd=5)
        self.lname_entry.pack(side = LEFT)

        # department
        departments = [(1,'cse'),(2,'arch')]
        department_frame = Frame(self)
        department_frame.pack()
        department_label = Label(department_frame, text='Department')
        department_label.pack(side=LEFT)
        self.department_list = Listbox(department_frame, selectmode=SINGLE, selectbackground='Blue',height=len(departments))

        for index, dep in departments:
            self.department_list.insert(index, dep)
        self.department_list.pack(side=LEFT)

        #section
        section_frame = Frame(self)
        section_frame.pack()
        section_label = Label(section_frame, text='section')
        section_label.pack(side=LEFT)
        self.section_spinbox = Spinbox(section_frame, from_=1, to=3)
        self.section_spinbox.pack(side=LEFT)

        # Year
        year_frame = Frame(self)
        year_frame.pack()
        year_label = Label(year_frame, text='Year')
        year_label.pack()
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

        #Re-password
        repassword_frame = Frame(self)
        repassword_frame.pack()
        repassword_label = Label(repassword_frame, text ='Re-password')
        repassword_label.pack(side = LEFT)
        self.repassword_entry = Entry(repassword_frame, bd=5)
        self.repassword_entry.pack(side = LEFT)

         #register button
        w = tkinter.Button(self, bg='Green', text='Register',command = self.register)
        w.pack()



    def sel(self):
        selection = 'You selected the year '+str(self.year_var.get())
        self.label.config(text = selection)

    def register(self):
        user = User()
        selected = self.department_list.curselection()
        if len(selected) < 1:
            tkinter.messagebox.showerror('Error','Department not selected !!!')
        else:
            department = self.department_list.get(self.department_list.curselection())
            id_ = self.id_entry.get()
            fname = self.fname_entry.get()
            lname = self.lname_entry.get()
            
            print(str(department))
            section = int(self.section_spinbox.get())
            print(section)
            print(type(section))
            year = int(self.year_var.get())
            print(year)
            print(type(year))
            password = self.password_entry.get()
            repassword = self.repassword_entry.get()
            if password == repassword:
                student = Student(fname, lname, department, section, year, id_, password=password)
                if user.student_register(student):
                    tkinter.messagebox.showinfo('Register', 'you are Registerd.')
                else:
                    tkinter.messagebox.showerror('Error', 'Registration failed.')
            else:
                tkinter.messagebox.showerror('Error', 'password is incorrect')