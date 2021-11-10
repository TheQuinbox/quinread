from .base import BaseDocument
from striprtf.striprtf import rtf_to_text

class RtfDocument(BaseDocument):
	def __init__(self, path):
		self.path = path
	
	def read(self):
		self.document = open(self.path, "r")
		text = self.document.read()
		text = rtf_to_text(text)
		return text
	
	def close(self):
		self.document.close()
		super().close()
