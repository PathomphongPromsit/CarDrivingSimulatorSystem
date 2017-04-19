import socket 
import Queue
import threading
import time
import sets 
import logging

import sys
import struct

from pyfirmata import Arduino, util
from pyfirmata import INPUT, OUTPUT, PWM, SERVO
from time import sleep


board = Arduino('/dev/ttyS0') #firmataCommunicate

board.digital[12].mode = SERVO #servo Pin
board.digital[12].write(90) # defult Degree
while True:
	inp = raw_input("_>")
			
	board.digital[12].write(inp)
		



			
			