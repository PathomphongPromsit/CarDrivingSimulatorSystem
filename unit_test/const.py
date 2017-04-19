class Test(object):
	"""docstring for Test"""
	def __init__(self, arg):
		super(Test, self).__init__()
		self.arg = arg

	def prints(self):
		global VAL

		print VAL