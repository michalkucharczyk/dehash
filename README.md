# Hash Replacement Utility

This utility allows to replace hash values with more convenient entities - words, making it easier to work with them in
logs and other text outputs. It supports both long `0x5064528fea22246df948814b11da057079fc02268a6321172392e36319ff652d`
and short `0x5064…652d` versions of hashes. The tool also recognizes `Imported` debug logs and replaces block hashes
with `BLOCKXXX` strings, where `XXX` is the block number. Forks are supported.

## Features

- Replaces long and short hash values with words for better readability.
- Supports specific replacements for recognized patterns, such as `Imported` debug logs.
- outputs a graphviz file with blocks tree

## Examples
### Block numbers

before:
```
substrate: 🏆 Imported #1 (0xdf18…c4ac → 0x0626…a11a)    
txpool: maintain: txs:(0, 0) views:[1;[(1, 0, 0)]] event:NewBestBlock { hash: 0x0626c20236b05022c206363171118c7881fc8b0cd8d0b4f6d155f3dc6919a11a, tree_route: None }  took:122.731µs    
txpool: maintain: txs:(0, 0) views:[1;[(2, 0, 0)]] event:NewBestBlock { hash: 0x028dd13e51d2506717ccd5805ba01d55b5075638466a9fb9cc16b6b4812d8955, tree_route: None }  took:178.051µs    
substrate: 🏆 Imported #2 (0x0626…a11a → 0x028d…8955)    
txpool: maintain: txs:(0, 0) views:[1;[(3, 0, 0)]] event:NewBestBlock { hash: 0x76846df7d3378038af3ef3fe6a59f594a44f040b7b11e514426b9a6d8e83949b, tree_route: None }  took:132.931µs    
```
after:
```
substrate: 🏆 Imported #1 (DIPLEX → BLOCK1)    
txpool: maintain: txs:(0, 0) views:[1;[(1, 0, 0)]] event:NewBestBlock { hash: BLOCK1, tree_route: None }  took:122.731µs    
txpool: maintain: txs:(0, 0) views:[1;[(2, 0, 0)]] event:NewBestBlock { hash: BLOCK2, tree_route: None }  took:178.051µs    
substrate: 🏆 Imported #2 (BLOCK1 → BLOCK2)    
txpool: maintain: txs:(0, 0) views:[1;[(3, 0, 0)]] event:NewBestBlock { hash: BLOCK3, tree_route: None }  took:132.931µs    
```

### Hashes
before:

```
txpool: [0x5064528fea22246df948814b11da057079fc02268a6321172392e36319ff652d] ValidatedPool::submit_at
txpool: [0xd4418332fbea4124a743395aebfc4000829a7bdcd7afac0016b1c03106c56960] ValidatedPool::submit_at
txpool: [0x5869c9a4f7bace630f90928e50dc27653a2fd996abcd9e57a6b9af8642ea21d2] ValidatedPool::submit_at
txpool: [0xf9b677735803998fcce33eca325008f884a69dd036f0b5c1dcd8fb65bacb8cba] ValidatedPool::submit_at
sc_basic_authorship::basic_authorship: 🎁 Prepared block for proposing at ...  [0x5064…652d, 0xd441…6960, 0x5869…21d2, 0xf9b6…8cba]"
```
after:

```
txpool: [ABEL] ValidatedPool::submit_at
txpool: [FADE] ValidatedPool::submit_at
txpool: [BURN] ValidatedPool::submit_at
txpool: [STAR] ValidatedPool::submit_at
sc_basic_authorship::basic_authorship: 🎁 Prepared block for proposing at ...  [ABEL, FADE, BURN, STAR]"
```

# Usage
```
usage: dehash.py [-h] [-b] file

Replace hashes in the log file with words.

positional arguments:
  file          Path to the log file.

options:
  -h, --help    show this help message and exit
  -b, --backup  Create a backup of the original file.
```

Example:
```
dehash.py log.txt
```

# Testing
To run all tests execute:
```
python3 ./test_dehash.py
```
To run some tests only:
```
python3 ./test_dehash.py TestScript.test_filter_and_findall
python3 ./test_dehash.py TestScript2
```
