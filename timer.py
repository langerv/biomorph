import threading

class Task(threading.Thread):
	def __init__(self, interval, execute, *args, **kwargs):
		threading.Thread.__init__(self)
		self.daemon = False
		self.stopped = threading.Event()
		self.interval = interval
		self.execute = execute
		self.args = args
		self.kwargs = kwargs

	def stop(self):
		self.stopped.set()
		self.join()

	def run(self):
		while not self.stopped.wait(self.interval.total_seconds()):
			self.execute(*self.args, **self.kwargs)

class Timer:
	def __init__(self):
		self.tasks = []

	def add_task(self, interval, execute, *args, **kwargs):
		self.tasks.append(Task(interval, execute, *args, **kwargs))

	def start(self):
		for t in self.tasks:
			t.start()

	def stop(self):
		for t in self.tasks:
			t.stop()