import requests
import json
import random
import hashlib
import time

URL = "http://localhost:1337/work"

def hash(string):
	return str(hashlib.sha256(str(string).encode()).hexdigest())

def __jsonStrOfTupleToTupleOfInt__(string):
	return tuple([int(k) for k in string[1:-1].replace('\'','').split(',')])

def getWork():
	return json.loads(requests.get(URL).text)

def submitWork(work):

	req = requests.post(URL, data=json.dumps(work))
	print("Submit Work: ", req.text)

if __name__ == '__main__':
	work = getWork()
	
	while hash(str(work['last_block']) + str(work['timestamp']) + str(work['pool']) + str(work['nonce']))[:int(work['difficulty'])] != work['string_difficulty']:
		blockTime = time.time()

		if random.random() <= int(work['minerate']):
			work['nonce'] += 1
			print(work['nonce'], "Hashrate: ", int(1 / (time.time() - blockTime)), "mh/s")
	
	work = {
		"last_block": work['last_block'],
		"nonce": work['nonce'],
		"pool": work['pool'],
		"timestamp": work['timestamp'] ,
		"difficulty": work['difficulty'],
		"minerate": work['minerate'],
	}
	print("Block Found: ", work['nonce'])

	submitWork(work)