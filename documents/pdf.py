from .base import BaseDocument
import fitz

class PdfDocument(BaseDocument):
	def __init__(self, path):
		self.path = path

	def read(self):
		final = ""
		self.document = fitz.open(self.path)
		for page in self.document:
			text = page.get_text().encode("utf8")
			final += text.decode()
		return final

	def close(self):
		super().close()
