import zipfile
from exceptions import *
import utils

class EpubBook:
	def __init__(self, filename):
		self.filename = filename
		self.container = None
		self.load()

	def load(self):
		try:
			self.zf = zipfile.ZipFile(self.filename, "r", compression=zipfile.ZIP_DEFLATED, allowZip64=True)
		except zipfile.BadZipfile:
			raise EpubError("Bad Zip file provided.")
		except zipfile.LargeZipFile:
			raise EpubError("Large Zip file provided.")
		self.container = utils.read_from_zipfile(self.zf, "META-INF/container.xml")
