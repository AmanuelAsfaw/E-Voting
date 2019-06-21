from datetime import datetime
from collections import OrderedDict
import uuid

from utility.printable import Printable
class Vote(Printable):
    def __init__(self, candidate, id=uuid.uuid4().hex, node= 0, signature=0,  time= datetime.now()):
        self.candidate = candidate
        self.id = id
        self.node = node
        self.signature = signature
        self.time = str(time)

    def to_order_dict(self):
        return OrderedDict([('candidate',self.candidate),('id',self.id),('node', self.node),('signature', self.signature),('time', self.time)])
