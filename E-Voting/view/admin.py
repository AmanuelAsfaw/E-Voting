import tkinter
import tkinter.messagebox
from tkinter import Frame, Label, Entry, Listbox, IntVar, Radiobutton, W,LEFT, Spinbox, SINGLE, Checkbutton

from user.users import User
from user.board import Board
# from view.admin import ConfigPage
from blockchain import Blockchain
from client import Client
from oop import Server
from view.login import LoginPage as LoginPage_

import asyncio
import threading
import socket
import ujson
import aiohttp
import time

class LoginPage(Frame):
    def __init__(self, master, blockchain=None, client=None, user= None):
        Frame.__init__(self, master)
        self.master = master
        self.blockchain = blockchain
        self.client = client
        self.user = user
        # print('public key :' + str(self.client.public_key))
        # user id
        id_frame = Frame(self)
        id_frame.pack()
        id_label = Label(id_frame, text ='User ID')
        id_label.pack(side = LEFT)
        self.id_entry = Entry(id_frame, bd=5)
        self.id_entry.pack(side = LEFT)
        
        # year
        # year_frame = Frame(self)
        # year_frame.pack()
        # self.year_var = IntVar()

        # years = [('2007',2007),('2008',2008),('2009',2009),('2010',2010),('2011',2011)]
        # for text, value in years:
        #     rb = Radiobutton(year_frame, text=text, variable=self.year_var, value=value, command = self.sel)
        #     rb.pack(anchor=W)

        # self.label = Label(year_frame)
        # self.label.pack()

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

    # def sel(self):
    #     selection = 'You selected the year '+str(self.year_var.get())
    #     self.label.config(text = selection)

    def login(self):
        self.user = User()
        id_ = self.id_entry.get()
        # year = int(self.year_var.get())
        # print(year)
        # print(type(year))
        # print('public key :' + str(self.client.public_key))
        password = self.password_entry.get()
        if self.user.login_board(id_, password):
            tkinter.messagebox.showinfo('Login', 'you are login.')
            """Destroys current frame and replaces it with a new one."""
            self.master.switch_frame(ConfigPage, self.blockchain, self.client, self.user)            
        else:
            tkinter.messagebox.showerror('Error', 'Login failed.')

    def to_register_page(self):
        """Destroys current frame and replaces it with a new one."""
        self.master.switch_frame(RegisterPage, self.blockchain, self.client, self.user)

class RegisterPage(Frame):
    def __init__(self, master, blockchain= None, client=None, user=None):
        Frame.__init__(self, master)

        self.blockchain = blockchain
        self.client = client
        
        #student id
        stud_id_frame = Frame(self)
        stud_id_frame.pack()
        stud_id_label = Label(stud_id_frame, text ='Student ID')
        stud_id_label.pack(side = LEFT)
        self.stud_id_entry = Entry(stud_id_frame, bd=5)
        self.stud_id_entry.pack(side = LEFT)

        #Board id
        board_id_frame = Frame(self)
        board_id_frame.pack()
        board_id_label = Label(board_id_frame, text ='Board ID')
        board_id_label.pack(side = LEFT)
        self.board_id_entry = Entry(board_id_frame, bd=5)
        self.board_id_entry.pack(side = LEFT)

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
            stud_id = self.stud_id_entry.get()
            board_id = self.board_id_entry.get()
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
            print(password)
            if password == repassword:
                board = Board(stud_id, board_id, fname, lname, department, section, year, member_password=password)
                if user.board_register(board):
                    tkinter.messagebox.showinfo('Register', 'you are Registerd.')
                else:
                    tkinter.messagebox.showerror('Error', 'Registration failed.')
            else:
                tkinter.messagebox.showerror('Error', 'password is incorrect')

