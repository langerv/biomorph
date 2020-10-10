import unittest
import time
from datetime import timedelta
from timer import Timer

WAIT_TIME_SECONDS1 = 1
WAIT_TIME_SECONDS2 = 2

class TestTimer(unittest.TestCase):

	def test_Timer(self):
		def foo1():
			print("foo1: {}".format(time.ctime()))

		def foo2(args):
			print("foo2: {}".format(args))

		timer = Timer()
		timer.add_task(interval=timedelta(seconds=WAIT_TIME_SECONDS1), execute=foo1)
		timer.add_task(interval=timedelta(seconds=WAIT_TIME_SECONDS2), execute=foo2, args="args")
		timer.start()
		while True:
			try:
				time.sleep(1)
			except KeyboardInterrupt:
				# print("Program killed: running cleanup code")
				timer.stop()
				break

if __name__ == '__main__':
	unittest.main()