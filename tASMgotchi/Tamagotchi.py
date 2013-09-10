def process(file):
	ifile = open(file[1], 'r').readlines()
	file.remove(file[1])
	i = 0
	tpl = open("template0.txt", 'rb').read()
	for item in ifile:
		s = convi(item.strip())
		
		tpl = tpl[:(0x60000 + i*0x100)] + s + tpl[(0x60000 + i*0x100 + len(s)):] 
		print i, 
		print item
		i = i + 2
	ft = open("template.txt", 'wb')
	ft.write(tpl)

	file2 = file[0]
	f = open(file2, 'r')
	l = f.readlines()
	addstart(l)
	port(l)
	addlcd(l)
	f.close()
	f = open("temporarycode.tmp", 'w')
	for item in l:
		f.write(item)
	f.close()
	file[0] = "temporarycode.tmp"

def addstart(l):
	l.insert(0, ".org $200\n")
def port(l):
	for i in range(0, len(l)):
		l[i] = l[i].replace("read_a", "$E209")

	

def addlcd(l):
	for i in range(0, len(l)):
		l[i] = l[i].replace("clear_lcd", "$E1EE")
	f = open("li.txt")
	l2 = f.readlines()
	l.append("\n")
	for item in l2:
		l.append(item)


def convi(path):


	s = ""
	tmp = 0
	rol = 0

	import Image

	im = Image.open(path)

	def tofourbit(a):
	#print a
		if ((a > -1) and (a < 1)):
			return 3;
		if ((a > 0) and (a < 8)):
			return 2;
		if ((a > 7) and (a < 10 )):
			return 1;
		if (a > 9):
			return 0;

	def conv(a):

		t = 0;
		t = t | (tofourbit(ord(a) & 0x0f) << 2)
		t = t | (tofourbit((ord(a) & 0xf0) >> 4))
		return t
	i = 0
	width = im.size[0]
	height = im.size[1]
	while ( i < (width * height) ):
		tmp = 0;
		if(1):
			for j in range(0, 4):
			
				tmp = tmp | tofourbit(im.getpixel(((i)%width, (i)/width)))
			
				i =  i + 1
				if j != 3:
					tmp = tmp * 4
				#print tmp
			

		#print tmp
		s = s + chr(tmp)
	
	return s
 

