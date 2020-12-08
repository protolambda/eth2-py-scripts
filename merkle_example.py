from eth2spec.phase0.spec import *
from remerkleable.core import *
from remerkleable.tree import gindex_bit_iter, merkle_hash
from typing import Sequence


def pretty_path(p: Path) -> str:  # not the default repr, yet.
    return p.anchor.__name__ + '/'.join(str(k) for k, _ in slot_path.path)


# declare a typed anchor once, then re-use later
signed_block_anchor = Path(SignedBeaconBlock)

# easy python syntax to navigate paths
body_path = signed_block_anchor / 'message' / 'body'

# Works with lists too, go as deep as you need into a dynamic structure
att_2_data_path = Path(BeaconBlockBody) / 'attestations' / 2 / 'data'

# Declare some helper paths, to use later
att_data_slot_path = Path(AttestationData) / 'slot'
att_data_root_path = Path(AttestationData) / 'beacon_block_root'

# Combine paths like lego blocks!
slot_path = signed_block_anchor / body_path / att_2_data_path / att_data_slot_path
slot_gindex = slot_path.gindex()
print(f"gindex of slot attribute of 3rd attestation in signed block: {slot_gindex}, in binary: {bin(slot_gindex)}")

print("path in readable form", pretty_path(slot_path))
print("path anchor type:", slot_path.anchor)
print("path, with step by step types:", slot_path.path)

# Paths can be initialized from lists easily too
programmatic_use = Path(BeaconState, path=[('eth1_data', Eth1Data), ('deposit_count', uint64)])
print("deposit count gindex", programmatic_use.gindex())

# some example data
my_block = SignedBeaconBlock(message=BeaconBlock(body=BeaconBlockBody(
    eth1_data=Eth1Data(deposit_root='aa' * 32, deposit_count=0xc0ffee, block_hash='bb' * 32))))

# Now use the gindices on the tree backing:
tree_block = my_block.get_backing()
block_eth1_vote_path = Path(SignedBeaconBlock) / 'message' / 'body' / 'eth1_data'
eth1_vote_subtree = tree_block.getter(block_eth1_vote_path.gindex())
print("navigated subtree:")
print(eth1_vote_subtree)
print("its root:")
print(eth1_vote_subtree.merkle_root().hex())
print("enhance! (yes it's little endian)")
print(eth1_vote_subtree.get_left().get_right().merkle_root().hex())  # etc. navigate how you like

# or use the paths directly on views (typed trees)
obj = my_block
for key, typ in block_eth1_vote_path.path:
    obj = obj.navigate_view(key)
print("navigated view:", obj)


def build_proof(anchor: Node, leaf_index: Gindex) -> Sequence[Root]:
    if leaf_index <= 1:
        return []  # Nothing to proof / invalid index
    node = anchor
    proof = []
    # Walk down, top to bottom to the leaf
    bit_iter, _ = gindex_bit_iter(leaf_index)
    for bit in bit_iter:
        # Always take the opposite hand for the proof.
        # 1 = right as leaf, thus get left
        if bit:
            proof.append(node.get_left().merkle_root())
            node = node.get_right()
        else:
            proof.append(node.get_right().merkle_root())
            node = node.get_left()
    # we want to see bottom to top
    proof.reverse()
    return proof


# For debugging merkle proofs, a function to dump the whole tree
def get_tree(node: Node, gindex=1):
    if node.is_leaf():
        return node.merkle_root().hex()
    else:
        return {
            'root': node.merkle_root().hex(),
            'left': get_tree(node.get_left(), gindex=gindex * 2),
            'right': get_tree(node.get_right(), gindex=gindex * 2 + 1),
            'gindex': bin(gindex),
        }


# import json
# print(json.dumps(get_tree(tree_block), indent=4))


# Now let's do a merkle proof, just to proof that one subtree of an eth1 data vote:

eth1_data_commitment = my_block.hash_tree_root()
print("commitment:", eth1_data_commitment.hex())

eth1_data_proof = build_proof(tree_block, block_eth1_vote_path.gindex())
print("proof:")
print("\n".join(f"{i}: {root.hex()}" for i, root in enumerate(eth1_data_proof)))

eth1_data_leaf = my_block.message.body.eth1_data.hash_tree_root()
print("leaf value:", eth1_data_leaf.hex())


def verify_proof(commit: Root, proof: Sequence[Root], leaf: Root, leaf_gindex: Gindex) -> bool:
    bit_iter, _ = gindex_bit_iter(leaf_gindex)
    dat: Root = leaf
    for bit, sibling in zip(reversed(list(bit_iter)), proof):
        if bit:  # is the leaf on the right side?
            dat = merkle_hash(sibling, dat)
        else:
            dat = merkle_hash(dat, sibling)
    return dat == commit


# Let's see if it verifies!
print("proof verification:",
      verify_proof(eth1_data_commitment, eth1_data_proof, eth1_data_leaf, block_eth1_vote_path.gindex()))

# Now mingle with the leaf, verification should fail
eth1_data_leaf = Root(b"\x42" * 32)
print("proof verification after changing data:",
      verify_proof(eth1_data_commitment, eth1_data_proof, eth1_data_leaf, block_eth1_vote_path.gindex()))
