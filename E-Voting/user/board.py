from collections import OrderedDict
from user.student import Student

class Board:
    def __init__(self, student_id, board_id, first_name, last_name, department, section, year, role=None, status='board', password=None, member_password=None):
        self.student = Student(first_name,last_name, department, section, year, student_id, status= status, password=password)
        self.board_id = board_id
        self.role = role
        self.password = member_password
    
    def to_order_dict(self):
        return OrderedDict([('student_id', self.student.student_id),('first_name',self.student.first_name),('last_name',self.student.last_name),('department', self.student.department),('section', self.student.section),('year', self.student.year),('board_id', self.board_id),('role', self.role),('status', self.student.status),('password', self.student.password),('member_password', self.password),('status', self.student.status)])