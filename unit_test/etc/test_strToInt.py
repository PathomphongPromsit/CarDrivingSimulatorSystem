def test(arg):
	try:
		int(arg)
		print arg
	except :
		pass



if __name__ == '__main__':
	test("0123")
	test("nuull")