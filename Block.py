import time
import hashlib

class Block:
    def __init__(self, last_hash, transactions, nonce, timestamp):
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.transactions = transactions
        self.nonce = nonce
        self.hash = self.compute_hash()


    def compute_hash(self):
        to_be_hashed = str(str(self.last_hash) + str(self.timestamp) + str(self.transactions) + str(self.nonce))
        return hashlib.sha256(to_be_hashed.encode()).hexdigest()


    @staticmethod
    def genesis():
        return None




    def to_json(self):
        return "lol"
