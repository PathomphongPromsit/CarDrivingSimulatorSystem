from pyfirmata import Arduino, util
from time import sleep
import os
board = Arduino('/dev/ttyS0')
print "car driving simmulator"
from pyfirmata import INPUT, OUTPUT, PWM, SERVO
from time import sleep
import socket

board = Arduino('/dev/ttyS0')
it = util.Iterator(board)
it.start()
##################################################



    
   
   



########################################################################################################
global gear
gear = ''

whell = board.get_pin('a:0:i')

accelerator = board.get_pin('a:1:i')
brake = board.get_pin('a:2:i')

P = board.get_pin('d:5:i')
R = board.get_pin('d:6:i')
N = board.get_pin('d:7:i')
D = board.get_pin('d:8:i')
multiplier = 100
###############################################################################################################
try:
	while True:

		t = whell.read()  # Read the value from pin 0
		if not t:  # Set a default if no value read
			t = 0
		else:
			t *= multiplier 
		t=int((t/100)*180)
		t = 'turn :'+str(t) 
		
		####################################################################
		a = accelerator.read()  # Read the value from pin 1
		if not a:  # Set a default if no value read
			a = 0
		else:
			a *= multiplier
			a = int((a*100)/8  )
		a = ' accelerator :'+str(a) 
		
		####################################################################
		b = brake.read()  # Read the value from pin 2
		if not b:  # Set a default if no value read
			b = 0
		else:
			b *= multiplier
			b = int((b*100)/20)
		b = ' brake : '+str(b) 
		
			
		####################################################################
		gear_p = P.read()
		
		
		gear_r = R.read()
		
		gear_n = N.read() # Read if the button has been pressed.
		
		gear_d = D.read()
	  # 	if not gear_d:  # Set a default if no value read
			# gear_d = 0

		global gear
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
		gear = ' gear : ' + str(gear)
		# ######################################################################
		
		
		print  a + b + t + gear
		
except KeyboardInterrupt:
	board.exit()
	os._exit()
	