import tkinter as tk
from view.admin import LoginPage, RegisterPage, ConfigPage
import view.login
class Config(tk.Tk):
    def __init__(self, blockchain= None, client=None, user=None):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(LoginPage, blockchain, client, user)
        # print('public key :' + str(client.public_key))
    
    def switch_frame(self, frame_class, blockchain, client, user= None):
        
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self, blockchain = blockchain, client = client)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

    
    def switch_to_login_page(self, blockchain, client, user):
        self.switch_frame(LoginPage, blockchain, client, user)

    def switch_to_register_page(self, blockchain, client, user):
        self.switch_frame(RegisterPage, blockchain, client, user)

    def switch_to_configPage(self, blockchain, client, user):
        self.switch_frame(ConfigPage, blockchain, client, user)

    def switch_to_voter_login_page(self, blockchain, client):
        self.switch_frame( view.login.LoginPage, blockchain, client)

    def switch_to_voting_page(self, blockchain, client, user):
        self.switch_frame(view.voting.VotePage, blockchain, client, user=user)



if __name__ == "__main__":
    app = Config()
    app.mainloop()
