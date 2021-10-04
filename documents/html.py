from .base import BaseDocument
import html2text
from bs4 import BeautifulSoup
import markdown

class HtmlDocument(BaseDocument):
	def __init__(self, path):
		self.path = path

	def read(self):
		self.document = open(self.path, "r", encoding="utf-8")
		text = self.document.read()
		text2 = html2text.html2text(text)
		html = markdown.markdown(text2)
		final = "".join(BeautifulSoup(html, features="html").findAll(text=True))
		return final

	def close(self):
		self.document.close()
		super().close()
