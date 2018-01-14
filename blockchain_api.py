#!/usr/bin/env python3.6

import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4

from flask import Flask

from blockchain import Blockchain

blockchain = Blockchain()

app = Flask(__name__)

node_id = str(uuid4()).replace('-', '')


@app.route('./mine', methods=['GET'])
def mine():
    return "we'll mine a new block"


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
