from collections import OrderedDict
import uuid
from user.student import Student

class Candidate:
    def  __init__(self, first_name, last_name, department, section, year, cgpa, student_id, candidate_id,  status='candidate', password = None):
        self.student = Student(first_name, last_name, department, section, year, student_id, status='candidate', password= password)
        self.candidate_id = candidate_id
        self.cgpa = cgpa
        self.willingness = True

    def to_order_dict(self):
        return OrderedDict([('first_name', self.student.first_name), ('last_name', self.student.last_name),('student_id', self.student.student_id),('candidate_id', self.candidate_id),('department', self.student.department),('section', self.student.section),('year', self.student.year),('cgpa', self.cgpa),('willingness', self.willingness),('password',self.student.password),('status', self.student.status)])