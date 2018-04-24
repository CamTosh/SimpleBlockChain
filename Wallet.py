import SimpleCrypto as simplecrypto
from Transaction import *
import _pickle as pickle
import os.path
import time

class Wallet():
	
	def __init__(self, blockchain, owner):
		self.blockchain = blockchain
		self.owner = owner
		self.walletPath = 'wallets/'+ owner +'_wallet.pkl'
		
		if os.path.exists(self.walletPath):
			pkl_file = open(self.walletPath, 'rb')
			keys = pickle.load(pkl_file)
			pkl_file.close()
			self.private_key = keys['private']
			self.public_key = keys['public']
		
		else:
			self.public_key, self.private_key = simplecrypto.generate_keypair()
			keys = {'public': self.public_key, 'private': self.private_key}
			
			output = open(self.walletPath, 'wb')
			pickle.dump(keys, output)
			output.close()

		print("Wallet : " + str(self.owner))
		print("Public key : " + str(self.public_key))
		print("Private key (keep that safe) : " + str(self.private_key))

	def balance(self):
		balance = 0
		for block in self.blockchain.chain:
			for transaction in block.transactions:
				print(transaction)
				if transaction['sender'] == self.public_key:
					balance = balance - transaction['amount']
				if transaction['recipient'] == self.public_key:
					balance = balance + transaction['amount']
		return balance

	def new_transaction_signed(self, public_key, private_key, recipient, amount):
		
		public_key = self.__jsonStrOfTupleToTupleOfInt__(public_key)
		private_key = self.__jsonStrOfTupleToTupleOfInt__(private_key)
		
		recipient = self.__jsonStrOfTupleToTupleOfInt__(recipient)

		transaction_unsigned = Transaction(public_key, recipient, amount, None, time.time())
		to_sign = transaction_unsigned.dump()
		
		signature = simplecrypto.encrypt(private_key, to_sign)
		transaction_unsigned.sign_transaction(signature)
		transaction_signed = transaction_unsigned
		
		if transaction_signed.is_valid():
			self.blockchain.add_transaction(transaction_signed)
			print("transaction valid -> added to pool")
		else:
			print("something went wrong")


	def new_transaction(self, recipient, amount):
		
		transaction_unsigned = Transaction(self.public_key, recipient, amount, None, time.time())
		to_sign = transaction_unsigned.dump()
		
		signature = simplecrypto.encrypt(self.private_key, to_sign)
		transaction_unsigned.sign_transaction(signature)
		transaction_signed = transaction_unsigned
		
		if transaction_signed.is_valid():
			self.blockchain.add_transaction(transaction_signed)
			print("transaction valid -> added to pool")
		else:
			print("something went wrong")

	def __jsonStrOfTupleToTupleOfInt__(self, string):
		return tuple([int(k) for k in string[1:-1].replace('\'', '').split(', ')])