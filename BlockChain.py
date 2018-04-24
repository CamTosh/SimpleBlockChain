from Block import *
import time
import random

class BlockChain():
	DIFFICULTY = 1

	def __init__(self):
		self.nodes = []
		self.chain = []
		self.transactions_pool = []
		self.minerate = 1

	def set_mining_rate(self, minerate):
		self.minerate = minerate

	def is_valid(self):
		for i in range(1, len(self.chain)):
			last_block = self.chain[i-1]
			current_block = self.chain[i]

			if current_block.hash != current_block.compute_hash():
				print("Block invalid : hash of block is incorrect")
				print(current_block.hash)
				print(current_block.compute_hash())
			
				return False
			
			if last_block.hash != current_block.last_hash:
				print("Block are not chained properly")
			
				return False
			
			if current_block.hash[:self.DIFFICULTY] != self.string_difficulty():
				print("Block has no proof of work")
			
				return False
		
		return True


	def todict(self):
		todict = []
		for block in self.chain:
			todict.append(block.__dict__)

		return todict

	def add_transaction(self, transaction):
		self.transactions_pool.append(transaction)

	def last_block(self):
		return self.chain[-1]

	def hash(self, string):
		return str(hashlib.sha256(str(string).encode()).hexdigest())

	def string_difficulty(self):
		t = ''
		return t.rjust(self.DIFFICULTY, '0')

	def mine(self):
		last_block = self.last_block()
		pool = self.transactions_pool
		nonce = 0
		timestamp = time.time()
		
		while self.hash(str(last_block.hash) + str(timestamp) + str(Block.todict(pool)) + str(nonce))[:self.DIFFICULTY] != self.string_difficulty():
			if random.random() <= self.minerate:
				nonce += 1
		
		self.chain.append(Block(last_block.hash, pool, nonce, timestamp))

		return {
			"status": "ok",
			"data": {
				"last_block": last_block.hash,
				"pool": Block.todict(pool),
				"nonce": nonce,
				"timestamp": timestamp,
				"string_difficulty": self.string_difficulty(),
				"difficulty": self.DIFFICULTY
			}
		}


	def addBlock(self, last_block, pool, nonce, timestamp):
		
		print(len(last_block), type(last_block))
		print(str(last_block))
		print("---")
		print(len(self.last_block().compute_hash()), type(self.last_block().compute_hash()))
		print(str(self.last_block().compute_hash()))
		

		if last_block == self.last_block().compute_hash():			
			self.chain.append(Block(last_block, pool, nonce, timestamp))
			return True
		
		return False

	@staticmethod
	def genesis():
		return Block(0, {}, 0, time.time())
	
	@staticmethod
	def get_block_object_from_block_data(block_data):
		return Block(
			block_data['index'],
			block_data['proof'],
			block_data['previous_hash'],
			block_data['transactions'],
			timestamp=block_data['timestamp']
		)
	
	def addNode(self, address):
		self.nodes.append(address)
		return True
