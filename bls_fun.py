from typing import (
    Sequence,
)
from math import (
    ceil,
    log2,
)
import abc
from eth_typing import (
    BLSPubkey,
    BLSSignature,
)
from eth_utils import (
    ValidationError,
)
from hashlib import sha256

from py_ecc.fields import optimized_bls12_381_FQ12 as FQ12
from py_ecc.optimized_bls12_381 import (
    add,
    curve_order,
    final_exponentiate,
    G1,
    multiply,
    neg,
    pairing,
    Z1,
    Z2,
)

from py_ecc.bls.hash import (
    hkdf_expand,
    hkdf_extract,
    i2osp,
    os2ip,
)
from py_ecc.bls.hash_to_curve import hash_to_G2
from py_ecc.bls.g2_primatives import (
    G1_to_pubkey,
    G2_to_signature,
    pubkey_to_G1,
    signature_to_G2,
)
from py_ecc.optimized_bls12_381 import (
    add,
    curve_order,
    final_exponentiate,
    G1,
    multiply,
    neg,
    pairing,
    Z1,
    Z2,
)

from py_ecc.bls.ciphersuites import G2ProofOfPossession as bls
priv = 100
pub = bls.SkToPk(priv)
print(pub.hex())

x = pubkey_to_G1(pub)
print(x)

x2 = add(x, x)
print(x2)

agg = G1_to_pubkey(x2)
print(agg.hex())

v = pubkey_to_G1(agg)
print(v)

