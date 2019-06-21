# Multi-frame tkinter application v2.3
import tkinter as tk
from view.login import LoginPage
from view.register import RegisterPage

class VoteApp(tk.Tk):
    def __init__(self, blockchain= None, client=None):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(LoginPage, blockchain, client)
        print('public key :' + str(client.public_key))

    def switch_frame(self, frame_class, blockchain, client, user=None):
        
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self, blockchain = blockchain, client = client)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

    @staticmethod
    def switch_to_login_page(cls, blockchain, client):
        cls.switch_frame(LoginPage, blockchain, client)

    def switch_to_register_page(self, blockchain, client):
        self.switch_frame(RegisterPage, blockchain, client)


# if __name__ == "__main__":
#     app = VoteApp()
#     app.mainloop()