class ConfigPage(Frame):
    def __init__(self, master, blockchain= None, client = None, user= None):
        Frame.__init__(self, master)

        self.blockchain = blockchain
        self.client = client
        self.url = None
        
        #port number
        port_frame = Frame(self)
        port_frame.pack()
        port_label = Label(port_frame, text ='Port ')
        port_label.pack(side = LEFT)
        self.port_entry = Entry(port_frame, bd=5)
        self.port_entry.pack(side = LEFT)

        #IP number or domain name
        ip_frame = Frame(self)
        ip_frame.pack()
        ip_label = Label(ip_frame, text ='IP Number ')
        ip_label.pack(side = LEFT)
        self.ip_entry = Entry(ip_frame, bd=5)
        self.ip_entry.pack(side = LEFT)

        #test button --- to test port number and IP number
        w = tkinter.Button(self, bg='Blue', text='Test',command = self.test)
        w.pack()

        #start time
        start_frame = Frame(self)
        start_frame.pack()
        start_label = Label(start_frame, text ='Start Time')
        start_label.pack(side = LEFT)
        self.start_entry = Entry(start_frame, bd=5)
        self.start_entry.pack(side = LEFT)

        #end time
        end_frame = Frame(self)
        end_frame.pack()
        end_label = Label(end_frame, text ='End Time')
        end_label.pack(side = LEFT)
        self.end_entry = Entry(end_frame, bd=5)
        self.end_entry.pack(side = LEFT)

        #new node
        node_frame = Frame(self)
        node_frame.pack()
        node_label = Label(node_frame, text ='Node URL')
        node_label.pack(side = LEFT)
        self.node_entry = Entry(node_frame, bd=5)
        self.node_entry.pack(side = LEFT)

        #root or genesis node
        self.var_root = IntVar()
        root_frame = Frame(self)
        root_frame.pack()
        Checkbutton(root_frame, text='root', variable=self.var_root).pack()

        #Connect button
        w = tkinter.Button(self, bg='Green', text='Connect',command = self.connect)
        w.pack()

    def connect(self):
        """ Connect the present node with other nodes in the network."""
        port = self.port_entry.get()
        threading.Thread(target=self.set_up_blockchain_and_connect_to_node, args=(port,)).start()
        
        # tkinter.messagebox.showinfo('Connect','The system connect the node.')
        # print('login  nn')
        # print(type(self.blockchain),' befor login')
        # self.master.switch_frame(LoginPage_, blockchain=self.blockchain, client=self.client)
        # async def to_voter_login_page
        
        
    def set_up_blockchain_and_connect_to_node(self, port):
        self.client = Client()
        self.client.create_keys()
        self.blockchain = Blockchain(self.client.public_key)

        # port = self.port_entry.get()

        # hostname = socket.gethostname()    
        # IPAddr = socket.gethostbyname(hostname)
        print(self.client.public_key)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        IPAddr = s.getsockname()[0]
        s.close()
        print(IPAddr)
        print(type(IPAddr))

        # time.sleep(10)
        self.to_voter_login_page(self.blockchain, self.client)
        server = Server(IPAddr, port, blockchain = self.blockchain, client=self.client)
        
        server.main()
        
        # time.sleep(1)
        print('the server already start........')
        if self.var_root.get() is 0:
            self.url = str(self.node_entry.get())+'/register_new_node'
            print(self.url)
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            IPAddr = s.getsockname()[0]
            s.close()
            # port = self.port_entry.get()

            print('new tread start...')

            # threading.Thread(target=self.blockchain.send_nodes(self.url,f'http://{IPAddr}:{port}')).start()
            threading.Thread(target=send_to_node).start()

            

            print('connect ot onother node')
            # self.blockchain.connect_node(self.url, f'http://{IPAddr}:{port}')

            async def send_to_node():
                if await self.blockchain.connect_to_new_node(self.url, f'http://{IPAddr}:{port}'):
                    print('connection succed.')
                    tkinter.messagebox.showinfo('Connect','The system connect the node.')

                else:
                    print('connection failed.')
                    tkinter.messagebox.showerror('Error','Your node not connected.')
        else:
            print('the first node')
            

    def test(self):
        """Test the port number and IP numer of the computer if it's available or not in the computer """
        port = int(self.port_entry.get())
        host = self.ip_entry.get()
        if self.check_port(port, host):
            tkinter.messagebox.showinfo('Test port', 'The port is available.')
        else:
            tkinter.messagebox.showerror('Error', 'The port is not available.')
            
    def check_port(self, port, host, rais=True):
        """ True -- it's possible to listen on this port for TCP/IPv4 or TCP/IPv6
        connections. False -- otherwise.
        """
        # hostname = socket.gethostname()    
        # IPAddr = socket.gethostbyname(hostname)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        IPAddr = s.getsockname()[0]
        s.close()
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # sock.bind(('127.0.0.1', port))
            # sock.bind((host, port))
            sock.bind((IPAddr, port))
            print('Server ip address is :'+IPAddr)
            sock.listen(5)
            sock.close()
            sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            sock.bind(('::1', port))
            sock.listen(5)
            sock.close()
        except socket.error as e:
            
            if rais:
                raise RuntimeError(
                    "The server is already running on port {0} \n {1}".format(port,e))
            return False
        return True

    def to_voter_login_page(self, blockchain, client):
        self.master.switch_frame(LoginPage_, blockchain, client)
