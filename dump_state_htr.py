from eth2spec.phase0.spec import *
import os

with open('test_state.ssz', 'rb') as f:
    state = BeaconState.deserialize(f, os.stat('test_state.ssz').st_size)

# print(state.hash_tree_root().hex())

backing = state.get_backing()

from remerkleable.tree import Node

def get_tree(node: Node):
    if node.is_leaf():
        return node.merkle_root().hex()
    else:
        return {'root': node.merkle_root().hex(), 'left': get_tree(node.get_left()), 'right': get_tree(node.get_right())}

import json

data = get_tree(backing)
print(json.dumps(data, indent='  '))
