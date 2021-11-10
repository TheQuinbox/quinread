from .base import BaseDocument
import fitz
import re

class PdfDocument(BaseDocument):
	def __init__(self, path):
		self.path = path
	
	def read(self):
		final = ""
		self.document = fitz.open(self.path)
		for page in self.document:
			text = page.get_text().encode("utf8")
			final += re.sub(" +\n", "\n", text.decode())
		return re.sub(r"\n\s*\n", "\n\n", final)
	
	def close(self):
		super().close()
