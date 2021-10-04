from .base import BaseDocument
import docx
import win32com.client

class DocxDocument(BaseDocument):
	def __init__(self, path):
		self.path = path

	def read(self):
		self.document = docx.Document(self.path)
		full_text = []
		for para in self.document.paragraphs:
			full_text.append(para.text)
		return "\n".join(full_text)

	def close(self):
		super().close()

class DocDocument(BaseDocument):
	def __init__(self, path):
		self.path = path

	def read(self):
		word = win32com.client.Dispatch("Word.Application")
		word.visible = False
		self.document = word.Documents.Open(self.path)
		doc = word.ActiveDocument
		text = doc.Range().Text
		return text

	def close(self):
		super().close()
