from .base import BaseDocument
from ebooklib import epub, ITEM_DOCUMENT
import html_parser

class EpubDocument(BaseDocument):
	def __init__(self, path):
		self.path = path

	def read(self):
		self.document = epub.read_epub(self.path)
		result = ""
		try:
			result += self.document.title + "\n"
		except AttributeError:
			pass
		for id, _ in self.document.spine:
			item = self.document.get_item_with_id(id)
			if item is None:
				continue
			result += item.content.decode()
		result = html_parser.parse_html(result)
		return result

	def close(self):
		super().close()
