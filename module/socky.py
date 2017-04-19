# import server_pc 
import socket 
import Queue
import threading
import time
import sets 
import logging
import constrant

"""
System status
"""
SYSTEM_STATUS = 0 

"""
Car Status
"""
CURRENT_SPEED = 0
CURRENT_GEAR = "N"
CURRENT_WHEEL_ANGLES = 0


"""

"""
ACCELATOR = 0

"""
Static Value
"""
DEFALUT_SPEED = 0
DEFALUT_GEAR = "N"

"""
Queue of order from data reciever
"""
TASK_QUEUE = Queue.Queue() 

"""
Phone Object socket
"""
PHONE_DRIVER = None
PHONE_CMD = None
"""
Driving SIMULATOR set Object socket
"""
SIMULATOR_SET_DRIVER = None
SIMULATOR_SET_CMD = None

"""
Current Driver Object socket 
"""
DRIVER = None

""" 
Determine 
0 = PH Control
1 = SIM Control
None = No Client 
"""
CONTROL_MODE = None

CLIENT_WHITELIST = sets.Set()

HOST = constrant.HOST

"""
Command Server
"""

logging.basicConfig(level=logging.DEBUG)

def commandSocket():
	command_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	command_sock.bind((HOST, 7769))
	command_sock.listen(3)

	while True:
		conn, addr = command_sock.accept()
		logging.debug( "Command socket connect from %r", addr)
		socketAuthenticate(conn,addr)

def commandSocketReceiver(conn, addr):
	try:
		while True:
			raw_data = conn.recv(1024)
			command(raw_data)
	except Exception as e:
		logging.debug("Command socket disconnected from %r %r", addr, e)
		
def socketResponse(conn, message):
	try:
		conn.send(message)
	except Exception as e:
		logging.debug("Command response Failed %r",e)

"""
Driver Control Socket
"""
def DriverControlSocket():
	global CONTROL_MODE, PHONE_DRIVER, CONTROL_MODE, SIMULATOR_SET_DRIVER, PHONE_DRIVER
	driver_control_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	driver_control_sock.bind((HOST, 7789))
	driver_control_sock.listen(3)

	try :

		while True:
			conn, addr = driver_control_sock.accept()
			logging.debug( "Driver socket connect from %r", addr)
			id_mess = conn.recv(1024)
			print id_mess

			if id_mess == "PHONE":
				PHONE_DRIVER = DeviceSocket(conn, "PHONE")
				PHONE_DRIVER.getEvent().set()
				PHONE_DRIVER.start()

				CONTROL_MODE = 0

			elif id_mess == "SIMULATOR_SET":
				SIMULATOR_SET_DRIVER = DeviceSocket(conn, "SIMULATOR_SET")	

				if PHONE_DRIVER == None:
					SIMULATOR_SET_DRIVER.getEvent().set()
					CONTROL_MODE = 1

				else:
					SIMULATOR_SET_DRIVER.getEvent().clear()

				SIMULATOR_SET_DRIVER.start()

			else:
				logging.debug( "Driver socket disconnect from %r", addr)
				# conn.close()
	except Exception as e :
		raise e

def command(message):
	command = message.split()[0] 

	if command == '-cg':
		changeGear(message.split()[1] )

	if command == '-cm':
		changeControlmode(message.split()[1])

def changeControlmode(cmd):
	global CONTROL_MODE, PHONE_DRIVER, CONTROL_MODE, SIMULATOR_SET_DRIVER

	print cmd 
	if cmd == "phone" and CONTROL_MODE != 0 and PHONE_DRIVER != None:
		CONTROL_MODE = 0
		SIMULATOR_SET_DRIVER.getEvent().clear()
		PHONE_DRIVER.getEvent().set()
		print "Change control mode to", cmd

	elif cmd == "sim" and SIMULATOR_SET_DRIVER != None:
		CONTROL_MODE = 1
		SIMULATOR_SET_DRIVER.getEvent().set()
		PHONE_DRIVER.getEvent().clear()

		print "Change control mode to", cmd

	else :
		print "Control mode not change"

	
def commandSend(conn):
	while True:
		inp = raw_input("_>")
		conn.send(inp)

def socketAuthenticate(conn, addr):
	global PHONE_CMD, SIMULATOR_SET_CMD
	conn.sendall("-sq Who're you")
	auth_data = conn.recv(1024)
	logging.debug("Auth message %r", auth_data)

	if auth_data == "-a PHONE":
		PHONE_CMD = conn
		logging.debug("Socket Auth %r %r", addr, "PHONE")

		threading.Thread(target=commandSocketReceiver, args=(conn, addr)).start()
		conn.send("test")
		threading.Thread(target=commandSend, args=(conn,)).start()

	elif auth_data == "-a SIMULATOR_SET" :
		SIMULATOR_SET_CMD = conn

	else:
		conn.close()
		print addr," connection failed to Authenticate"
		
