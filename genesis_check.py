from eth2spec.phase0.spec import *
import os
import json

with open('beacon_state_0.ssz', 'rb') as f:
    prysm_state = BeaconState.deserialize(f, os.stat('beacon_state_0.ssz').st_size)

    with open('prysm_genesis.json', 'wt') as f2:
        json.dump(prysm_state.to_obj(), f2, indent='  ')


with open('teku_genesis_state.json', 'r') as f:
    teku_state = BeaconState.from_obj(json.load(f))

    with open('teku_genesis.json', 'wt') as f2:
        json.dump(teku_state.to_obj(), f2, indent='  ')

# .readonly_iter() is only optimization, can do without
for i, prysm_v, teku_v in zip(range(len(prysm_state.validators)), prysm_state.validators.readonly_iter(), teku_state.validators.readonly_iter()):
    if prysm_v != teku_v:
        print(f"validator {i} differs:")
        print("prysm:")
        print(json.dumps(prysm_v.to_obj(), indent=' '))
        print("teku:")
        print(json.dumps(teku_v.to_obj(), indent=' '))

