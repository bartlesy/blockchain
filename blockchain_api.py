#!/usr/bin/env python3.6

import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request

from blockchain import Blockchain

blockchain = Blockchain()

app = Flask(__name__)

node_id = str(uuid4()).replace('-', '')


@app.route('/mine', methods=['GET'])
def mine():
    # run the PoW algo to get the next proof
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # create and receive reward for finding the proof
    # sender is "0" to signify that this is a newly minted coin
    blockchain.new_transaction(
        sender="0",
        recipient=node_id,
        amount=1
    )

    # forge the new block by adding it to the chain
    prev_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, prev_hash)
    response = {
        'message': "New block forged",
        "index": block["index"],
        "transactions": block['transactions'],
        "proof": block['proof'],
        "previous_hash": block["previous_hash"]
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # check that all req fields are present
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing fields', 400

    # create a new Transaction
    index = blockchain.new_transaction(**values)

    response = {'message': f'Transaction will be added to block {index}'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if not nodes:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'all_nodes': list(blockchain.nodes)
    }
    return jsonify(response), 201

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()
    if replaced:
        response = {
            'message': 'Our chain was replace',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': "Our chain is authoritative",
            'chain': blockchain.chain
        }
    return jsonify(response), 200




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
