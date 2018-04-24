
class Node(object):

	def __init__(self, ip, port, id):
		
		self.ip = ip
		self.port = port
		self.id = id


	def toJson(self):
		return {
			"ip": self.ip,
			"port": self.port,
			"id": self.id,
		}