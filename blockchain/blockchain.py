from typing import Dict, List
from time import time
import json
import hashlib
from urllib.parse import urlparse
import requests

class BlockChain(object):
    def __init__(self):
        self.chain: List[Dict] = []
        self.current_transactions: List[Dict] = []

        #create the genesis block
        self.new_block(previous_hash="1", proof=10)

    #Consensus start ===================================================================================
        self.nodes = set()

    def register_node(self, address: str) -> None:
        """
        Add a new node to the list of nodes
        :param address: <str> Address of a node, dominio + porta Eg. '192.168.0.5:5000'
        :return: None
        """
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def valid_chain(self, chain: List[Dict]) -> bool:
        """
        Determine if a given block chain is valid
        :param chain: <list> A blockchain
        :return: <bool> True if valid, False otherwaise
        """
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print(f'\n----------\n')
            #check if the hash of the previous block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False
            
            #chack that the proof of the work is correct
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False
            
            last_block = block
            current_index += 1

        return True

    def resolve_conflict(self) -> bool:
        """
        This is our consensus algo, it resolve conflicts
        by replacing our chain with the longest one in the network.
        :return: <bool> True if our chain was replaced, False if not
        """
        neighbours = self.nodes
        new_chain = None

        #We are only looking for chain longer then ours
        max_lenght = len(self.chain)

        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                #check if the is longer and the chain is valid
                if length > max_lenght and self.valid_chain(chain):
                    max_lenght = length
                    new_chain = chain

        # Replace our chain if we found a new valid longer then ours
        if new_chain:
            self.chain = new_chain
            return True
        return False
    #Consensus end ===================================================================================

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
