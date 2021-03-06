from .base import BaseDocument

class TextDocument(BaseDocument):
	def __init__(self, path):
		self.path = path
	
	def read(self):
		self.document = open(self.path, "r", encoding="utf-8")
		return self.document.read()
	
	def close(self):
		self.document.close()
		super().close()
