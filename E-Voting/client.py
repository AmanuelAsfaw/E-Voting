from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import Crypto.Random
import binascii

from utility.file_util import File_Manager

class Client:
    def __init__(self):
        self.private_key = None
        self.public_key = None

    def create_keys(self):
        private_key, public_key = self.generate_keys()
        self.private_key = private_key
        self.public_key = public_key

    def save_keys(self):
        if self.public_key != None and self.private_key != None:
            if File_Manager.save_keys(self.public_key, self.private_key):
                print('saving keys succed.')
                return True
            else:
                print('saving keys failed.')
                return False
        else:
            print('keys are errors!!!')    
            return False

    def load_keys(self):
        (public_key, private_key) = File_Manager.load_keys()
        if public_key != None and private_key != None:
            self.public_key = public_key
            self.private_key = private_key
            return True
        else:
            print('Load keys are failed.')
            return False
            
    @staticmethod
    def generate_keys():
        private_key = RSA.generate(2048, Crypto.Random.new().read)
        public_key = private_key.publickey()
        return (binascii.hexlify(private_key.exportKey(format='DER')).decode(), binascii.hexlify(public_key.exportKey(format='DER')).decode())

    def sign_vote(self, candidate, id):
        signer = PKCS1_v1_5.new(RSA.importKey(binascii.unhexlify(self.private_key)))
        h = SHA256.new((str(candidate)+str(id)+str(self.public_key)).encode('utf8'))
        signature = signer.sign(h)
        return binascii.hexlify(signature).decode('ascii')

    @staticmethod
    def verify_vote(vote):
        public_key = RSA.importKey(binascii.unhexlify(vote.node))
        verifier = PKCS1_v1_5.new(public_key)
        h = SHA256.new((str(vote.candidate)+str(vote.id)+str(vote.node)).encode('utf8'))
        return verifier.verify(h, binascii.unhexlify(vote.signature))


# if __name__ == "__main__":
#     client = Client()
#     client.generate_keys()

















    