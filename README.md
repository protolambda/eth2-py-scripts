# Eth2 py scripts

Debugging tools, quick util / checks, etc. for Eth2.

Built with:
- [`eth2spec`](https://github.com/ethereum/eth2.0-specs)
- [`eth2`](https://github.com/protolambda/eth2.py/)
- [`eth2fastspec`](https://github.com/protolambda/eth2fastspec/)
- [`remerkleable`](https://github.com/protolambda/remerkleable/)

## Quick start

```shell script
# Create a python virtual environment, called `venv`
python -m venv venv
# Activate it
. venv/bin/activate
# Install dependencies into the venv
python install -r requirements.txt

# Run any script, e.g.
python pubkeys.py
```

Some scripts depend on a beacon state or other data. Use scripts like `fetch_state.py` to download it via the (not yet standardized) beacon API.
Or provide your own :)


## License

MIT, see [LICENSE](./LICENSE) file.

