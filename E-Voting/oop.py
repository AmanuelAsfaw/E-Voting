from aiohttp import web 
import aiohttp
import asyncio
import logging

# from routes import setup_routes
from blockchain import  Blockchain 
from client import Client
from vote import Vote
from block import Block
from user.candidate import Candidate
from utility.file_util import File_Manager
from user.users import User
from user.student import Student

# from ui import VoteApp

from urllib.parse import urlparse

from utility.file_util import File_Manager
from urllib.parse import urlparse
import json
import ujson

class Server:
    def __init__(self, host, port, loop=asyncio.get_event_loop(), blockchain=None, client = None):
        self.host = host
        self.port = port
        self.loop = None
        # self.loop = asyncio.get_event_loop()
        self.tasks = []
        self.my_node = f'http://{host}:{port}'

        self.user = User()
        self.routes = web.RouteTableDef()
        self.blockchain = blockchain
        self.client = client
        self.app = web.Application()

    # @self.routes.get('/')
    async def handle(self, request):
        response_obj = {'status': 'success'}
        return web.Response(text=json.dumps(response_obj))

    # @self.routes.post('/user')
    async def new_user(self, request):
        try:
            user = request.query['name']
            print('Creating user', user)

            response_obj = {'status':'succes','message':'user create'}
            return web.Response(text=json.dumps(response_obj), status=200)
        except Exception as e:
            response_obj = {'status':'failed', 'reason': str(e)}
            return web.Response(text=json.dumps(response_obj), status=500)

    # @routes.get('/client')
    async def load_keys(self, request):
        if self.client.load_keys():
            self.blockchain = Blockchain(self.client.public_key)
            response = {
                'message': 'Keys are exist.',
                'public key': self.client.public_key,
                'private key': self.client.private_key,
            }
            return web.json_response(data=response, status = 201)
        else:
            response = {
                'message': 'loading keys failed'
            }
            return web.json_response(data=response, status = 500)

    # @routes.post('/keys')
    async def create_keys(self, request):
        self.client.create_keys()
        if self.client.save_keys():
            # global blockchain 
            self.blockchain = Blockchain(self.client.public_key)
            response = {
                'message': 'creating and saving keys are successed.',
                'public key': self.client.public_key,
                'private key': self.client.private_key,
            }
            return web.json_response(data=response, status = 201)
        else:
            response ={
                'message': 'Saving the keys failed.'
            }
            return web.json_response(data=response, status = 500)

    # @routes.post('/vote')
    async def add_vote(self, request):
        """If the client machine not create a keys."""
        if self.client.public_key == None:
            response = {
                'message': 'No client set up.'
            }
            return web.json_response(data=response, status = 400)

        """If user are not login."""
        if self.user.user is None:
            response = {
                'message': 'User are not Login.'
            }
            return web.json_response(data=response, status = 400)

        """If the request has not data."""
        values = await request.json()
        if not values:
            response = {
                'message': 'No data found.'
            }
            return web.json_response(data=response, status = 400)

        """If the required data has an missing. """
        required_fields = ['candidate', 'id']
        if not all(field in values for field in required_fields):
            response = {
                'message': 'Required data missing.'
            }
            return web.json_response(data=response, status = 400)
    
        candidate = values['candidate']
        vote = Vote(candidate)
        vote.signature = self.client.sign_vote(candidate, vote.id) 
        vote.node = self.client.public_key

        success = await self.blockchain.add_to_open_votes(vote)

        """if the system add vote successflly."""
        if success:
            response ={
                'message': 'Successfully added vote.',
                'vote':{
                    'candidate': candidate,
                    'id': vote.id,
                    'node': self.client.public_key,
                    'signature': vote.signature
                }
            }
            return web.json_response(data=response, status = 201)
        else:
            response = {
                'message': 'creating a vote failed.'
            }
            return web.json_response(data=response, status = 500)

    # @routes.post('/receive_vote')
    async def receive_vote(self, request):
        """ Recieving the vote form another client."""

        """ If client not set up."""
        if self.client.public_key == None:
            response = {
                'message': 'No client setup.'
            }
            return web.json_response(data=response, status = 400)
        
        result = await request.json()
        if not result:
            response = {
                'message': 'No data found.'
            }
            return web.json_response(data=response, status = 400)
        vote = Vote(result['candidate'], result['id'], result['node'], result['signature'])
        if self.client.verify_vote(vote):
            self.blockchain.add_to_open_votes(vote)
            response = {
                'message': 'Recieved succed.'
            }
            return web.json_response(data=response, status = 200)
        else:
            response = {
                'message': 'Corrapted vote.'
            }
            return web.json_response(data=response, status = 400)

    # @routes.post('/mine')
    async def mine(self, request):
        """ Mining the Blcok in to chain."""

        """ If client not set up."""
        if self.client.public_key == None:
            response = {
                'message': 'No client setup.'
            }
            return web.json_response(data=response, status = 400)

        block = self.blockchain.mine_block()
        if block != None:
            dict_block = block.__dict__.copy()
            dict_block['votes'] = [vt.__dict__ for vt in dict_block['votes']]
            response = {
                'message': 'Block added successfully.',
                'block': dict_block
            }
            return web.json_response(data=response, status = 201)
        else:
            response = {
                'message': 'Adding a block failed.',
                'client_set_up': self.client.public_key != None,
                'have_open_votes': len(self.blockchain.get_open_votes()) >= 0
            }
            return web.json_response(data=response, status = 500)

    # @routes.post('/recieve_block')
    async def recieve_block(self, request):
        """Verifing and adding to the blockchain, which mined by other client. """

        """ If client not set up."""
        if self.client.public_key == None:
            response = {
                'message': 'No client setup.'
            }
            return web.json_response(data=response, status = 400)

        result = await request.json()
        if not result:
            response = {
                'message': 'No data found.'
            }
            return web.json_response(data=response, status = 400)
        block = Block(result['index'], result['preveous_hash'],[Vote(vt['candidate'], vt['id'], vt['node'], vt['signature']) for vt in result['votes']], result['proof'], result['timestamp'])
        
        block = self.blockchain.mine_by_other_client(block)
        if block is  False:
            response = {
                'message': 'Corrapted block.'
            }
            return web.json_response(data=response, status = 400)
        elif not block is None:
            response = {
                'message' : 'Add the Block done.',
                'block' : Block.to_order_dict(block)
            }
            return web.json_response(data=response, status = 201)
        else:
            response = {
                'message' : 'Adding the block failed. No client set up.'
            }
            return web.json_response(data=response, status = 500)

    # @routes.get('/votes')
    async def get_open_votes(self, request):
        """ To get the votes which are not mined."""

        """ If client not set up."""
        if self.client.public_key == None:
            response = {
                'message': 'No client setup.'
            }
            return web.json_response(data=response, status = 400)
        
        votes = self.blockchain.get_open_votes()
        if len(votes) > 0:
            dict_votes = [vt.__dict__ for vt in votes]
            return web.json_response(data=dict_votes, status = 200)
        else:
            response = {
                'message': 'Has no open votes.'
            }
            return web.json_response(data=response, status = 500)

    # @routes.get('/chian')
    async def get_chain(self, request):
        """ To get full chain """

        """ If the client not set up."""
        if self.client.public_key == None:
            response = {
                'message': 'No client setup.'
            }
            return web.json_response(data=response, status = 400)

        chain_snapshot = self.blockchain.chain
        dict_chian = [block.__dict__.copy() for block in chain_snapshot]
        for dict_block in dict_chian:
            dict_block['votes'] = [vt.__dict__ for vt in dict_block['votes']]
        response = {
            'chain': dict_chian,
            'length': len(dict_chian)
        }

        return web.json_response(data=response, status = 200)

    # @routes.post('/verify')
    async def verify_chain(self, request):
        """ To verify chain """

        """ If client not set up."""
        if self.client.public_key == None:
            response = {
                'message': 'No client setup.'
            }
            return web.json_response(data=response, status = 400)

        if await self.blockchain.verify_chain():
            copied_chain = self.blockchain.chain
            dict_chain = [block.__dict__ for block in copied_chain]
            response = {
                'message': 'Valid chain.',
                'chain': dict_chain
            }
            return web.json_response(data=response, status = 201)
        else:
            response = {
                'message': 'Found error in chain.'
            }
            return web.json_response(data=response, status = 500)
    
    # @routes.get('/verify')
    async def verify_votes(self, request):
        """ To verify open votes."""

        """ If client not set up."""
        if self.client.public_key == None:
            response = {
                'message': 'No client setup.'
            }
            return web.json_response(data=response, status = 400)

        (flag, type) = await self.blockchain.verify_votes()
        if flag:
            votes = self.blockchain.get_open_votes()
            dict_votes = [vote.__dict__ for vote in votes]
            response = {
                'message': 'All Votes are Valid.',
                'open_votes': dict_votes
            }
            return web.json_response(data=response, status = 201)
        elif type == 'size':
            response = {
                'message': 'Open Votes not Found.'
            }
            return web.json_response(data=response, status = 500)
        response ={
            'message': 'Error foun in open Votes.'
        }
        return web.json_response(data=response, status = 500)

    # @routes.get('/data')
    async def load_data(self, request):
        if self.client.public_key == None:
            response = {
                'message': 'No client setup.'
            }
            return web.json_response(data=response, status = 400)
        if await self.blockchain.load_data():
            copied_chiain = self.blockchain.chain
            dict_chain = [block.__dict__ for block in copied_chiain]

            copied_votes = self.blockchain.get_open_votes()
            dict_votes = [vote.__dict__ for vote in copied_votes]
            response = {
                'message': 'Load data Succed.',
                'chain': dict_chain,
                'open_votes': dict_votes
            }
            return web.json_response(data=response, status = 201)
        else:
            response = {
                'message': 'Data Loading failed.'
            }
            return web.json_response(data=response, status = 500)
    
    # @routes.post('/data')
    async def save_data(self, request):
        if self.client.public_key == None:
            response = {
                'message': 'No client setup.'
            }
            return web.json_response(data=response, status = 400)
        if await self.blockchain.save_data():
            copied_chiain = self.blockchain.chain
            dict_chain = [block.__dict__ for block in copied_chiain]

            copied_votes = self.blockchain.get_open_votes()
            dict_votes = [vote.__dict__ for vote in copied_votes]
            response = {
                'message': 'Data Saved.',
                'chain': dict_chain,
                'open_votes': dict_votes
            }
            return web.json_response(data=response, status = 201)
        else:
            response = {
                'message': 'Data saving failed.'
            }
            return web.json_response(data=response, status = 500)

    # @routes.post('/register_new_node')
    async def registerNode(self, request):
        try:
            json = await request.json()
            node = json['new_node']
            parsed_url = urlparse(node)
            netloc = parsed_url.netloc

            if(node==self.my_node):
                response = {
                    'message':'current node cannot be added'
                }
                return web.json_response(data=response, status = 400)
            
            elif(netloc in self.blockchain.nodes_url):
                response = {
                    'message': 'already exist.'
                }
                return web.json_response(data=response, status = 400)
            else:
                self.blockchain.add_node(node)
                response = {
                    'note': 'New node registered successfully.' 
                    }
                return web.json_response(data=response, status = 200)
        except Exception as e:
            return web.json_response(data=json.dumps(e), status=500)

    # @routes.post('/register_node/broadcast')
    async def registerBroadcastNode(self, request):
        json = await request.json()
        new_node = json['new_node']
        parsed_url = urlparse(new_node)
        netloc = parsed_url.netloc
        if(new_node == self.my_node):
            return "current node cannot be added"
        if(netloc in self.blockchain.nodes_url):
            return "already exist"
        
        self.blockchain.add_node(new_node)

        for node in self.blockchain.nodes_url:
            url = f'http://{node}/register_new_node'
            parse_data = {
                'new_node': new_node
            }
            # task = asyncio.ensure_future(self.send_to(url, parse_data))
            # self.tasks.append(task)
            async with aiohttp.ClientSession(json_serialize = ujson.dumps) as session:
                await session.post(url, json = parse_data)
            # requests.post(url, json=parse_data)
        
        # task = asyncio.ensure_future(self.send_node(netloc, self.my_node))
        # self.tasks.append(task)
        await self.send_node(netloc, self.my_node)
        response = {
                        'message': 'All the nodes are now connected. The Blockchain now contains the following nodes:',
                        'total_nodes': [f'http://{node}' for node in self.blockchain.nodes_url]
                }
        return web.json_response(data=response, status = 201)

    # @routes.post('/register_nodes')
    async def register_nodes(self, request):
        json = await request.json()
        nodes = json['nodes']
        
        if nodes is None:
            response = {
                'message': 'Nodes are not found.'
            }
            return web.json_response(data=response, status = 400)
        if nodes.__contains__(self.my_node):
            nodes.remove(self.my_node) 
        
        self.blockchain.register_nodes(nodes)  
        #resend nodes to the sender of the nodes
        await self.blockchain.send_nodes(nodes[0], self.my_node)
        
        response = {
            'message': 'nodes registere successfuly'
        }
        return web.json_response(data=response, status = 200)

    # @routes.post('/send_nodes')
    async def send_nodes(self, request):
        # global my_node
        print('my_node is  '+self.my_node)
        if await self.blockchain.send_nodes('localhost:7000', self.my_node):
            response = {
                'message': 'Nodes are send successfully.'
            }
            return web.json_response(data=response, status = 200)
        else:
            response = {
                'message': 'Error get in process.'
            }
            return web.json_response(data=response, status = 500)

    # @routes.get('/replace')
    async def replace_chain(self, request):
        """ If client not set up."""
        if self.client.public_key == None:
            response = {
                'message': 'No client setup.'
            }
            return web.json_response(data=response, status = 400)

        if self.blockchain.replace_chain():
            response = {
                'message':'sucesss'
            }
            return web.json_response(data=response, status = 200)
        else:
            response = {
                'message': 'error exist'
            }
            return web.json_response(data=response, status = 500)

    # @routes.get('/get_nodes')
    async def get_nodes(self, request):
        """ If client not set up."""
        if self.client.public_key == None:
            response = {
                'message': 'No client setup.'
            }
            return web.json_response(data=response, status = 400)
            
        node_list = []
        for node in self.blockchain.nodes_url:
            node_list.append(node)
        if len(node_list) > 0:
            response = {
                'nodes': node_list,
                'count': len(node_list)
            }
            return web.json_response(data=response, status = 200)
        else:
            response = {
                'message':'Nodes not found.'
            }
            return web.json_response(data=response, status = 500)
    
    # @routes.post('/candidate')
    async def add_candidate(self, request):
        """ If client not set up."""
        if self.client.public_key == None:
            response = {
                'message': 'No client setup.'
            }
            return web.json_response(data=response, status = 400)

        """If user are not login."""
        if self.user.user is None:
            response = {
                'message': 'User are not Login.'
            }
            return web.json_response(data=response, status = 400)
        
        result = await request.json()
        if result is None:
            response = {
                'message':'data not found.'
            }
            return web.json_response(data=response, status = 400)
        """If the required data has an missing. """
        required_fields = ['first_name', 'last_name','department','section','year','cgpa','student_id','candidate_id']
        for values in result:
            if not all(field in values for field in required_fields):
                response = {
                    'message': 'Required data missing.'
                }
                return web.json_response(data=response, status = 400)
    
        for values in result:
            candidate =  Candidate(values['first_name'],values['last_name'],values['department'], values['section'], values['year'], values['cgpa'], values['student_id'], values['candidate_id'])
            self.blockchain.candidates_set.add(candidate)
        self.blockchain.save_candidates()
        response = {
            'message': 'Successfuly add candidates.'
        }
        return web.json_response(data=response, status = 200)

    # @routes.post('/student')
    async def add_student(self, request):
        """ If client not set up."""
        if self.client.public_key == None:
            response = {
                'message': 'No client setup.'
            }
            return web.json_response(data=response, status = 400)

        """If user are already login."""
        # global user
        if not self.user.user is None:
            response = {
                'message':'The user already login. Yout have to Logout to register.'
            }
            return web.json_response(data=response, status = 400)

        result = await request.json()
        if result is None:
            response = {
                'message': 'data not found.'
            }
            return web.json_response(data=response, status = 400)
        required_fields = ['student_id','first_name','last_name','department','section','year','password']
        if not all(field in result for field in required_fields):
            response = {
                'message': 'Required data missing.'
            }
            return web.json_response(data=response, status = 400)
    
        student = Student(result['first_name'],result['last_name'],result['department'],result['section'],result['year'],result['student_id'],password=result['password'])
        (boole, ) = self.user.student_register(student) 
        if boole:
            response = {
                'message': 'Register successfully.',
                'user_login': not self.user.user is None,
                'user_status': self.user.type
            }
            return web.json_response(data=response, status = 200)
        else:
            response = {
                'message': 'Register failed.',
                'user_login': not self.user.user is None,
                'user_status': self.user.type
            }
            return web.json_response(data=response, status = 400)

    # @routes.get('/candidates')
    async def get_candidates(self, request):
        """ If client not set up."""
        if self.client.public_key == None:
            response = {
                'message': 'No client setup.'
            }
            return web.json_response(data=response, status = 400)
        if len(self.blockchain.candidates_set) > 0:
            candidates = self.blockchain.candidates_set.copy()
            candidates_list = []
            for candidate in candidates:
                candidate = candidate.to_order_dict()
                candidates_list.append(candidate)
            response = {
                'candidates': candidates_list,
                'count': len(candidates)
            }
            return web.json_response(data=response, status = 201)
        else:
            response = {
                'message': 'candidates not found.'
            } 
            return web.json_response(data=response, status = 500)

    # @routes.post('/student/login')
    async def login(self, request):
        """ If client not set up."""
        if self.client.public_key == None:
            response = {
                'message': 'No client setup.'
            }
            return web.json_response(data=response, status = 400)

        """If user are already login."""
        # global user
        if not self.user.user is None:
            response = {
                'message':'The user already login. Yout have to Logout to Login again.'
            }
            return web.json_response(data=response, status = 400)

        result = await request.json()
        required_fields = ['id','year','password']
        if not all(field in result for field in required_fields):
            response = {
                'message': 'Required data missing.'
            }
            return web.json_response(data=response, status = 400)
        if self.user.login_student(result['id'],result['year'],result['password']):
            response = {
                'message': 'you are login Successfully',
                'user_login': not self.user.user is None,
                'user_status': self.user.type
            }
            return web.json_response(data=response, status = 201)
        else:
            response = {
                'message': 'Login failed.',
                'user_login': not self.user.user is None,
                'user_status': self.user.type
            }
            return web.json_response(data=response, status = 400)

    # @routes.post('/logout')
    async def logout(self, request):
        if self.user.user is None:
            response = {
                'message': 'user not login.'
            }
            return web.json_response(data=response, status = 400)

        self.user.user = None
        self.user.type = None
        response = {
            'message': 'Logout Successfully.'
        }
        return web.json_response(data=response, status = 200)


    async def on_shutdown(self, app):
        print('shutting down:', end='')
        for task in app['tasks']:
            print('#', end='')
            if not task.cancelled():
                task.cancel()
        for ws in app['websockets']:
            print('.', end='')
            await ws.close(code=aiohttp.WSCloseCode.GOING_AWAY, message='server shutdown')

        # global tasks
        for task in self.tasks:
            print('#', end='')
            if not task.cancelled():
                task.cancel()
        print('Done!')

    async def send_node(self, netloc, my_node):
            await self.blockchain.send_nodes(netloc, my_node)
    
    async def send_to(self, url, parse_data):
        async with aiohttp.ClientSession(json_serialize = ujson.dumps) as session:
                    await session.post(url, json = parse_data)

    async def add_to_route(self):
        self.app.router.add_get('/',self.handle)
        self.app.router.add_post('/user', self.new_user)
        self.app.router.add_get('/client', self.load_keys)
        self.app.router.add_post('/keys', self.create_keys)
        self.app.router.add_post('/vote', self.add_vote)
        self.app.router.add_post('/mine', self.mine)
        self.app.router.add_post('/recieve_block', self.recieve_block)
        self.app.router.add_get('/votes', self.get_open_votes)
        self.app.router.add_get('/chain', self.get_chain)
        self.app.router.add_post('/verify', self.verify_chain)
        self.app.router.add_get('/verify', self.verify_votes)
        self.app.router.add_get('/data', self.load_data)
        self.app.router.add_post('/data', self.save_data)
        self.app.router.add_post('/register_new_node',  self.registerNode)
        self.app.router.add_post('/register_node/broadcast', self.registerBroadcastNode)
        self.app.router.add_post('/register_nodes', self.register_nodes)
        self.app.router.add_post('/send_nodes', self.send_nodes)
        self.app.router.add_get('/replace', self.replace_chain)
        self.app.router.add_get('/get_nodes', self.get_nodes)
        self.app.router.add_post('/candidate', self.add_candidate)
        self.app.router.add_post('/student', self.add_student)
        self.app.router.add_get('/candidates', self.get_candidates)
        self.app.router.add_post('/student/login', self.login)
        self.app.router.add_post('/logout', self.logout)
        
    def main(self):

        # logging.basicConfig(level=logging.DEBUG)
        # logging.Logger
        # logging.getLogger("asyncio").setLevel(logging.WARNING)

        # import logging

        stdio_handler = logging.StreamHandler()
        stdio_handler.setLevel(logging.INFO)
        _logger = logging.getLogger('aiohttp.access')
        _logger.addHandler(stdio_handler)
        _logger.setLevel(logging.DEBUG)

        # kick off the web server
        async def start():
            # global app, tasks
            await self.add_to_route()
            runner = web.AppRunner(self.app, access_log=None)
            await runner.setup()
            print('setup finished')
            site = web.TCPSite(runner, self.host,self.port)
            await site.start()
            print('server start ...')
            asyncio.gather(*self.tasks)

        async def end():
            # global app
            await self.app.shutdown()
        print('main func')

        # async def ui():
        #     app = VoteApp()
        #     app.mainloop()
        
        asyncio.set_event_loop(asyncio.new_event_loop())
        asyncio.ensure_future(start())
        # self.loop.create_task(ui())
        # self.loop.run_until_complete(start())
        self.loop = asyncio.get_event_loop()

        # main program "loop"
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            # on exit, web server
            self.loop.run_until_complete(end())

        # stop the main event loop
        self.loop.close()

# if __name__ == '__main__':
#     server = Server('localhost', 8080)
#     server.main()


    