from .base import BaseDocument
import docx
from bs4 import BeautifulSoup

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
		self.document = open(self.path, "r", encoding="ISO-8859-1")
		soup = BeautifulSoup(self.document.read())
		[s.extract() for s in soup(["style", "script"])]
		temp_text = soup.get_text()
		text = "".join("".join(temp_text.split("\t")).split("\n")).encode("utf-8").strip()
		return text

	def close(self):
		super().close()
