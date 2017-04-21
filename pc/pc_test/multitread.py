import threading 
import time
import Queue

def test2():

	time.sleep(3)

def test1():
	threading.Thread(target=test2).start()
	print threading.enumerate()

	time.sleep(3)

class EC(threading.Thread):
	"""docstring for ClassName"""	
	def __init__(self, name):
		threading.Thread.__init__(self)
		self.name = name			
	def run(self):
		time.sleep(3)

def cmd():
	while True:
		inp = raw_input("_>")
		if inp == "go" :
			e.set()
		elif inp == "wait" :
			e.clear()

def testEvent(e):

	while True:
		e.wait()
		time.sleep(0.5)
		print "Here"
		
if __name__ == '__main__':

	e = threading.Event()

	t = threading.Thread(target=testEvent, args=(e,) )
	t.start()

	t2 = threading.Thread(target=cmd)
	t2.start()


