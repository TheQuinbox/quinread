from .base import BaseDocument
import mobi
import shutil
from . html import HtmlDocument
from .epub import EpubDocument
from .pdf import PdfDocument

class MobiDocument(BaseDocument):
	def __init__(self, path):
		self.path = path
	
	def read(self):
		final = ""
		dir, file = mobi.extract(self.path)
		if file.lower().endswith(".epub"):
			parser = EpubDocument(file)
		elif file.lower().endswith(".pdf"):
			parser = PdfDocument(file)
		elif file.lower().endswith(".html") or file.lower().endswith(".htm"):
			parser = HtmlDocument(file)
		final = parser.read()
		parser.close()
		del parser
		shutil.rmtree(dir)
		return final
	
	def close(self):
		super().close()
