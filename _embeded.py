from pyfirmata import Arduino, util
from pyfirmata import INPUT, OUTPUT, PWM, SERVO

from _global import *

board = Arduino('/dev/ttyS0') #firmataCommunicate
board.digital[3].mode = PWM #forward Pin
board.digital[5].mode = PWM #revers Pin
board.digital[12].mode = SERVO #servo Pin
board.digital[12].write(100) # defult Degree


"""
Command Motor By CURRENT_SPEED
"""
def MotorController():
	global CURRENT_GEAR,CURRENT_SPEED
	MaxSpeed = 160.0

	pwmStartRun = 0.20 #Motor begin run
	pwmMaxRun = 0.60
	pwmRange = pwmMaxRun - pwmStartRun

	while True:
		t1 = time.time()
		
		if CURRENT_GEAR == 'D':
			if CURRENT_SPEED == 0:
				board.digital[3].write(0)
			else:

				pwmForword = (CURRENT_SPEED/MaxSpeed * pwmRange) + pwmStartRun
				board.digital[3].write(pwmForword)

		elif CURRENT_GEAR == 'R':
			if CURRENT_SPEED == 0:
				board.digital[5].write(0)
			else:
				pwmReverse= (CURRENT_SPEED/MaxSpeed * pwmRange) + pwmStartRun
				board.digital[5].write(pwmReverse)
			

		elif CURRENT_GEAR == 'P':
			
			board.digital[3].write(0.02)
			

		elif CURRENT_GEAR == 'N':

			board.digital[3].write(0)
		#t2 = time.time()

		# print "time used ", t2-t1

"""
Command Servo By CURRENT_WHEEL_ANGLES
"""
def ServoController():
	global CURRENT_WHEEL_ANGLES
	while True:
		
		left = 75 											#left max degree
		right = 125 										#right max degree
		carDegree = left+(((right-left)*CURRENT_WHEEL_ANGLES)/180)		#cal degree servo
		board.digital[12].write(carDegree)	