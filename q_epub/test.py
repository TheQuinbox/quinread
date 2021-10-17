import epub
import sys
import os

if len(sys.argv) != 2:
	print("Usage: test.py <filename>")
	sys.exit()

path = sys.argv[1]
book = epub.EpubBook(path)
if not os.path.isfile(path):
	print("That file doesn't exist.")
	sys.exit()

f = open("book.txt", "w")
f.write(book.container.decode())
f.close()
