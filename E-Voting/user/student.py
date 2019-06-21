from collections import OrderedDict
import uuid

class Student:
    def __init__(self, first_name, last_name, department, section, year, student_id, status='student', password=None):
        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name
        self.department = department
        self.section = section
        self.year = year
        self.voted = False
        self.password = password
        self.status = status

    def to_order_dict(self):
        return OrderedDict([('student_id', self.student_id),('first_name', self.first_name),('last_name', self.last_name),('department', self.department),('section', self.section),('year', self.year),('voted', self.voted),('password', self.password),('status', self.status)])
    
    