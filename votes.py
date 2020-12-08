# Get a state JSON file, may take a while (pulls data of all 100k validators)
#
# standard API spec: https://ethereum.github.io/eth2.0-APIs/#/Config/getSpec
#  curl -s http://localhost:4000/eth/v1/debug/beacon/states/2832 > my_state_response.json
#
# Prysm API spec: https://api.prylabs.net/
# Warning: have to increase max GRPC size to pull an API response that is as large as the state
#  curl -s http://localhost:4000/eth/v1alpha1/debug/state?slot=2832 > my_state_response.json

# pip install eth2spec==1.0.0
from eth2spec.phase0.spec import *
import json
with open('my_state_response.json', 'r') as f:
    api_response = json.load(f)
    state_json = api_response["data"]
    state = BeaconState.from_obj(state_json)

# print("recompute the state root! (slow)", state.hash_tree_root().hex())

print("eth1 votes!")  # each of the votes is just the data that was voted for. Validation happens during block processing.
print('\n'.join(f'{i}: {vote}' for i, vote in enumerate(state.eth1_data_votes)))

print(f"state is at slot {state.slot}")

# root -> Eth1Data
votes_by_root = {}
# root -> count
vote_counts = {}

for vote in state.eth1_data_votes:
    root = vote.hash_tree_root()
    if root not in votes_by_root:
        votes_by_root[root] = vote
        vote_counts[root] = 0

    vote_counts[root] += 1

# Remember, from the spec:
#
# class Eth1Data(Container):
#     deposit_root: Root
#     deposit_count: uint64
#     block_hash: Bytes32

for root, vote_data in votes_by_root.items():
    vote_count = vote_counts[root]
    print(f"block: {vote_data.block_hash.hex()} dep root: {vote_data.deposit_root.hex()} ({vote_data.deposit_count} deposits) {vote_count} votes")

