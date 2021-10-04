from .base import BaseDocument
from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup

class EpubDocument(BaseDocument):
	def __init__(self, path):
		self.path = path

	def read(self):
		self.document = epub.read_epub(self.path)
		result = ""
		try:
			result += self.document.title
		except AttributeError:
			pass
		for id, _ in self.document.spine:
			item = self.document.get_item_with_id(id)
			if item is None:
				continue
			soup = BeautifulSoup(item.content, "lxml")
			for child in soup.find_all(["p", "div", "blockquote", "h1", "h2", "h3", "h4", "h5", "h6"]):
				result += child.text + "\n"
		return result

	def close(self):
		super().close()
