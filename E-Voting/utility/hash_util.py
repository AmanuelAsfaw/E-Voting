import hashlib as hl
import json
from json import dumps

__all__ = ['hash_string_256', 'hash_block']

def hash_string_256(string):
    return hl.sha256(string).hexdigest()

def hash_block(block):
    # print(block.index)
    hasheble_block = block.__dict__.copy()
    # print(hasheble_block)
    # hasheble_block['timestamp'] = str(hasheble_block['timestamp'])
    hasheble_block['votes'] = [vt.to_order_dict() for vt in hasheble_block['votes']]

    return hl.sha256(json.dumps(hasheble_block, sort_keys= True).encode()).hexdigest()  