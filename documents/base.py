class BaseDocument:
	def __init__(self, path):
		self.path = path
		self.document = None

	def read(self):
		pass

	def close(self):
		self.document = None
