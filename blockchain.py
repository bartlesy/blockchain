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


    def new_block(self, proof: int, previous_hash: str=None) -> dict:
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


    def new_transaction(self, sender: str, recipient: str, amount: float):
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
    def hash(block: dict):
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

    def proof_of_work(self, last_proof: int):
        """
        Simple PoW:
            - find a number p` S.T. hash(pp`) contains 4 leading zeros, where p is the previous p`
            - p is the previous proof, and p` is the new proof

        :param last_proof[Int]:
        :return Int:
        """

        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof: int, proof: int):
        """
        Validates the proof: does hash(last_proof, proof) contain 4 leading zero

        :param last_proof[Int]: Prev proof
        :param proof[Int]: current proof
        :return Bool: True if correct else false
        """
        guess = '%d'.encode() % (last_proof * proof)
        guess_hash = hashlib.sha256(guess).hexdigest()
        return gues_hash.startswith('0000')


