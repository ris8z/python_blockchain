from blockchain import BlockChain
from flask import Flask, jsonify, request
from uuid import uuid4

#we need 3 endpoints
#   /transactions/new   (to create a new transaction to a block)
#   /mine               (to tell our server to mine a new block)
#   /chain              (to return the full block chain)


# another two for consensus algo
#   /nodes/register     (to accept a list of new nodes in form of url)
#   /nodes/resolve      (to use our Consenus alog, so we know that we have the right chain)


# Instantiate our Node
app = Flask(__name__)

# Generate a global unique address for this node
node_identifier = str(uuid4()).replace('-','')

# Instantiate the Block Chain
blockchain = BlockChain()


@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work alog the get the next proof
    last_block = blockchain.last_block
    last_proof = last_block['proof']

    proof = blockchain.proof_of_work(last_proof)

    # We must recive a reward for finding the the proof
    # The sender is 0 to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # Forge the new block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New block forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400
    
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {
        'message': f'This transaction will be added to Block {index}',
    }
    return jsonify(response), 201 

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    valuse = request.get_json()

    nodes = valuse.get('nodes')

    if nodes is None:
        return "Error: Plase supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes)
    }

    return jsonify(response), 201 

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflict()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }
    return jsonify(response), 200

#test with postman
if __name__ == "__main__":
    p = int(input("Which port?"))
    app.run(host="0.0.0.0", port=p)
