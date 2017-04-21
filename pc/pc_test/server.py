import socket ,sys, os
import threading
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import constrant
import logging

logging.basicConfig(level=logging.DEBUG)

HOST = constrant.HOST

def s1():
	driver_control_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	driver_control_sock.bind((HOST, 7789))
	driver_control_sock.listen(3)
	conn, addr = driver_control_sock.accept()

	try :

		while True:
			logging.debug( "Driver socket connect from %r", addr)
			id_mess = conn.recv(1024)
			print id_mess
	except Exception as e:
		raise e 
def s2():
	driver_control_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	driver_control_sock.bind((HOST, 7769))
	driver_control_sock.listen(3)
	conn, addr = driver_control_sock.accept()

	try :

		while True:
			logging.debug( "CMD socket connect from %r", addr)
			id_mess = conn.recv(1024)
			print id_mess
	except Exception as e:
		raise e 


if __name__ == '__main__':
	

	print "START"

	t1 = threading.Thread(target=s1)
	t2 = threading.Thread(target=s2)
	t1.start()
	t2.start()