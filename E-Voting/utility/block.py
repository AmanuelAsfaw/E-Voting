from datetime import datetime

from .printable import Printable 

class Block(Printable):
    def __init__(self, index, preveous_hash, votes, proof,   time= datetime.now().time()):
        self.index = index
        self.preveous_hash = preveous_hash
        self.votes = votes
        self.proof = proof
        self.timestamp = str(time)
        