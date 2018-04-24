import SimpleCrypto as simplecrypto
import _pickle as pickle

class Transaction:

	def __init__(self, sender, recipient, amount, signature, timestamp):
		 self.sender = sender
		 self.recipient = recipient
		 self.amount = amount
		 self.signature = signature
		 self.timestamp = timestamp


	def dump(self):
		return str(self.sender) + str(self.recipient) + str(self.amount)
	
	def toJson(self):
		return {
			"sender": str(self.sender),
			"recipient": str(self.recipient),
			"amount": self.amount,
			"timestamp": self.timestamp,
		}

	def __dict__(self):
		return {
			"sender": str(self.sender),
			"recipient": str(self.recipient),
			"amount": self.amount,
			"timestamp": self.timestamp,
		}


	def sign_transaction(self, signature):
		self.signature = signature

	def is_valid(self):
		if simplecrypto.decrypt(self.sender, self.signature) == self.dump():
			return True
		else:
			return False
