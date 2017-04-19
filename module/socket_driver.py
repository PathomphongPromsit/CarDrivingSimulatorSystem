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
