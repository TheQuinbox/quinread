import posixpath

def read_from_zipfile(zip, filename):
	name = posixpath.normpath(filename)
	return zip.read(name)
