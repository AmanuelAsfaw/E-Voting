from utility.hash_util import hash_string_256, hash_block
from vote import Vote
from client import Client

class Verification:
    @staticmethod
    def valid_proof(votes, last_hash, proof):
        guess = (str([vt.to_order_dict() for vt in votes])+str(last_hash)+str(proof)).encode('utf8')

        print(guess)
        guess_hash = hash_string_256(guess)
        print(guess_hash)
        return guess_hash[0:2] == '00'

    @staticmethod
    def verify_vote(vote, candidates, users):
        if not vote.candidate in candidates:
            return False
        if not vote.id in users:
            return False
        return True

    @staticmethod
    def verify_vote_sign(vote):
        print(vote.candidate)
        print(vote.id)
        print(vote.node)
        print(vote.signature)
        print(type(vote.signature))
        flag = Client.verify_vote(vote)
        print(flag)
        if flag:
            print('-----vote valid--------')
            return True
        print('********vote invalid*********')
        return False

    @classmethod
    def verify_chain(cls, chain):
        for (index, block) in enumerate(chain):
            if index == 0:
                if not cls.valid_proof(block.votes, block.preveous_hash, block.proof):
                    print('proof of work is invalid')
                    """Replace the exiting blcok by valid genesis block Block(0,'',[],100)"""
                    return False,'genesis_error'
                else:
                    continue
            if not block.preveous_hash == hash_block(chain[index-1]):
                print('Hash Error')
                return False,'hashing_error'
            if not cls.valid_proof(block.votes, block.preveous_hash, block.proof):
                print('proof of work is invalid')
                return False, 'proof_error'
        return True, 'valid'

    @classmethod
    def verify_votes(cls, open_votes):
        return all([cls.verify_vote_sign(vote) for vote in open_votes]) 
    
    @classmethod
    def verify_block(cls, block):
        return cls.valid_proof(block.votes, block.preveous_hash, block.proof)
