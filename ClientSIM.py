import socket
import threading
import sys

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

IP = "192.168.100.1"
PORT1 = 7769
PORT2 = 7789



command_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
command_server.connect((IP, PORT1))
auth_message = "-a SIMULATOR_SET"
command_server.send(auth_message)

driver_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
driver_server.connect((IP, PORT2))	


def driverSocketResponse():
		while True:
			raw_data = driver_server.recv(1024)
			print raw_data

def commandSocketResponse():

		while True:
			raw_data = command_server.recv(1024)
			print raw_data


def readWheell():
	while True:
		t = whell.read()  # Read the value from pin 0
		global CURRENT_WHEEL_ANGLES
		
		if not t:  # Set a default if no value read
			CURRENT_WHEEL_ANGLES = 0
			data = 't' + str(CURRENT_WHEEL_ANGLES)
			driver_server.send(data)
		else:
			t *= 100
			t=int((t/100)*180)
			if t != CURRENT_WHEEL_ANGLES:
				CURRENT_WHEEL_ANGLES = a
				data = 't' + str(CURRENT_WHEEL_ANGLES)
				driver_server.send(data)
	
	
def readAccelerator():
	while True:
		a = accelerator.read()  # Read the value from pin 1
		global ACCELERATOR
		
		if not a:  # Set a default if no value read
			ACCELERATOR = 0
			data = 'a' + str(ACCELERATOR)
			driver_server.send(data)
		else:
			a *= 100
			a = int((a*100)/8)
			if a != ACCELERATOR:
				ACCELERATOR = a
				data = 'a' + str(ACCELERATOR)
				driver_server.send(data)
	
	
def readBrake():
	while True:
		b = brake.read()  # Read the value from pin 2
		global BRAKE
		
		if not b:  # Set a default if no value read
			BRAKE = 0
			data = 'b' + str(BRAKE)
			driver_server.send(data)
		else:
			b *= 100
			b = int((b*100)/20)
			if b != BRAKE:
				BRAKE = b
				data = 'b' + str(BRAKE)
				driver_server.send(data)

def readGear():	# Read if the button has been pressed.
	while True:
		
		gear_p = P.read()
		gear_r = R.read()
		gear_n = N.read() 
		gear_d = D.read()
		global GEAR
		#-cg
		
		if gear_p == True and GEAR != 'P':
			GEAR = 'P'
			data = '-cg ' + str(GEAR)
			command_server.send(data)
		elif gear_r == True and GEAR != 'R':
			GEAR = 'R'
			data = '-cg ' + str(GEAR)
			command_server.send(data)
		elif gear_n == True and GEAR != 'N':
			GEAR = 'N'
			data = '-cg ' + str(GEAR)
			command_server.send(data)
		elif gear_d == True and GEAR != 'D':
			GEAR = 'D'
			data = '-cg ' + str(GEAR)
			command_server.send(data)
	
	