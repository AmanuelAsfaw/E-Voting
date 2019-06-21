from datetime import datetime

from utility.printable import Printable 

class Block(Printable):
    def __init__(self, index, preveous_hash, votes, proof,   time= datetime.now().time()):
        self.index = index
        self.preveous_hash = preveous_hash
        self.votes = votes
        self.proof = proof
        self.timestamp = str(time)

    @staticmethod
    def to_order_dict(block):
        return {
            'index': block.index,
            'preveous_hash': block.preveous_hash,
            'votes':[vt.__dict__ for vt in block.votes],
            'proof' : block.proof,
            'timestamp': block.timestamp
        }
        