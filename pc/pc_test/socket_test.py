import threading
import time
import Queue
import sys 
import socket

def p(queue):
	i=0
	while True and i<500:
		i = i+1
		queue.put(i)		

# def g(queue):
# 	while True:
# 		if not q.Empty():
# 			print queue.get()


if __name__ == '__main__':
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(("192.168.137.1", 7769))

	
