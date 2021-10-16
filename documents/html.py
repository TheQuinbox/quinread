from .base import BaseDocument
import html_parser

class HtmlDocument(BaseDocument):
	def __init__(self, path):
		self.path = path

	def read(self):
		self.document = open(self.path, "r", encoding="utf-8")
		text = self.document.read()
		final = html_parser.html_to_text(text)
		return final

	def close(self):
		self.document.close()
		super().close()
