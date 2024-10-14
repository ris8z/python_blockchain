from typing import Dict
from time import time
import json
import hashlib

class BlockChain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        #create the genesis block
        self.new_block(previous_hash="1", proof=10)

    def new_block(self, proof: int, previous_hash: str | None = None) -> Dict:
        """
        Create a new block in the chain
        :param proof: <int> the proof given by the Proof of work algorithm
        :param previous_hash: (Optional) <str> Hash of the previous block
        :return: <dict> New block
        """
        Block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }

        # reset the current list of transactions
        self.current_transactions = []

        self.chain.append(Block)
        return Block

    def new_transaction(self, sender: str, recipient: str, amount: int) -> int:
        """
        Creates a new transaction to go into the next mined Block
        :parm sender: <str> Address of the sender
        :parm recipient: <str> Address of the recipient
        :parm amount: <int> Amount
        :return: <int> The index of the block that will hold this transaction
        """

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block: Dict) -> str:
        # Hashs a Block
        """
        Create a SHA-256 hash of a Block
        :param block: <dict>
        :return: <str>
        """

        #json.dumps() gives u back the object as a string
        #encode gives u back the json as byte so then u can hash it
        block_string: bytes = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof:int) -> int:
        """
        Simple Proof Of Work Algorithm:
         - given that p is the last proof, and p' is the next proof 
         - Find a numper p' such that hash(pp') contains 4 leading 0s
        :param last_proof: <int>
        :return: <int>
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof: int, proof: int) -> bool:
        """
        Validates the Proof: Does hash(last_proof, proof) conatins 4 leading 0s
        :param last_proof: <int> Previous proof
        :param proof: <int> Current proof
        :return: <bool> True if it is correct, False otherwaise
        """
        guess: bytes = f'{last_proof}{proof}'.encode()
        guess_hash: str = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
