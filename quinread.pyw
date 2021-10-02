import sys
sys.dont_write_bytecode = True
import application

def setup():
	stderr_file = open("errors.log", "a")
	sys.stderr = stderr_file
	app = application.Application()
	app.run()

if __name__ == "__main__":
	setup()
