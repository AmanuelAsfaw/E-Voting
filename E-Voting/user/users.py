from user.auth import Auth_student, Auth_Board, Auth
from utility.file_util import File_Manager
class User:
    def __init__(self):
        self.user = None
        self.type = None 
        
    def student_register(self,student):
        batch = File_Manager.load_students(student.year)
        if batch is None:
            auth = Auth_student(student)
            auth.set_password(student.password)
            batch = []
            batch.append(student)
            File_Manager.register_students(batch, student.year)
            self.user = student
            self.type = 'student'
            return True, 'batch'
        for student_batch in batch:
            if student_batch.student_id == student.student_id:
                return False, 'exist'
        auth = Auth_student(student)
        auth.set_password(student.password)
        batch.append(student)
        File_Manager.register_students(batch, student.year)
        self.user = student
        self.type = 'student'
        return True, 'success'

    def student_set_password(self, id, year, password):
        batch = File_Manager.load_students(year)
        if batch is None:
            return False
        for student in batch:
            if student.student_id == id:
                auth = Auth_student(student)
                self.user = student
                self.type = 'student'
                auth.set_password(password)
                File_Manager.register_students(batch, year)
    
    def login_student(self, id, year, password):
        batch = File_Manager.load_students(year)
        if batch is None:
            print('batch not found.')
            return False
        for student in batch:
            if student.student_id == id:
                print('user found.')
                print(student.first_name)
                print(student.password)
                auth = Auth_student(student)
                login = auth.verify_password(password)
                if login:
                    self.user = student
                    self.type = 'student'
                    return True
                else:
                    return False
        return False

    def board_register(self,board):
        (candidates, boards, senates) = File_Manager.load_users()
        if boards is None:
            auth = Auth_Board(board)
            auth.set_member_password(board.password)
            boards = []
            boards.append(board)
            File_Manager.save_users(candidates, boards, senates)
            self.user = board
            self.type = 'board'
            return True, 'boards'

        for board_member in boards:
            if board_member.board_id == board.board_id:
                return False, 'exist'

        auth = Auth_Board(board)
        auth.set_member_password(board.password)
        boards.append(board)
        File_Manager.save_users(candidates, boards, senates)
        self.user = board
        self.type = 'board'
        return True, 'success'

    def board_set_password(self, id, password):
        (candidates, boards, senates) = File_Manager.load_users()
        if boards is None:
            return False
        for board in boards:
            if board.board_id == id:
                auth = Auth_Board(board)
                self.user = board
                self.type = 'board'
                auth.set_password(password)
                File_Manager.save_users(candidates, boards, senates)

    def board_set_member_password(self, id, password):
        (candidates, boards, senates) = File_Manager.load_users()
        if boards is None:
            print('batch not found.')
            return False
        for board in boards:
            if board.board_id == id:
                auth = Auth_Board(board)
                self.user = board
                self.type = 'board'
                auth.set_member_password(password)
                File_Manager.save_users(candidates, boards, senates)

    def login_board(self, id, password):
        (candidates, boards, senates) = File_Manager.load_users()
        if boards is None:
            print('boards not found.')
            return False
        for board in boards:
            if board.board_id == id:
                print('board found.')
                print(board.student.first_name)
                print(board.password)
                auth = Auth_Board(board)
                login = auth.verify_member_password(password)
                if login:
                    self.user = board
                    self.type = 'board'
                    print('succed')
                    return True
                else:
                    print('not succed')
                    return False
        return False

    def logout(self):
        self.user = None
        self.type = None