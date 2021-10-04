from .base import BaseDocument
from bs4 import BeautifulSoup
import markdown

class MarkdownDocument(BaseDocument):
	def __init__(self, path):
		self.path = path

	def read(self):
		self.document = open(self.path, "r")
		text = self.document.read()
		html = markdown.markdown(text)
		final = "".join(BeautifulSoup(html, features="html").findAll(text=True))
		return final

	def close(self):
		self.document.close()
		super().close()
