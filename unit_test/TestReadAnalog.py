import socket
import threading
import sys

from pyfirmata import Arduino, util
from time import sleep
import os
board = Arduino('/dev/ttyS0')
from pyfirmata import INPUT, OUTPUT, PWM, SERVO
from time import sleep

board = Arduino('/dev/ttyS0')
it = util.Iterator(board)
it.start()
################################################################################################
whell = board.get_pin('a:0:i')  		#set a0 pin input whell
accelerator = board.get_pin('a:1:i')	#set a1 pin input accellerator
brake = board.get_pin('a:2:i')			#set a2 pin input brake

P = board.get_pin('d:5:i')				#set d5 pin input gp
R = board.get_pin('d:6:i')				#set d6 pin input gr
N = board.get_pin('d:7:i')				#set d7 pin input gn
D = board.get_pin('d:8:i')				#set d8 pin input gd

CURRENT_GEAR = 'N'
CURRENT_WHEEL_ANGLES = 90
ACCELERATOR = 0
BRAKE = 0



	 
	
def readBrake():
	global DRIVER_SERVER, BRAKE
	while True:
		brk = brake.read()  # Read % value from pin 2
		brk = int(brk*100) #change to 0-100
		if not brk:
			BRAKE = 0
		elif brk != BRAKE:
			BRAKE = brk
			data = 'b' + str(BRAKE)
			print data
			DRIVER_SERVER.send(data)




if __name__ == '__main__':
	print "Start Server !! "
	
	
	Read_Brake_thread = threading.Thread(name = "Read_Brake", target=readBrake)
	
	Read_Brake_thread.start()
	