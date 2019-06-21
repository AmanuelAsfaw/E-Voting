from passlib.hash import pbkdf2_sha256
from user.candidate import Candidate
from user.student import Student
from user.board import Board
from user.senate import Senate

class Auth:
    def __init__(self, user):
        self.user = user
    
    def set_password(self, password):
        hash = pbkdf2_sha256.hash(password)
        self.user.student.password = hash

    def verify_password(self, password):
        if self.user.student.password is None:
            return False
        return pbkdf2_sha256.verify(password, self.user.student.password)

class Auth_Board:
    def __init__(self, user):
        self.user = user
    
    def set_password(self, password):
        hash = pbkdf2_sha256.hash(password)
        self.user.student.password = hash

    def verify_password(self, password):
        if self.user.student.password is None:
            return False
        return pbkdf2_sha256.verify(password, self.user.student.password)

    def set_member_password(self, password):
        print(password)
        print(type(password))
        hash = pbkdf2_sha256.hash(password)
        print(hash)
        self.user.password = hash
    
    def verify_member_password(self, password):
        if self.user.password is None:
            return False
        return pbkdf2_sha256.verify(password, self.user.password)

class Auth_student:
    def __init__(self, user):
        self.user = user
    
    def set_password(self, password):
        hash = pbkdf2_sha256.hash(password)
        self.user.password = hash

    def verify_password(self, password):
        if self.user.password is None:
            print('password is None')
            return False
        return pbkdf2_sha256.verify(password, self.user.password)


# student =  Student('qaz','wsx','cse',1,2008,3.6,'stud1')
# au = Auth(student)
# au.set_password('qwe')
# print(au.user.student.first_name)
# print(au.user.first_name)
# ver = au.verify_password('qwe')
# ver2 = au.verify_password('qwer')        
# print(ver)
# print(ver2)

        