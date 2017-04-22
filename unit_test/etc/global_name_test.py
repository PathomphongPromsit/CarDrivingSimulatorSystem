from const import *

def test():
	global TEST, TEST2
	TEST = 1
	TEST2 = 2

if __name__ == '__main__':
	global TEST1

	print TEST1

	TEST1 = 2

	print TEST1