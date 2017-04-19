import socket
import sys
import struct
import Queue

from pyfirmata import Arduino, util
from pyfirmata import INPUT, OUTPUT, PWM, SERVO
from time import sleep

board = Arduino('/dev/ttyS0')
board.digital[3].mode = PWM #forward
board.digital[5].mode = PWM #revers

board.digital[12].mode = SERVO
board.digital[12].write(90)


global accelerator,brake,gear,forwardSpeed,reverseSpeed,forwardPWM,reversePWM,Q
accelerator = 0.0
brake = 0.0
gear = 'd'
forwardSpeed = 0.0
reverseSpeed = 0.0
forwardPWM = 0.0
reversePWM = 0.0

Q = Queue.Queue()



########################################################
def decodePutQ(param):
	global Q
	in_head = ''
	in_data = ''

	decode = ""
	__header__ = ['a','b','t','g']

	_len = len(param)

	if( _len <= 4):

		for h in range( _len ):

			if param[h] in __header__ :
				#print 'decode :'+in_head +in_data
				
				#in_data = '' #setdatanull
				in_head = param[h] #sethead
				
			else:
				in_data = in_data+param[h]	
				if h == _len-1:
					Q.put(in_head+in_data)

					#sprit(in_head,in_data)
					#print 'decode:' +in_head +in_data
				## decode done

	else: 
	
		for h in range( _len ):
			#print param[h]
			if (param[h] in __header__ ) & (in_data != ''):
				

				Q.put(in_head+in_data)
				
				#sprit(in_head,in_data)
			
			elif param[h] in __header__:
				#print 'decode :'+in_head +in_data
				in_data = '' #setdatanull
				in_head = param[h] #sethead
				
			else:
				in_data = in_data+param[h]	





#######################################################
def decodegetQ(param):
	
	in_head = ''
	in_data = ''

	decode = ""
	__header__ = ['a','b','t','g']

	_len = len(param)

	if( _len <= 4):

		for h in range( _len ):

			if param[h] in __header__ :
				#print 'decode :'+in_head +in_data
				
				#in_data = '' #setdatanull
				in_head = param[h] #sethead
				
			else:
				in_data = in_data+param[h]	
				if h == _len-1:
					

					sprit(in_head,in_data)
					#print 'decode:' +in_head +in_data
				## decode done

	else: 
	
		for h in range( _len ):
			#print param[h]
			if (param[h] in __header__ ) & (in_data != ''):
				

				
				
				sprit(in_head,in_data)
			
			elif param[h] in __header__:
				#print 'decode :'+in_head +in_data
				in_data = '' #setdatanull
				in_head = param[h] #sethead
				
			else:
				in_data = in_data+param[h]	

###########################################################################################



def sprit (in_head,in_data):
	
	if in_head == 'a':
		a = float(in_data)
		#calDegree_180(a)
		#input_status(in_head,a)
		global accelerator
		accelerator= a
		#print a


	elif in_head == 'b':
		b = float(in_data)
		#input_status(in_head,b)
		global brake
		brake = b
	
	elif in_head == 't':
		t = int(in_data)
		#print ' spritT' + t
		calDegree_to_car(t) #TestMobileClient0-180
	
	elif in_head == 'g':
		g= str(in_data)
		global gear
		gear = g
		#input_status(in_head,g)




##################Turn##########################################################
###########Turn#############Turn################################################
def calDegree_180(turnPercen):
	degree=(turnPercen*180)/100
	calDegree_to_car(degree)
	
def calDegree_to_car(degree180):
	left = 65
	right = 115
	carDegree = left+(((right-left)*degree180)/180)
	print carDegree

	board.digital[12].write(carDegree)

#############################################################################
##################RUN####RUN###RUN#####RUN###################################

def MoterControl(accelerator,brake,gear):
	
	if gear == 'd':
		gearD(accelerator,brake)
		
	elif gear == 'r':
		gearR(accelerator,brake)
	elif gear == 'p':
		gearP(accelerator,brake)
	elif gear == 'n':
		gearN(accelerator,brake)
	
	global decreaseSpeed
	decreaseSpeed=5.0
	global forwardMaxSpeed 
	forwardMaxSpeed= 100.0
	global reverseMaxSpeed 
	reverseMaxSpeed= 30.0
	global motorPeriod 
	motorPeriod= 1.000
	


def gearD(accelerator,brake):

	defaultSpeed = 5.0
	decreaseSpeed = 0.5
	forwardMaxSpeed = 120.0
	global forwardSpeed

	
	accelerator_percent = accelerator/100
	brake_percent = brake/100
	brake_percent
	
	if forwardSpeed == 0 and accelerator == 0 and brake != 0: #unAcc+brake
		
		forwardSpeed = 0
		
	elif forwardSpeed == 0 and accelerator == 0 and brake == 0:#unAcc+unBrake
		forwardSpeed = defaultSpeed
	
	
	else:
		
		forwardSpeed = forwardSpeed + accelerator_percent - brake_percent- decreaseSpeed
		if forwardSpeed > forwardMaxSpeed:
			forwardSpeed = forwardMaxSpeed
		elif forwardSpeed <= defaultSpeed and brake == 0:
			forwardSpeed = defaultSpeed
		elif forwardSpeed < 0:
			forwardSpeed = 0


	

def gearR(accelerator,brake):
	defaultSpeed = 5.0
	decreaseSpeed = 0.5
	reverseMaxSpeed = 40.0
	global reverseSpeed
	
	accelerator_percent = accelerator/100
	brake_percent = brake/100
	brake_percent
	
	if reverseSpeed == 0 and accelerator == 0 and brake != 0: #unAcc+brake
		
		reverseSpeed = 0
		
	elif reverseSpeed == 0 and accelerator == 0 and brake == 0:#unAcc+unBrake
		reverseSpeed = defaultSpeed
	
	
	else:
		
		reverseSpeed = reverseSpeed + accelerator_percent - brake_percent- decreaseSpeed
		if reverseSpeed > reverseMaxSpeed:
			reverseSpeed = reverseMaxSpeed
		elif reverseSpeed <= defaultSpeed and brake == 0:
			reverseSpeed = defaultSpeed
		elif reverseSpeed < 0:
			reverseSpeed = 0

def driveD(forwardSpeed):
	
	
	if forwardSpeed < 5:
		pwmForword = 0.0
	else:
		pwmForword= 0.2+((0.8/120)*forwardSpeed)
	print pwmForword
	
	board.digital[3].write(pwmForword)

def driveR(reverseSpeed):
	
	if reverseSpeed < 5:

		pwmReverse = 0.0
	else:
		pwmReverse= 0.2+((0.8/120)*reverseSpeed)
	
	
	board.digital[5].write(pwmReverse)
	

def gearP():
	
	
	board.digital[9].write(0.1)
	

def gearN():
	
	
	board.digital[9].write(0)
##############################################################################


def testq():

	global Q

	while not Q.empty():
	    decodegetQ(Q.get())
	    MoterControl(accelerator,brake,gear)
	    driveD(forwardSpeed)

decodePutQ('a90a90a90a90a90a90a90a90a90a90a90a90a90a90a90a90a90a90a90a90a90a90a90a90a90a90a90a90a90a90a90a90a90a90a90a90a90a90a90a90a90a90a90a90a90a90a90a90a90a90a90a90')
testq()





