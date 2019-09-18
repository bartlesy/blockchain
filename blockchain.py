#!/usr/bin/env python3.6
import hashlib
import json
from time import time
from urllib.parse import urlparse


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()

        # create the gensis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof: int, previous_hash: str = None) -> dict:
        """
        Create a new block in the blockchain

        :param proof[Int]: The proof given by the Proof of Work algo
        :param previous_hash[Str]: Hash of the previous block
        :return Dict: New Block
        """

        block = {
            "index": len(self.chain) + 1,
            "timestamp": time(),
            "transactions": self.current_transactions,
            "proof": proof,
            "previous_hash": previous_hash or self.hash(self.chain[-1]),
        }

        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender: str, recipient: str, amount: float) -> int:
        """
        Creates a new transaction to go into the next mined last_block

        :param sender[String]: Address of the Sender
        :param receipient[String]: Address of the recipient
        :param amount[Float]: Amount
        :return Int: Index of the block that will hold this transaction
        """
        self.current_transactions.append(
            {"sender": sender, "recipient": recipient, "amount": amount}
        )

        return self.last_block["index"] + 1

    def register_node(self, address: str):
        """
        Add a new node to the list of nodes

        :param address[String]: address of node. E.g., 'http://192.168.0.5:5000'
        :return None:
        """
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
        return

    @staticmethod
    def hash(block: dict) -> str:
        """
        Create a SHA-256 hash of a block

        :param block[Dict]: Block
        :return String:
        """
        # need to make sure the dict is ordered, or will have inconsistent hashes

        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self) -> dict:
        return self.chain[-1]

    def proof_of_work(self, last_proof: int) -> int:
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
    def valid_proof(last_proof: int, proof: int) -> bool:
        """
        Validates the proof: does hash(last_proof, proof) contain 4 leading zero

        :param last_proof[Int]: Prev proof
        :param proof[Int]: current proof
        :return Bool: True if correct else false
        """
        guess = "%d".encode() % (last_proof * proof)
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash.startswith("0000")

    def valid_chain(self, chain: list) -> bool:
        """
        Determine if a given blockchain is valid

        :param chain[List]: A blockchain
        :return Bool: True if valid, else False
        """

        for last_block, block in zip(chain, chain[1:]):
            print(f"{last_block}")
            print(f"{block}")
            print("\n----------------\n")
            # check that the hash of the block is correct
            if block["previous_hash"] != self.hash(last_block["proof"], block["proof"]):
                return False

            # check that PoW is correct
            if not self.valid_proof(last_block["proof"], block["proof"]):
                return False

        return True

    def resolve_conflicts(self) -> bool:
        """
        This is our consensus algo, it resolves conflicts by replacing
        our chain with the longest one in the network

        :return bool: True if our chain was replaced, false if not
        """

        neighbors = self.nodes
        new_chain = None

        # only looking for chains longer than ours
        max_len = len(self.chain)

        # grab and verify all the chains from all the nodes in the network
        for node in neighbors:
            response = requests.get(f"http://{node}/chain")

            if response.status_code == 200:
                length = response.json()["length"]
                chain = response.json()["chain"]

                # check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True
        return False
