from collections import OrderedDict

from user.student import Student
class Senate:
    def __init__(self, student_id, senate_id, first_name, last_name, department, section, year, role = None, status='senate', password=None):
        self.student =Student(first_name, last_name, department, section, year, student_id, status, password=password)
        self.senate_id = senate_id
        self.role = role

    def to_order_dict(self):
        return OrderedDict([('student_id', self.student.student_id),('senate_id', self.senate_id),( 'first_name', self.student.first_name),('last_name', self.student.last_name),('department', self.student.department),('section', self.student.section),('year', self.student.year), ('role', self.role),('status',self.student.status),('password', self.student.password)])