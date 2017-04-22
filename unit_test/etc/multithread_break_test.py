import threading

class TestThread(threading.Thread):
	"""docstring for TestThread"""
	def __init__(self, name):
		super(TestThread,self).__init__()

		self.arg = name
		self.setter = True

	def run(self):
		while self.setter :
			pass		

	def gerSetter(self):
		return self.setter

	def stop(self):
		self.setter = False 
	

def test():
	try:
		print "start "+self.name
		while True:
			pass
	except KeyboardInterrupt as e:
		return False

if __name__ == '__main__':
	
	t1 = TestThread("1")
	t2 = TestThread("2")

	try:
		t1.setDaemon(True)
		t1.start()
		print "Begin !!!"

		while True:
			pass


	except KeyboardInterrupt as e:
		print "stop all thread"
		# t1.join	()


