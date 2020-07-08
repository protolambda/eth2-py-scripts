from eth2spec.phase0.spec import *
import os

with open('my_state.ssz', 'rb') as f:
    state = BeaconState.deserialize(f, os.stat('my_state.ssz').st_size)

pubkey2index = {v.pubkey.hex(): i for i, v in enumerate(state.validators)}

import json
dat = json.dumps(pubkey2index, indent=4)
with open('pubkeys.json', 'wt') as f:
    f.write(dat)

print('done!')
