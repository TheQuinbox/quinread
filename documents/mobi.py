from .base import BaseDocument
import mobi
import shutil
import html_parser

class MobiDocument(BaseDocument):
	def __init__(self, path):
		self.path = path

	def read(self):
		final = ""
		dir, file = mobi.extract(self.path)
		self.document = open(file, "r", encoding="utf-8")
		content=self.document.read()
		self.document.close()
		shutil.rmtree(dir)
		final = html_parser.html_to_text(content)
		return final

	def close(self):
		super().close()