def Driving():
	if DRIVER != None :
		new_thread = threading.Thread(name="Driver", target=MotorControl)
		THREAD_POOL.append(new_thread)
	else:
		CURRENT_SPEED = DEFALUT_SPEED 

"""
Set Current Speed 
"""
def CurrentSpeedControl(driver):

	global CURRENT_SPEED
	global CONTROL_MODE
	global TASK_QUEUE

	try:
		while True:
			data = driver.recv(128)
			print data
	except:
		print "something is wrong"

"""
Command Motor By CURRENT_SPEED
"""
def MotorController():
	global ACCELATOR
	while True:
		time.sleep(0.3)
		# print ACCELATOR

def ServoController():
	global CURRENT_WHEEL_ANGLES
	while True:
		time.sleep(0.3)
		# print ACCELATOR

def DriverController():
	global CONTROL_MODE, DRIVER
	if CONTROL_MODE == 1:
		if DRIVER != None and SIMULATOR_SET.is_connect :
			SIMULATOR_SET.stop()
		PHONE.start()

def SystemCommand(command):
	global SYSTEM_STATUS
	if command == "shutdown":
		SYSTEM_STATUS = 0

	elif command == "start":
		SYSTEM_STATUS =1
	else:
		pass

"""
@param
String head
Integer value

Use tasking low-level devices 
"""
def changeGear(value):
	global CURRENT_GEAR, PHONE_CMD
	if CURRENT_GEAR != value :
		CURRENT_GEAR = value
		response_message = "-cg "+value
		socketResponse(PHONE_CMD, response_message)
		print "Change gear to ", value

def assignTask(head, value):
	control_head = ['a','t','b']
	if head in control_head:
		TASK_QUEUE.put(head+value)
	elif head == 'g' :
		changeGear(value)

def decode(income_data):
	__header = ['a','b','t','g']
	block_head = ""
	block_value = ""

	lenght = len(income_data)

	for i in range(lenght):
		if income_data[i] in __header  :
			if block_head != "" and block_value != "":
				assignTask(block_head, block_value)
				# print block_head, block_value

				block_head = income_data[i]
				block_value = ""

			else:
				block_head = income_data[i]
				block_value = ""	

		else:
			block_value += income_data[i]



		if i == lenght-1 :
			assignTask(block_head, block_value)
			# print block_head, block_value


if __name__ == '__main__':
	print "Start Server !! "

	SystemCommand("start")

	# Event 
	# phone_event = threading.Event()
	# SIM_event = threading.Event()

	# Socket Part
	main_socket_thread = threading.Thread(name="Main_Socket_Thread", target=commandSocket)
	main_socket_thread.setDaemon(True)


	driver_control_socket_thread = threading.Thread(name="Driver_Control_Socket_Thread", target=DriverControlSocket)
	driver_control_socket_thread.setDaemon(True)

	main_socket_thread.start()
	driver_control_socket_thread.start()

	# Car System Part
	car_sys_motor_driven_thread = threading.Thread(name="Car_System_Motor_Driven", target=MotorController)
	car_sys_servo_driven_thread = threading.Thread(name="Car_System_Servo_Driven", target=ServoController)
	# car_sys_gear_control_thread = threading.Thread("Car_System_Gear_Control", target=GeearController)

	car_sys_motor_driven_thread.start()
	car_sys_servo_driven_thread.start()


class DeviceSocket(threading.Thread):
	

	def __init__(self, conn, name, event=threading.Event()):
		threading.Thread.__init__(self)
		self._name = name

		self.driver_sock = conn
		self.driver_event = threading.Event()

	def handleCommandSocket():
		while True:
			cmd = self.command_sock.recv(1024)
			commandRequest(command_sock, cmd)

	def setDriverEvent(self, event):
		self.driver_event = event

	def getEvent(self):
		return self.driver_event

	def setCommandSocket(conn, id_code):
		self.command_sock = conn, code

	def commandSocket():
		return self.command_sock

	def setDriverSocket(conn):
		self.driver_sock = conn

	def driverSocket(self):
		return self.driver_sock

	def setId(self, Id):
		self._Id = Id

	def getId(self):
		return self._Id

	def getName(self):
		return self._name

	def run(self):
		print "starting with ", self._name
		try:
			while True:
				self.driver_event.wait()
				raw_data = self.driver_sock.recv(1024)
				# Log data recv
				logging.debug("Driver Socket Receive data from %r -> %r", self.getName(), raw_data)

				# decode(raw_data)
		except Exception as e:

			print "Disconenct by", self.getName(), e



