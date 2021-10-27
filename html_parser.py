from html.parser import HTMLParser
from html.entities import name2codepoint
import re

class HtmlToText(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self._buf = []
		self.hide_output = False

	def handle_starttag(self, tag, attrs):
		if tag in ("b", "i", "span"):
			return
		elif tag in ("p", "br", "div", "h1", "h2", "h3", "h4", "h5", "h6", "blockquote", "li") and not self.hide_output:
			self._buf.append("\n")
		elif tag in ("script", "style", "title"):
			self.hide_output = True

	def handle_startendtag(self, tag, attrs):
		if tag == "br":
			self._buf.append("\n")

	def handle_endtag(self, tag):
		if tag in ("script", "style", "title"):
			self.hide_output = False

	def handle_data(self, text):
		if text and not self.hide_output:
			self._buf.append(text)

	def handle_entityref(self, name):
		if name in name2codepoint and not self.hide_output:
			c = unichr(name2codepoint[name])
			self._buf.append(c)

	def handle_charref(self, name):
		if not self.hide_output:
			n = int(name[1:], 16) if name.startswith("x") else int(name)
			self._buf.append(unichr(n))

	def get_text(self):
		return re.sub(r" +", " ", "".join(self._buf))

def html_to_text(html):
	parser = HtmlToText()
	parser.feed(html)
	parser.close()
	return re.sub(r"\n\s*\n", "\n", parser.get_text()).strip()
