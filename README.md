# Block Chain

## What is a BlockChain?

A BlockChain is an immutable chain of records called Blocks.
They can contain transactions, files or any data you like.
But the important thing is that they're chained together using hashes.

## What does a block look like?

Each block has: 
- an index,
- a timestamp in UNIX time,
- a list of transactions,
- a proof,
- and an hash of the previous Block

```python3
block = {
    'index': 1,
    'timestamp': 1506057125.900785,
    'transactions': [
        {
            'sender': "8527147fe1f5426f9dd545de4b27ee00",
            'recipient': "a77f5cdfa2934df3954a5c7c7da5df1f",
            'amount': 5,
        }
    ],
    'proof': 324984774000,
    'previous_hash': "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
}
```
> [!IMPORTANT]
> each new block contains within itself, the hash of the previous Block. This is crucial because it’s what gives blockchains immutability: If an attacker corrupted an earlier Block in the chain then all subsequent blocks will contain incorrect hashes.

## What is Proof of Work?

Is how new block are created/mined on the chain,
The goal of PoW is to discover a number which solves a math problem.
The number must be **difficult to find** but **easy to verify** (by anyone on the network)

### Simple example
the goal is to find an hash of any integer x mutiplied by an integer y that ends with 0
`hash(x * y) = 123bsd...0` 
for this simplified exmaple let's fix x 
`x = 5` 
code in python
```python3
from hashlib import sha256
x = 5
y = 0
while sha256(f'{x*y}'.encode()).hexdigest()[-1] != "0":
    y += 1
print(f'The solution is y = {y}')
```
the solution now is:
`y = 21` 
because the hash ends in 0
`hash(5 * 21) = 1231a2312b31.....0` 

In bitcoin the miners solve the PoW, so a new block is createad, (the miners is rewarded with a coin)
and then every one in the network can his validity with ease


## Consensus
The whole point of blockchain is the fact that should be decentralized, so we neeed more nodes.
(each node is a computer/server that runs the blockchain code)

### How we ensure that all nodes have the same chain?
- we track all node with a set, and a register new node function
- each time to get the right chain we fetch all the chains from the other nodes
- the right one is the longest, we also need a valid chain function to check immbtuability
