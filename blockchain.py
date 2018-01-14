#!/usr/bin/env python3.6

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

    def new_block(self):
        # Creates a new block and adds it to the chain
        pass

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
        # hashes a block
        pass

    @property
    def last_block(self):
        # returns the last block in the chain
        pass


