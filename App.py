import json
from Wallet import *
from flask import Flask, jsonify, request
from uuid import uuid4
import requests
import time
import json

app = Flask(__name__)

from BlockChain import *
from Transaction import *
from Network import *
from Node import *
from Nodes import *

n0 = Node("0.0.0.0", 1337, str(uuid4()).replace('-', ''))
n1 = Node("0.0.0.0", 1338, str(uuid4()).replace('-', ''))

nodes = Nodes([n0, n1])

blockchain = BlockChain()
blockchain.chain.append(blockchain.genesis())
# add into db
# share to other nodes

walletAlice = Wallet(blockchain, "Alice")
walletBob = Wallet(blockchain, "Bob")


@app.route('/valid', methods=['GET'])
def valid():
	return jsonify(blockchain.is_valid())

@app.route('/minerate', methods=['POST'])
def minerate():
	request_values = request.get_json()
	amount = request_values["amount"]
	blockchain.set_mining_rate(amount)
	
	return "Changed mining rate"


@app.route('/chain', methods=['GET'])
def chain():
	response = {
		'chain': blockchain.todict(),
		'length': len(blockchain.chain),
	}
	return jsonify(response), 200

@app.route("/tx/<id>", methods=['GET'])
def tx(id):
	print(id)
	for block in blockchain.todict():
		for i in block.pool:
			if i == id:
				return id

	return "error"

@app.route('/wallet/balance', methods=['GET'])
def balance():
	return jsonify({'Balance': str(wallet.balance())})


@app.route('/mine', methods=['GET'])
def mine():
	return jsonify(blockchain.mine())

@app.route('/work', methods=['GET'])
def getWork():
	#txPool = [tx.toJson() for tx in blockchain.transactions_pool]

	return jsonify({
			"last_block": str(blockchain.last_block().hash),
			"pool": [tx.toJson() for tx in blockchain.transactions_pool],
			"nonce": 0,
			"timestamp": time.time(),
			"string_difficulty": blockchain.string_difficulty(),
			"difficulty": blockchain.DIFFICULTY,
			"minerate": blockchain.minerate,
		})

@app.route('/work', methods=['POST'])
def postWork():
	request_values = request.get_json(force=True)
	required = ['last_block', 'pool', 'nonce', 'timestamp', 'difficulty', 'minerate']

	if request_values == None or not all(k in request_values for k in required):
		return 'Missing values', 400

	result = blockchain.addBlock(request_values['last_block'], request_values['pool'], request_values['nonce'], request_values['timestamp'])
	
	if result:
		return jsonify(blockchain.last_block().compute_hash())
	else:
		return jsonify("Don't be a jerk")





@app.route('/registerNode', methods=['POST'])
def registerNode():
	return request.get_json()
	"""
	request_values = request.get_json()
	address = request_values["address"]
	blockchain.addNode(address)

	return jsonify(address, " was added to node list")
	"""
@app.route('/addNode', methods=['POST'])
def addNode():

	request_values = request.get_json()
	address = request_values["address"]

	blockchain.addNode(address)
	r = requests.post(address + '/registerNode', data=jsonify({'address': 'http://localhost:1337'}))
	return "l"
	"""

	response = {
		'message': 'New node has been added',
		'node_count': len(blockchain.nodes),
		'nodes': list(blockchain.nodes),
	}
	return jsonify(response), 201
	"""

@app.route('/sync-chain', methods=['GET'])
def consensus():

	def get_neighbour_chains():
		neighbour_chains = []
		for node_address in blockchain.nodes:
			resp = requests.get(node_address + '/chain').json()
			chain = resp['chain']
			neighbour_chains.append(chain)
		return neighbour_chains

	neighbour_chains = get_neighbour_chains()
	if not neighbour_chains:
		return jsonify({'message': 'No neighbour chain is available'})

	longest_chain = max(neighbour_chains, key=len)  # Get the longest chain

	if len(blockchain.chain) >= len(longest_chain):  # If our chain is longest, then do nothing
		response = {
			'message': 'Chain is already up to date',
			'chain': blockchain.todict()
		}
	else:  # If our chain isn't longest, then we store the longest chain
		blockchain.chain = [blockchain.get_block_object_from_block_data(block) for block in longest_chain]
		response = {
			'message': 'Chain was replaced',
			'chain': blockchain.todict()
		}

	return jsonify(response)








"""
	@app.route('/transactions/new', methods=['POST'])
	def new_transaction():
		request_values = request.get_json()
		print(request)
		print(request_values)
		
		required = ['sender', 'recipient', 'amount']
		if request_values == None or not all(k in request_values for k in required):
			return 'Missing values', 400
		
		transaction = Transaction(request_values["sender"], request_values["recipient"], request_values["amount"])
		blockchain.add_transaction(transaction)
		
		return "Your transaction has been added to the pool"


	@app.route('/wallet/transaction', methods=['POST'])
	def new_transaction_wallet():

	request_values = request.get_json()
	required = ['recipient', 'amount', 'owner']
	
	if request_values == None or not all(k in request_values for k in required):
		return 'Missing values', 400
	
	wallet = Wallet(blockchain, request_values['owner'])
	transaction_signed = wallet.new_transaction(request_values['recipient'], request_values['amount'])
	
	return jsonify({
		'status': "Your transaction has been added to the pool",
		'data': transaction_signed
	})
"""
@app.route('/wallet/transaction/signed', methods=['POST'])
def new_transaction_signed():
	
	request_values = request.get_json()
	required = ['public_key', 'private_key', 'recipient', 'amount']
	
	if request_values == None or not all(k in request_values for k in required):
		return 'Missing values', 400
	
	transaction_signed = walletAlice.new_transaction_signed(
		request_values['public_key'],
		request_values['private_key'],
		request_values['recipient'],
		request_values['amount']
	)
	
	return jsonify({
		'status': "Your transaction has been added to the pool",
		'data': transaction_signed
	})

if __name__ == '__main__':
	app.run(host='localhost', port=1337)
