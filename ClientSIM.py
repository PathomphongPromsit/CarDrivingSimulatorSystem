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


IP = "192.168.100.1"
PORT1 = 7769
PORT2 = 7789

auth_message = "-a SIMULATOR_SET"








def driverSocketResponse():
	global DRIVER_SERVER
	while True:
		raw_data = DRIVER_SERVER.recv(1024)
		print raw_data

def commandSocketResponse():
	global COMMAND_SERVER
	while True:
		raw_data = COMMAND_SERVER.recv(1024)
		print raw_data


def readWheell():
	global DRIVER_SERVER
	while True:
		t = whell.read()  # Read the value from pin 0
		global CURRENT_WHEEL_ANGLES
		
		if not t:  # Set a default if no value read
			CURRENT_WHEEL_ANGLES = 0
			data = 't' + str(CURRENT_WHEEL_ANGLES)
			DRIVER_SERVER.send(data)
		else:
			t *= 100
			t=int((t/100)*180)
			if t != CURRENT_WHEEL_ANGLES:
				CURRENT_WHEEL_ANGLES = a
				data = 't' + str(CURRENT_WHEEL_ANGLES)
				DRIVER_SERVER.send(data)
	
	
def readAccelerator():
	global DRIVER_SERVER
	while True:
		a = accelerator.read()  # Read the value from pin 1
		global ACCELERATOR
		
		if not a:  # Set a default if no value read
			ACCELERATOR = 0
			data = 'a' + str(ACCELERATOR)
			DRIVER_SERVER.send(data)
		else:
			a *= 100
			a = int((a*100)/8)
			if a != ACCELERATOR:
				ACCELERATOR = a
				data = 'a' + str(ACCELERATOR)
				DRIVER_SERVER.send(data)
	
	
def readBrake():
	global DRIVER_SERVER
	while True:
		b = brake.read()  # Read the value from pin 2
		global BRAKE
		
		if not b:  # Set a default if no value read
			BRAKE = 0
			data = 'b' + str(BRAKE)
			DRIVER_SERVER.send(data)
		else:
			b *= 100
			b = int((b*100)/20)
			if b != BRAKE:
				BRAKE = b
				data = 'b' + str(BRAKE)
				DRIVER_SERVER.send(data)

def readGear():	# Read if the button has been pressed.
	global COMMAND_SERVER
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
			COMMAND_SERVER.send(data)
		elif gear_r == True and GEAR != 'R':
			GEAR = 'R'
			data = '-cg ' + str(GEAR)
			COMMAND_SERVER.send(data)
		elif gear_n == True and GEAR != 'N':
			GEAR = 'N'
			data = '-cg ' + str(GEAR)
			COMMAND_SERVER.send(data)
		elif gear_d == True and GEAR != 'D':
			GEAR = 'D'
			data = '-cg ' + str(GEAR)
			COMMAND_SERVER.send(data)



if __name__ == '__main__':
	print "Start Server !! "


	COMMAND_SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	COMMAND_SERVER.connect((IP, PORT1))
	COMMAND_SERVER.send(auth_message)

	DRIVER_SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	DRIVER_SERVER.connect((IP, PORT2))	
	#read and sent
	Read_Wheell_thread = threading.Thread(name = "Read_Wheel", target =readWheell)
	Read_Accelerator_thread = threading.Thread(name = "Read_Accelerator", target = readAccelerator)
	Read_Brake_thread = threading.Thread(name = "Read_Brake", target=readBrake)
	Read_Gear_thread = threading.Thread(name = "Read_Gear", target =readGear)

	Read_Wheell_thread.start()
	Read_Accelerator_thread.start()
	Read_Brake_thread.start()
	Read_Gear_thread.start()


	#monitor
	Monitor_Driver_thread = threading.Thread(target = driverSocketResponse)
	Monitor_Command_thread = threading.Thread(target = commandSocketResponse)
	Monitor_Driver_thread.start()
	Monitor_Command_thread.start()
