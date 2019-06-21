import json
import os

from block import Block
from vote import Vote
from user.candidate import Candidate
from user.student import Student
from user.board import Board
from user.senate import Senate 
 
class File_Manager:
    @staticmethod
    def load_data():
        try:
            with open('db/blockchain.txt', mode = 'r') as f:
                file_contents = f.readlines()
                
                """ Read blockchain form the file"""
                blockchain = json.loads(file_contents[0][:-1])
                updated_blockchain = []
                for block in blockchain:
                    for vt in block['votes']:
                        print(vt)
                    converted_vt = [Vote(vt['candidate'], vt['id']) for vt in block['votes']]

                    updated_block = Block(block['index'], block['preveous_hash'], converted_vt, block['proof'], block['timestamp'])

                    updated_blockchain.append(updated_block)
                
                blockchain = updated_blockchain

                """ Read open votes form the file"""
                open_votes = json.loads(file_contents[1])
                updated_votes = []
                for vt in open_votes:
                    updated_vote = Vote(vt['candidate'], vt['id'])

                    updated_votes.append(updated_vote)
                
                open_votes = updated_votes

                return blockchain, open_votes         
        
        except(IOError, IndexError):
             print('Load data Failed!!!!!!')
             return None, None
        finally:
            print('clean up')

    @staticmethod
    def save_data(blockchain, open_votes):
        try:
            with open('db/blockchain.txt', mode = 'w') as f:
                saveable_data = [block.__dict__ for block in [Block(block_el.index, block_el.preveous_hash, [vt.__dict__ for vt in block_el.votes], block_el.proof, block_el.timestamp) for block_el in blockchain]]
                f.write(json.dumps(saveable_data))
                f.write('\n')

                saveable_votes = [vt.__dict__ for vt in open_votes]
                f.write(json.dumps(saveable_votes))
                return True

        except(IOError, IndexError):
            print('Saving Failed!!!')
            return False
        finally:
            pass

    @staticmethod
    def save_data_in_pickle_file(blockchain, open_votes):
        try:
            with open('db/blockchain.p' , mode = 'w') as f:
                save_data = {
                    'chain': blockchain,
                    'votes': open_votes
                }
                f.write(save_data)
        except(IOError, IndexError):
            print('Saving Failed!!!')

    @staticmethod
    def save_keys(public_key, private_key):
        try:
            with open('db/client.txt', mode='w') as f:
                f.write(public_key)
                f.write('\n')
                f.write(private_key)
                return True
        except(IOError, IndexError):
            print('Saving client Error ....')
            return False
    
    @staticmethod
    def load_keys():
        try:
            with open('db/client.txt', mode ='r') as f:
                keys = f.readlines()
                public_key = keys[0][:-1]
                private_key = keys[-1]
                return public_key, private_key

        except (IOError, IndexError):
            print('Loading client is Error ...')
            return None, None

    @staticmethod
    def json_save_chain(chain, id):
        saveable_data = [block.__dict__ for block in [Block(block_el.index, block_el.preveous_hash, [vt.__dict__ for vt in block_el.votes], block_el.proof, block_el.timestamp) for block_el in chain]]
        data_dict = {f'{id}': saveable_data}
        print(saveable_data)
        print(type(saveable_data))
        if os.path.isfile('workspace.json'):
            #File is exists
            with open('workspace.json','a+') as outfile:
                # outfile.seek(outfile.tell() -1, os.SEEK_END)
                outfile.seek(0, os.SEEK_END)
                outfile.seek(outfile.tell() -1, os.SEEK_SET)
                outfile.truncate()
                outfile.write(',')
                json.dump(data_dict, outfile)
                outfile.write(']')
        else:
            # Create File
            with open('db/workspace.json','w') as outfile:
                array = []
                array.append(data_dict)
                json.dump(array, outfile)
    
    @staticmethod
    def json_read():
        with open('db/workspace.json','r') as f:
            datastore = json.load(f)
            print (datastore)
    
    @staticmethod
    def json_readed():
        with open('db/file.json','r') as outfile:
            data = outfile.readlines()
            print(data)
            print(type(data))
    
    @staticmethod
    def file_remove(file_name):
        if os.path.isfile(file_name):
            os.remove(file_name)
            return True
        else:
            return False

    @staticmethod
    def save_users(candidates=None, boards=None, senates=None):
        with open('db/user.txt', 'w') as f:
            if not candidates is None:
                save = [candidate.to_order_dict() for candidate in candidates]
                f.write(json.dumps(save))
                f.write('\n')
            else:
                f.write('\n')
            if not boards == None:
                save = [board.to_order_dict() for board in boards]
                f.write(json.dumps(save))
                f.write('\n')
            else:
               f.write('\n')
            if not senates is None:
                save = [senate.to_order_dict() for senate in senates]
                f.write(json.dumps(save))
    
    @staticmethod
    def load_users():
        try:
            with open('db/user.txt', 'r') as f:
                data = f.readlines()
                candidates = json.loads(data[0][:-1])
                print('-------------------')
                if not candidates is None:
                    converted_candidates = [Candidate(candidate['first_name'], candidate['last_name'], candidate['student_id'], candidate['candidate_id'],candidate['department'], candidate['section'], candidate['year'], candidate['cgpa'], candidate['status'],candidate['password']) for candidate in candidates]
                else:
                    converted_candidates = None
               
                boards = json.loads(data[1][:-1])
                if not boards is None:
                    converted_boards = [Board(board['student_id'], board['board_id'], board['first_name'],board['last_name'],board['department'],board['section'],board['year'], board['role'], board['status'],board['password'], board['member_password']) for board in boards]
                else:
                    converted_boards = None

                senates = json.loads(data[2])
                if not senates is None: 
                    converted_senates = [Senate(senate['senate_id'], senate['senate_id'],senate['first_name'],senate['last_name'],senate['department'], senate['section'], senate['year'], senate['role'], senate['status'], senate['password']) for senate in senates]
                else:
                    converted_senates = None
                return converted_candidates, converted_boards, converted_senates

        except(IndexError, IOError):
            print('loading error.')
            return None, None, None

    @staticmethod    
    def register_students(students, year):
        with open(f'db/student_db/{year}.txt', 'w') as f:
            save = [student.to_order_dict() for student in students]
            f.write(json.dumps(save))
    
    @staticmethod
    def load_students(year):
        try:
            with open(f'db/student_db/{year}.txt', 'r') as f:
                data = f.readline()
                out_put = json.loads(data)
                converted_data = [Student(student['first_name'], student['last_name'], student['department'], student['section'], student['year'], student['student_id'], student['status'], student['password']) for student in out_put]
                return converted_data
        except(IndexError, IOError):
            print('loading error.')
            return None

