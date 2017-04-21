import socket
import threading
import sys
import time

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

board.digital[13].mode = OUTPUT

CURRENT_GEAR = 'N'
CURRENT_WHEEL_ANGLES = 90
ACCELERATOR = 0
BRAKE = 0


IP = "192.168.100.1"
PORT1 = 7769
PORT2 = 7789


def readWheell():
	global DRIVER_SERVER, CURRENT_WHEEL_ANGLES
	minAnalog = 0
	maxAnalog = 1
	rangeAnalog = maxAnalog - minAnalog
	while True:
		angle = whell.read()
		if not angle:
			angle = 90
		else:
			angle = ((whell.read()-minAnalog)/rangeAnalog)*180  # Read % value from pin 0
			angle = int(angle) 
		
		if angle != CURRENT_WHEEL_ANGLES:
			if angle <=15 and CURRENT_WHEEL_ANGLE != 0:						#set 0
				CURRENT_WHEEL_ANGLES = 0
				data = 't' + str(CURRENT_WHEEL_ANGLES)
				print data
				DRIVER_SERVER.send(data)
			elif angle >15:
				CURRENT_WHEEL_ANGLES = angle
				data = 't' + str(CURRENT_WHEEL_ANGLES)
				print data
				DRIVER_SERVER.send(data)


			
			
		
	
def readAccelerator():
	global DRIVER_SERVER, ACCELERATOR
	minAnalog = 0.05
	maxAnalog = 0.095
	rangeAnalog = maxAnalog - minAnalog
	while True:
		acc = accelerator.read()  # Read the value from pin 2
		if not acc:  # Set a default if no value read
			acc = 0
		else:
			acc = ((accelerator.read()-minAnalog)/rangeAnalog)*100  # Read % value from pin 1
			acc = int(acc) 
		
		if acc != ACCELERATOR:
			if acc <=15 and ACCELERATOR !=0: 							#set 0
				ACCELERATOR = 0
				data = 'a' + str(ACCELERATOR)
				print data
				DRIVER_SERVER.send(data)
			elif acc >15:

				ACCELERATOR = acc
				data = 'a' + str(ACCELERATOR)
				print data
				DRIVER_SERVER.send(data)
		 
	
def readBrake():
	global DRIVER_SERVER, BRAKE
	minAnalog = 0.1
	maxAnalog = 0.18
	rangeAnalog = maxAnalog - minAnalog
	while True:
		brk = brake.read()
		if not brk:
			brk = 0
		else:

			brk = ((brake.read()-minAnalog)/rangeAnalog) *100 # Read % value from pin 2
			brk = int(brk) 
		
		if brk != BRAKE:
			if brk <= 15 and BRAKE != 0:
				BRAKE = 0
				data = 'b' + str(BRAKE)
				print data
				DRIVER_SERVER.send(data)
			elif brk >15:
				BRAKE = brk
				data = 'b' + str(BRAKE)
				print data
				DRIVER_SERVER.send(data)

def readGear():	# Read if the button has been pressed.
	global COMMAND_SERVER, CURRENT_GEAR
	while True:
		
		gear_p = P.read()
		gear_r = R.read()
		gear_n = N.read() 
		gear_d = D.read()
		
		#-cg
		
		if gear_p == True and CURRENT_GEAR != 'P':
			CURRENT_GEAR = 'P'
			data = '-cg ' + str(CURRENT_GEAR)
			print data
			COMMAND_SERVER.send(data)
		elif gear_r == True and CURRENT_GEAR != 'R':
			CURRENT_GEAR = 'R'
			data = '-cg ' + str(CURRENT_GEAR)
			print data
			COMMAND_SERVER.send(data)
		elif gear_n == True and CURRENT_GEAR != 'N':
			CURRENT_GEAR = 'N'
			data = '-cg ' + str(CURRENT_GEAR)
			print data
			COMMAND_SERVER.send(data)
		elif gear_d == True and CURRENT_GEAR != 'D':
			CURRENT_GEAR = 'D'
			data = '-cg ' + str(CURRENT_GEAR)
			print data
			COMMAND_SERVER.send(data)


# def driverSocketResponse():
# 	global DRIVER_SERVER
# 	while True:
# 		raw_data = DRIVER_SERVER.recv(1024)
# 		print raw_data

# def commandSocketResponse():
# 	global COMMAND_SERVER
# 	while True:
# 		raw_data = COMMAND_SERVER.recv(1024)
# 		print raw_data

if __name__ == '__main__':
	print "Start Server !! "
	# global IP, PORT1, PORT2, auth_message

	board.digital[13].write(1)
	sleep(1)
	board.digital[13].write(0)
	sleep(1)
	board.digital[13].write(1)
	sleep(1)
	board.digital[13].write(0)
	sleep(1)
	board.digital[13].write(1)
	sleep(1)
	board.digital[13].write(0)
	sleep(1)
	
	auth_message = "-a SIMULATOR_SET"
	device = "SIMULATOR_SET"
				
	COMMAND_SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	COMMAND_SERVER.connect((IP, PORT1))
	

	DRIVER_SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	DRIVER_SERVER.connect((IP, PORT2))

	COMMAND_SERVER.send(auth_message)	
	DRIVER_SERVER.send(device)

	time.sleep(1)

	#read and sent
	Read_Gear_thread = threading.Thread(name = "Read_Gear", target =readGear)
	Read_Accelerator_thread = threading.Thread(name = "Read_Accelerator", target = readAccelerator)
	Read_Brake_thread = threading.Thread(name = "Read_Brake", target=readBrake)
	# Read_Wheell_thread = threading.Thread(name = "Read_Wheel", target =readWheell)
	
	
	
	Read_Gear_thread.start()
	Read_Accelerator_thread.start()
	Read_Brake_thread.start()
	# Read_Wheell_thread.start()
	
	# #monitor
	# Monitor_Driver_thread = threading.Thread(target = driverSocketResponse)
	# Monitor_Command_thread = threading.Thread(target = commandSocketResponse)
	# Monitor_Driver_thread.start()
	# Monitor_Command_thread.start()