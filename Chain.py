
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

@app.route('/wallet/balance', methods=['GET'])
def balance():
	return jsonify({'Balance': str(wallet.balance())})
