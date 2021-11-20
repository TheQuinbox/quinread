from html.parser import HTMLParser
from html.entities import name2codepoint
import re

class HtmlToText(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.buf = []
		self.hide_output = False
		self.in_paragraph = False
	
	def handle_starttag(self, tag, attrs):
		if tag in ("b", "i"): return
		if tag in ("p", "div"):
			self.in_paragraph = True
		if tag in ("p", "br", "div", "h1", "h2", "h3", "h4", "h5", "h6", "blockquote", "li") and not self.hide_output:
			self.buf.append("\n")
		if tag in ("script", "style", "title"):
			self.hide_output = True
	
	def handle_startendtag(self, tag, attrs):
		if tag == "br":
			self.buf.append("\n")
	
	def handle_endtag(self, tag):
		if tag in ("script", "style", "title"):
			self.hide_output = False
		if tag in ("p", "div"):
			self.in_paragraph = False
	
	def handle_data(self, text):
		if text and not self.hide_output:
			if self.in_paragraph:
				text = text.replace("\r\n", " ")
				text = text.replace("\n", " ")
			text = re.sub(r"\s*\n\s*", "\n", text)
			self.buf.append(text)
	
	def handle_entityref(self, name):
		if name in name2codepoint and not self.hide_output:
			c = unichr(name2codepoint[name])
			self.buf.append(c)
	
	def handle_charref(self, name):
		if not self.hide_output:
			n = int(name[1:], 16) if name.startswith("x") else int(name)
			self.buf.append(unichr(n))
	
	def get_text(self):
		return re.sub(r" +", " ", "".join(self.buf))

def html_to_text(html):
	parser = HtmlToText()
	parser.feed(html)
	parser.close()
	# Bleck! Nested regex.
	return re.sub("\n\s", "\n", re.sub(r"\s\n\s", "\n", re.sub(r"\n\s*\n", "\n", parser.get_text()))).strip()
