from .base import BaseDocument
import markdown
import html_parser

class MarkdownDocument(BaseDocument):
	def __init__(self, path):
		self.path = path
	
	def read(self):
		self.document = open(self.path, "r")
		text = self.document.read()
		html = markdown.markdown(text)
		return html_parser.html_to_text(html)
	
	def close(self):
		self.document.close()
		super().close()
