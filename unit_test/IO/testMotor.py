from pyfirmata import Arduino, util
from pyfirmata import INPUT, OUTPUT, PWM, SERVO
from time import sleep
import time






board = Arduino('/dev/ttyS0') #firmataCommunicate
board.digital[3].mode = PWM #forward Pin

while True:
	inp = raw_input("_>")
			
	board.digital[3].write(inp)
		





