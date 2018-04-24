
class Nodes(object):

	def __init__(self, nodes):
		self.nodes = nodes

	def addPeers(self, node):
		self.nodes.append(node)

	def toJson(self):
		return [n.toJson() for n in self.nodes]