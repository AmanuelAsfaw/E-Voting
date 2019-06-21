import tkinter
import tkinter.messagebox
from tkinter import Label, Frame, Entry, LEFT, Button

from blockchain import Blockchain, Vote
from client import Client
# from ui import VoteApp 
import asyncio
import threading

# client = Client()
# client.create_keys()
# blockchain = Blockchain(client.public_key)



class VotePage(Frame):
    def __init__(self, master, blockchain= None, client = None, user=None):
        Frame.__init__(self, master)
        self.master = master
        self.blockchain = blockchain
        self.client = client
        self.user = user
        # if user is None:
        #     tkinter.messagebox.showerror('Error', 'The user not found.')
        #     self.master.switch_to_login_page(self.blockchain, self.client)
            
        #candidate
        candidate_frame = Frame(self)
        candidate_frame.pack()
        candidate_label = Label(candidate_frame, text='Candidate')
        candidate_label.pack(side=LEFT)
        self.candidate_entry = Entry(candidate_frame, bd=5)
        self.candidate_entry.pack(side=LEFT)

        #button - vote
        v = Button(self, bg='green', text='Vote',command=self.vote)
        v.pack()

    def save(self, vote):    
        if self.blockchain.add_to_open_votes(vote):
            tkinter.messagebox.showinfo('voting', 'vote succed.')
            # asyncio.sleep(0.01)
            # print(blockchain.get_open_votes()[0].to_order_dict())
            self.master.switch_to_login_page()
        else:
            tkinter.messagebox.showerror('Error', 'vote failed.')

    def vote(self):
        # global client
        candidate = self.candidate_entry.get()
        vote = Vote(candidate, node=self.client.public_key)
        print('public key :' + str(self.client.public_key))
        signature = self.client.sign_vote(candidate, vote.id)
        vote.signature = signature

        async def save():    
            print(type(self.blockchain))
            if await self.blockchain.add_to_open_votes(vote):
                tkinter.messagebox.showinfo('voting', 'vote succed.')
                # asyncio.sleep(0.01)
                # print(self.blockchain.get_open_votes()[0].to_order_dict())
                # self.master.switch_to_login_page(self.blockchain, self.client, user=None)

                # new_frame = LoginPage(self, self.blockchain, self.client)
                # if self.master._frame is not None:
                #     self.master._frame.destroy()
                # self.master._frame = new_frame
                # self.master._frame.pack()

                # VoteApp.switch_to_login_page(blockchain=self.blockchain, client=self.client)

                self.master.switch_to_voter_login_page(self.blockchain, self.client)


            else:
                tkinter.messagebox.showerror('Error', 'vote failed.')

        def save_thread():
            asyncio.set_event_loop(asyncio.new_event_loop())
            asyncio.ensure_future(save())
            loop = asyncio.get_event_loop()
            loop.run_forever()
            
        threading.Thread(target=save_thread).start()
        
        # self.save(vote)
    
    