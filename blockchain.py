#!/usr/bin/env python3.6
import hashlib
import json
from time import time


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # create the gensis block
        self.new_block(previous_hash=1, proof=100)


    def new_block(self, proof, previous_hash=None):
        """
        Create a new block in the blockchain

        :param proof[Int]: The proof given by the Proof of Work algo
        :param previous_hash[Str]: Hash of the previous block
        :return Dict: New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }

        self.current_transactions = []
        self.chain.append(block)
        return block


    def new_transaction(self, sender, recipient, amount):
	"""
        Creates a new transaction to go into the next mined last_block

        :param sender[String]: Address of the Sender
        :param receipient[String]: Address of the recipient
        :param amount[Float]: Amount
        :return Int: Index of the block that will hold this transaction
	"""
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })

        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        """
        Create a SHA-256 hash of a block

        :param block[Dict]: Block
        :return String:
        """
        # need to make sure the dict is ordered, or will have inconsistent hashes

        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]


