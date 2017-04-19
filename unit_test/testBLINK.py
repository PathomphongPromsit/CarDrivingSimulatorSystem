from pyfirmata import Arduino, util
from time import sleep
 
board = Arduino('/dev/ttyS0')
print "car driving simmulator"
from pyfirmata import INPUT, OUTPUT, PWM, SERVO
from time import sleep
board = Arduino('/dev/ttyS0')

board.digital[13].mode = OUTPUT
while True:
	
	board.digital[13].write(1)
	sleep(1)
	board.digital[13].write(0)
	sleep(1)