import sys
from html.parser import HTMLParser
import re
from html import entities

class MyHtmlParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.__text = []

	def handle_data(self, data):
		text = data.strip()
		if len(text) > 0:
			text = re.sub("[ \t\r\n]+", " ", text)
			self.__text.append(text + " ")

	def handle_starttag(self, tag, attrs):
		if tag == "p":
			self.__text.append("\n\n")
		elif tag == "br":
			self.__text.append("\n")

	def handle_startendtag(self, tag, attrs):
		if tag == "br":
			self.__text.append("\n\n")

	def text(self):
		return "".join(self.__text).strip()

def extract_text(html):
	if html is None:
		html = ""
	parser = MyHtmlParser()
	parser.feed(html)
	parser.close()
	return parser.text()
