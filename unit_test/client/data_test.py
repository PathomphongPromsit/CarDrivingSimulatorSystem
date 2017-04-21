import random 

HEADER = ['a','b','t','g']
def random_generator(n = 100):
	__header__ = ['a','b','t']
	__list__ = ""

	n = int(n)
	if(n == 0):
		n = random.randint(1, 100)

	for i in range( n ):

		head = random.choice(__header__)
		value = random.randint(0,100)	
		__list__ += head+str(value)

	return __list__

def decoder(pair):
	global HEADER 
	block_head = ""
	block_value = ""

	lenght = len(pair)

	for i in range(lenght):
		if pair[i] in HEADER  :
			if block_head != "":
				
				taskManager(block_head, block_value)
				block_head = pair[i]
				block_value = ""

			else:
				block_head = pair[i]
				block_value = ""	

		else:
			block_value += pair[i]

		if i == lenght-1 :

			taskManager(block_head, block_value)


def acceletor_limitation_generater(start=0, end=100, distribute=1):
	pair = ""
	start = int(start)
	end = int(end)
	distribute = int(distribute)

	_list = [mem for mem in range(start, end) ]

	for i in range(start, end+1):
		for j in range( random.randint(1,distribute)):
			pair += 'a'+str(i)
	return pair

def rotation_sloper_test(start=0, end=180, distribute=1):
	pair = ""
	start = int(start)
	end = int(end)
	distribute = int(distribute)
	_list = [mem for mem in range(int(start), int(end)) ]

	for i in range(start, end+1):
		for j in range( random.randint(1,distribute)):
			pair += 't'+str(i)
	return pair

def taskManager(head, value):
	if head != "" and value != "":
		if head == 'a':
			print "order Accelator : ", value
		elif head == 'b':
			print "order Brake : ", value
		
		elif head == 't':
			print "order Rotation : ", value
		
		elif head == 'g':
			print "order Gear : ", value
		else:
			print "None Head"
	else:
		print "None Head or Value "


if __name__ == '__main__':

	datapair = acceletor_limitation_generater(20,80,3)
	print datapair
	decoder(datapair)
