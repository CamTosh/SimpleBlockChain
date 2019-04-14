import os
import json
import requests
import datetime
import logging
from flask import Flask, request

from Node import *
from Nodes import *

app = Flask(__name__)

class Bootnode(Nodes):

	def __init__(self, file):
		self.lastUpdated = datetime.datetime.now()
		self.file = file
		if os.path.isfile(self.file):
			self.nodes = [Node(n['id'], n['ip'], n['port']) for n in self.load_data_from_file(self.file)['peers']]
		else:
			self.write_data_to_file(self.file, json.dumps({'peers': [], 'lastUpdated': str(self.lastUpdated)}))
			self.nodes = []
		
		super().__init__(self.nodes)

	def get_last_updated(self):
		return self.lastUpdated

	def add_peer(self, id, ip, port):
		try:
			if id in [node.toJson()['id'] for node in self.nodes]:
				return False
			
			newPeer = Node(ip, int(port), id)
			self.addPeers(newPeer)
			self.lastUpdated = datetime.datetime.now() 

			self.write_data_to_file(self.file, json.dumps({'peers': self.toJson(), 'lastUpdated': str(self.lastUpdated)}))

		except Exception as e:
			raise e
			return False

		return True

	def load_data_from_file(self, filename):
		try:
			file = open(filename, encoding='utf8')
			data = json.load(file)
			file.close()
			print("Datas loaded")
			return data
		except Exception as e:
			print("Can't load data from " + filename + ", error :")
			logging.exception(e)

	def write_data_to_file(self, filename, data):
		try:
			file = open(filename, 'w')
			file.write(data)
			file.close()  
			print("Datas writed")
		except Exception as e:
			print("Can't write data from " + filename + ", error :")
			logging.exception(e)

bootnode = Bootnode('peers.json')

@app.route('/peers', methods=['GET'])
def peers():
	return json.dumps(bootnode.toJson())

@app.route('/lastUpdated', methods=['GET'])
def lastUpdated():
	return json.dumps({'lastUpdated': str(bootnode.get_last_updated())[:19]})

@app.route('/peer', methods=['POST'])
def addPeer():
	request_values = request.get_json()
	
	id = request_values['id']
	ip = request_values['ip']
	port = request_values['port']
	
	return str(bootnode.add_peer(id, ip, port))

if __name__ == '__main__':
	app.run(host='localhost', port=1342)