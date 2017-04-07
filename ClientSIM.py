import socket
import threading
import sys
################################################################################################


PORT1 = 7769
PORT2 = 7789


class Client(threading.Thread):
	"""docstring for Client"""

	def __init__(self, name):
		super(Client, self).__init__()
		self.name = name

	def driverSocketResponse(self):
		while True:
			raw_data = self.driver_server.recv(1024)
			print raw_data

	def commandReciever(self):

		while True:
			raw_data = command_server.recv(1024)
			print raw_data
			
	def driverSender(self):

		self.driver_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.driver_server.connect((IP, PORT2))	
		self.driver_server.send(self.name)
		t2 = threading.Thread(target=self.driverSocketResponse)
		t2.start()


		while True:
			inp = raw_input("_>")


			
			self.driver_server.send(inp)

	def run(self):
		global PORT1, PORT2
		command_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.command_server = command_server

		# Send Command socket
		self.command_server.connect((IP, PORT1))
		auth_message = "-a "+self.name
		self.command_server.send(auth_message)

		# Create Thread
		t1 = threading.Thread(target=self.driverSender)
		
		t1.start()
		
			
if __name__ == '__main__':

	try:
		inp =  str(sys.argv[1])
	except Exception as e:
		inp = None
	if inp == '-m' :
		inp = "SIMULATOR_SET"
	else:
		inp = "PHONE"

	Client(inp).start()



################################################################################################################################################################



from pyfirmata import Arduino, util
from time import sleep
import os
board = Arduino('/dev/ttyS0')
print "car driving simmulator"
from pyfirmata import INPUT, OUTPUT, PWM, SERVO
from time import sleep


board = Arduino('/dev/ttyS0')
it = util.Iterator(board)
it.start()
################################################################


whell = board.get_pin('a:0:i')  		#set a0 pin input whell
accelerator = board.get_pin('a:1:i')	#set a1 pin input accellerator
brake = board.get_pin('a:2:i')			#set a2 pin input brake

p = board.get_pin('d:5:i')				#set d5 pin input gp
r = board.get_pin('d:6:i')				#set d6 pin input gr
n = board.get_pin('d:7:i')				#set d7 pin input gn
d = board.get_pin('d:8:i')				#set d8 pin input gd



def readDataWhell():
		t = whell.read()  # Read the value from pin 0
		if not t:  # Set a default if no value read
			t = 0
		else:
			t *= 100
		t=int((t/100)*180)
		t = 't'+str(t) 
		
def readDataAccelerator():
		a = accelerator.read()  # Read the value from pin 1
		if not a:  # Set a default if no value read
			a = 0
		else:
			a *= 100
			a = int((a*100)/8.0 )
		a = 'a'+str(a) 
		
def readDataBrake():
		b = brake.read()  # Read the value from pin 2
		if not b:  # Set a default if no value read
			b = 0
		else:
			b *= 100
			b = int((b*100)/24.0)
		b = 'b'+str(b) 
		
def readDataGear():
		gear_p = p.read()
		
		gear_r = r.read()
		
		gear_n = n.read() # Read if the button has been pressed.
		
		gear_d = d.read()

		if gear_p == True:
			
			gear = 'p'
		elif gear_r == True :
			
			gear = 'r'
		elif gear_n == True:
			
			gear = 'n'
		elif gear_d == True:
			
			gear = 'd'
		
		else:
			
			gear = 'k'
		
		gear = 'g'+str(gear) 