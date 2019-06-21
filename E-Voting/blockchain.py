from block import Block
from vote import Vote
from utility.hash_util import hash_string_256, hash_block
from utility.verification import Verification
from utility.file_util import File_Manager

from urllib.parse import urlparse
import requests
import json
import aiohttp
import ujson
import aiohttp
import async_timeout

#for testing 
# from client import Client

class Blockchain:
    def __init__(self,hosting_node):
        
        proof = 0
        while True:
            if Verification.valid_proof([],'',proof):
                break
            proof +=1

        genesis_block = Block(0,'',[],proof, '14:03:03.849673')
        self.__chain = [genesis_block]
        self.__open_votes = []
        self.hosting_node = hosting_node
        self.nodes_url = set() 
        self.candidates_set = set()

    @property
    def chain(self):
        return self.__chain[:]

    def get_chain(self):
        return self.__chain[:]

    @chain.setter
    def chain(self, val):
        self.__chain = val

    def get_open_votes(self):
        return self.__open_votes[:]

    async def add_to_open_votes(self, vote):
        """ If the public key of client not exist """
        if self.hosting_node == None:
            return False
        self.__open_votes.append(vote)
        
        # await self.save_data()

        if await self.send_vote(vote):
            print('Vote send.')
        else:
            print('Vote send failed.')

        return True

    async def load_data(self):
        (chain, open_votes) = await File_Manager.load_data()
        if chain == None and open_votes == None:
            return False
        else:
            self.__chain = chain
            self.__open_votes = open_votes
            return True

    async def save_data(self):
        # File_Manager.save_data_in_pickle_file(self.__chain, self.__open_votes)
        return await File_Manager.save_data(self.__chain, self.__open_votes)

    def get_last_blockchain_value(self):
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]
  
    def proof_of_work(self):
        last_block = self.get_last_blockchain_value()
        last_hash = hash_block(last_block)
        proof = 0
        while not Verification.valid_proof(self.__open_votes, last_hash, proof):
            proof +=1
        return proof

    async def add_vote(self, candidate, id, signature = 0):
        """ If the public key of client not exist """
        if self.hosting_node == None:
            return False
        vote = Vote(candidate,id, node=self.hosting_node, signature= signature)
        self.__open_votes.append(vote)

        if self.send_vote(vote):
            print('Vote send.')
        else:
            print('Vote send failed.')

        return True

    async def send_vote(self, vote):
        if len(self.nodes_url) > 0:
            dict_vote = vote.__dict__
            for node in self.nodes_url:
                url = f'http://{node}/receive_vote'
                # requests.post(url, json = dict_vote)
                async with aiohttp.ClientSession(json_serialize = ujson.dumps) as session:
                    await session.post(url, json = dict_vote)
            return True
        else:
            return False

    def mine_block(self):
        """ If the public key of client not exist """    
        if self.hosting_node == None:
            return None

        print('Minning Start')
        copied_votes = self.__open_votes[:]
        
        """ If there is no vote to mine """
        if len(copied_votes) == 0:
            print('There is no vote')
            return None

        last_block = self.get_last_blockchain_value()
        hashed_block = hash_block(last_block)
        
        proof = self.proof_of_work()
        
        block = Block(len(self.__chain),hashed_block, copied_votes, proof)
        print('before: '+str(len(self.__chain)))
        self.__chain.append(block)
        print('After: '+str(len(self.__chain)))
        self.__open_votes = []

        if self.send_block(block):
            print('Block send.')
        else:
            print('Block not send.')

        print('Minning End')

        return block

    async def send_block(self, block):
        """ Sending Minned block to all registered block."""

        if len(self.nodes_url) > 0:
            dict_block = Block.to_order_dict(block)
            # json_block = json.dumps(dict_block)
            for node in self.nodes_url:
                url = f'http://{node}/recieve_block'
                # requests.post(url, json = dict_block)
                async with aiohttp.ClientSession(json_serialize = ujson.dumps) as session:
                    await session.post(url, json = dict_block)
            return True
        else:
            return False
    
    def mine_by_other_client(self,block):
        """ If the public key of client not exist """    
        if self.hosting_node == None:
            return None
        if Verification.verify_block(block):
            last_block = self.get_last_blockchain_value()
            hashed_block = hash_block(last_block)
            
            block = Block(len(self.__chain), hashed_block, block.votes, block.proof, block.timestamp)

            self.__chain.append(block)
            print('mine done by other client.')
            return block
        return False
    
    def print_chain(self):
        for block in self.__chain:
            print('=======================')
            print(block.index)
            print(block.preveous_hash)
            print(block.timestamp)
            print(block.proof)
            for vote in block.votes:
                print('--------------')
                print(vote.candidate)
                print(vote.id)
                print('--------------')
        else:
            print('-'*20)
    
    def get_user_choice(self):
        user_input = input('Your choice: ')
        return user_input
    
    def verify_chain(self):
        (flag, error) =  Verification.verify_chain(self.__chain)
        if flag:
            return True
        else:
            """Replace the existing blcok by valid genesis block Block(0,'',[],100)"""
            if error == 'genesis_error':
                self.__chain[0] =  Block(0,'',[],100)
                print(self.__chain[0].proof)
                return False
            """Replace the existing chain by valid chain"""
            if error == 'hashing_error':
                return False
            if error == 'hashing_error':
                return False
                
    def verify_other_chain(self, chain):
        (flag, ) =  Verification.verify_chain(chain)
        return flag

    def verify_votes(self):
        if len(self.get_open_votes) > 0:
            if Verification.verify_votes(self.__open_votes):
                return True, 'valid'
            return False, 'error'
        else:
            return False, 'size'
    
    def save_candidates(self):
        pass
        # File_Manager.save_candidates(self.candidates_set)

    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes_url.add(parsed_url.netloc)

    async def send_nodes(self, reciver_node, sender_node):
        """ Sending nodes list from sender node to reciver node
            reciver_node: like 127.0.0.1:8000,
            sender_node: like http://127.0.0.1:8000 """
        nodes_list = []
        print('-------------list of nodes ----------------')
        for node in self.nodes_url:
            nodes_list.append(f'http://{node}')
            print (node)
        print('-----------------------------------------')
        nodes_list.append(sender_node)
        nodes_file = {
            'nodes': nodes_list,
            'count': len(nodes_list)
            }
        url = f'http://{reciver_node}/register_nodes'

        try:
            # requests.post(url, data = nodes_file)    
            # requests.post(url, json=nodes_file)
            async with aiohttp.ClientSession(json_serialize = ujson.dumps) as session:
                await session.post(url, json = nodes_file)
            print(nodes_list)    
            return True
        except(Exception):
            print("parsing error")
            return False

    def register_nodes(self, nodes):
        """ Registering nodes which are send form another node.
            nodes: type --- dict ---"""
        for node in nodes:
            parsed_url = urlparse(node)
            netloc = parsed_url.netloc
            if not netloc in self.nodes_url:
                print (node)
                self.add_node(node)
        print('==========')
        for n in self.nodes_url:
            print(n)
        return True
        
    async def repalce(self):
        """Replacing the chain by valid chain. Using Byzantine fault tolerance."""
        network = self.nodes_url
        chains = {}

        """ Byzantine fault tolerance """
        for node in network:
            print(node)
            response = None
            status_code = None
            # response = requests.get(f'http://{node}/chain')
            async with aiohttp.ClientSession() as session:
                async with session.get(f'http://{node}/chain') as resp:
                    status_code = resp.status
                    response = await resp.json()
            if status_code == 200:
                response_json = response
                new_chain = []
                print(response_json)
                for block in response_json:
                    added_block = Block(block['index'], block['preveous_hash'],[vt.__dict__ for vt in block['votes']], block['proof'], block['timestamp'])
                    new_chain.append(added_block)
                   
                if self.verify_other_chain(new_chain):
                    print(new_chain)
                    hashed_chain = str(new_chain).encode('utf8')
                    print(hashed_chain)
                    str_chain =str(new_chain)
                    print(str_chain)
                    if str_chain in chains.items():
                        chains[f'{str_chain}'] += 1
                        print(chains[f'{str_chain}'])
                        print('yes')
                    else:
                        print(str(chains))
                        chains[f'{str_chain}'] = 1
                        
                    print(chains)
            
        if len(chains) > 0:
            print(len(chains))
            for key in chains:
                print(type(key))
                
            # File_Manager.file_remove('workspace.json') 
            return True
        return False
            # if response.status_code == 200 and self.verify_other_chain(response.json()):

    async def replace_chain(self):
        """ Replacing chian, Using longest chain Algorithm."""
        network = self.nodes_url
        max_length = 0
        longest_chain = None

        """ Longest chain """
        for node in network:
            new_chain = []
            response = requests.get(f'http://{node}/chain')
            response = None
            status_code = None
            # response = requests.get(f'http://{node}/chain')
            async with aiohttp.ClientSession() as session:
                async with session.get(f'http://{node}/chain') as resp:
                    status_code = resp.status
                    response = await resp.json()
            if status_code == 200:
                length = response['length']
                chain = response['chain']
                for block in chain:
                    # added_block = Block(block['index'], block['preveous_hash'],[vt.__dict__ for vt in block['votes']], block['proof'], block['timestamp'])
                    added_block = Block(block['index'], block['preveous_hash'],[Vote(vt['candidate'], vt['id'], vt['node'], vt['signature']) for vt in block['votes']], block['proof'], block['timestamp'])
                    new_chain.append(added_block)
                if self.verify_other_chain(new_chain) and length > max_length:
                    longest_chain = new_chain
                    max_length = length
        if longest_chain:
            print(max_length)
            self.__chain = longest_chain
            return True
        return False

    def listen_for_input(self):
        waiting = True
        while waiting:
            print('please make choice:')
            print('1: for add vote')
            print('2: for Mine block')
            print('3: for Print chain')
            print('q: for Exit')
            choice = self.get_user_choice()
            if choice == '1':
                candidate = input('Input candidate name: ')
                id = input ('Input your id :')
                if self.add_vote(candidate,id):
                    print('vote added')
                    votes = self.__open_votes
                    for vote in votes:
                        print(vote.candidate)
                else:
                    print('faild')
            elif choice == '2':
                if not self.mine_block() == None:
                    print('Minning succed')
                    chain = self.__chain
                    print('chain length: '+str(len(chain)))
                    for block in self.__chain:
                        print('=============================')
                        print('index: '+str(block.index))
                        print('preveous hash: '+block.preveous_hash)
                        print('timestamp:'+str(block.timestamp))
                        print('proof:'+str(block.proof))
                else:
                    print('Minning failed')
            elif choice == '3':
                self.print_chain()
            elif choice == 'q':
                waiting = False
                print('Done!')
            else:
                print('Wrong Input')
    
    async def connect_to_new_node(self, receiver, sender):
        url = receiver+'/register_node/broadcast'
        try:
            # requests.post(url, data = nodes_file)    
            # requests.post(url, json=nodes_file)
            jsonn={'new_node': sender}
            print(type(jsonn))
            print(url)
            async with aiohttp.ClientSession(json_serialize = ujson.dumps) as session:
                with async_timeout.timeout(10):
                    async with session.post(url, json={'new_node': sender}) as resp:
                        status_code = resp.status
                        print(status_code)
                        data = await resp.read()
                        response = json.loads(data)
                        print('test')
                        print(type(response))  
                        print(response)
                        if status_code is 201:
                            print('*****************data found****************')
                            self.register_nodes(response)
                        else:
                            pass
            print(sender)    
            return True
        except(Exception) as e:
            print("parsing error")
            print(e)
            return False




