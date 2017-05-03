from pyfirmata import Arduino, util
from pyfirmata import INPUT, OUTPUT, PWM, SERVO

from _global import *

board = Arduino('/dev/ttyS0') #firmataCommunicate
board.digital[3].mode = PWM #forward Pin
board.digital[5].mode = PWM #revers Pin
board.digital[12].mode = SERVO #servo Pin
board.digital[12].write(100) # defult Degree

board.digital[10].mode = SERVO #cam Pin
board.digital[10].write(90) #
