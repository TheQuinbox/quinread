import sys
from html.parser import HTMLParser
import re

class MyHtmlParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.__text = []

	def handle_data(self, data):
		text = data.strip()
		if len(text) > 0:
			text = re.sub("[ \t\r\n]+", " ", text)
			self.__text.append(text)

	def handle_starttag(self, tag, attrs):
		if tag == "br":
			self.text.append("\n\n")

	def handle_endtag(self, tag):
		if tag == "p" or tag == "div" or tag == "h1" or tag == "h2" or tag == "h3" or tag == "h4" or tag == "h5" or tag == "h6" or tag == "blockquote":
			self.__text.append("\n")
		elif tag == "br":
			self.__text.append("\n\n")

	def handle_startendtag(self, tag, attrs):
		if tag == "br":
			self.__text.append("\n\n")

	def text(self):
		return "".join(self.__text).strip()

def parse_html(html):
	if html is None:
		html = ""
	parser = MyHtmlParser()
	parser.feed(html)
	parser.close()
	return parser.text()
