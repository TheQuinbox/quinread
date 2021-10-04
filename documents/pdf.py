from .base import BaseDocument
from pyxpdf import Document, Config
from pyxpdf.xpdf import TextOutput, TextControl, page_iterator

class PdfDocument(BaseDocument):
	def __init__(self, path):
		self.path = path
		self.configure()

	def configure(self):
		Config.text_keep_tiny = False
		Config.text_eol = "unix"
		Config.text_page_breaks = False

	def read(self):
		self.document = Document(self.path)
		result = ""
		control = TextControl(mode="reading", enable_html=True, discard_diagonal=True)
		text_out = TextOutput(self.document, control)
		for pg_txt in page_iterator(text_out):
			result += pg_txt + "\n"
		return result

	def close(self):
		super().close()
