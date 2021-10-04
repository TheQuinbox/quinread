import threading

class RepeatingTimer(threading.Thread):
	def __init__(self, interval, function, daemon=True, *args, **kwargs):
		threading.Thread.__init__(self)
		self.daemon = daemon
		self.interval = interval
		self.function = function
		self.args = args
		self.kwargs = kwargs
		self.finished = threading.Event()
		self.running = False

	def cancel(self):
		self.finished.set()
	stop = cancel

	def run(self):
		self.running = True
		while not self.finished.is_set():
			self.finished.wait(self.interval)
			if self.finished.is_set():
				self.running = False
				return
			try:
				self.function(*self.args, **self.kwargs)
			except:
				pass
