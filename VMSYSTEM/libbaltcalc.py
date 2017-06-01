#!/usr/bin/env python

#v3.0.0

def numflip(numtoflip):
	return(numtoflip[::-1])

#converts balanced ternary integers to decimal.
#this is a core function to the library.
def BTTODEC(NUMTOCONV1):
	FLIPPEDSTR1=(numflip(NUMTOCONV1))
	EXTRAP1=0
	SUMDEC1=0
	for btnumlst1 in FLIPPEDSTR1:
		EXTPOLL1 = (3**EXTRAP1)
		if btnumlst1==("+"):
			SUMDEC1 += EXTPOLL1
		if btnumlst1==("-"):
			SUMDEC1 -= EXTPOLL1
		EXTRAP1 += 1
	return (SUMDEC1)

#converts decimal integers to balanced ternary.
#this is a core function to the library.
def DECTOBT(NUMTOCONV1):
	digbat=""
	while NUMTOCONV1 != 0:
		if NUMTOCONV1 % 3 == 0:
			#note_digit(0)
			digbat=("0" + digbat)
		elif NUMTOCONV1 % 3 == 1:
			#note_digit(1)
			digbat=("+" + digbat)
		elif NUMTOCONV1 % 3 == 2:
			#note_digit(-1)
			digbat=("-" + digbat)
		NUMTOCONV1 = (NUMTOCONV1 + 1) // 3
	#print NUMTOCONV1
	#zero exception
	if (str(digbat)==""):
		digbat="0"
	return(digbat)
	

def btmul(numA, numB):
	numAcon=BTTODEC(numA)
	numBcon=BTTODEC(numB)
	decRes=(numAcon * numBcon)
	btRes=(DECTOBT(decRes))
	return(btRes)

def btadd(numA, numB):
	numAcon=BTTODEC(numA)
	numBcon=BTTODEC(numB)
	decRes=(numAcon + numBcon)
	btRes=(DECTOBT(decRes))
	return(btRes)

def btsub(numA, numB):
	numAcon=BTTODEC(numA)
	numBcon=BTTODEC(numB)
	decRes=(numAcon - numBcon)
	btRes=(DECTOBT(decRes))
	return(btRes)

#note that values may not be exact. this is due to that the libbaltcalc currently handles integers only.

def btdivcpu(numA, numB):
	numAcon=BTTODEC(numA)
	numBcon=BTTODEC(numB)
	try:
		decRes=(numAcon // numBcon)
	except ZeroDivisionError:
		#Special zero divisoon return for SBTCVM to detect. "ZDIV"
		return "ZDIV"
	btRes=(DECTOBT(decRes))
	return(btRes)
	
def btdiv(numA, numB):
	numAcon=BTTODEC(numA)
	numBcon=BTTODEC(numB)
	decRes=(numAcon // numBcon)
	btRes=(DECTOBT(decRes))
	return(btRes)

def btdivclass(numA, numB):
	numAcon=BTTODEC(numA)
	numBcon=BTTODEC(numB)
	decRes=(numAcon // numBcon)
	btRes=(DECTOBT(decRes))
	return(btRes)
btdev=btdiv

def mpi(tritlen):
	return (((3**(tritlen))-1)//2)
def mni(tritlen):
	return ( - ((3**(tritlen))-1)//2)
def mcv(tritlen):
	return (3**(tritlen))
	


#inverts the positive and negative numerals in a balanced ternary integer, 
#(ie 1T0T would become T101 and vice versa)
def BTINVERT(numtoinvert):
	BTINV1 = numtoinvert.replace("-", "P").replace("+", "-").replace("P", "+")
	#print BTINV2
	return (BTINV1)

def trailzerostrip(numtostri):
	pritokfg=0
	#print ("argh -.-" + numtostri)
	numtostri = numtostri.replace("-", "T").replace("+", "1")
	#numtostri = (numflip(numtostri))
	numretbankd=""
	#print (numtostri)
	allzero=1
	for fnumt in numtostri:
		if (fnumt=="T" or fnumt=="1"):
			pritokfg=1
			allzero=0
		if pritokfg==1:
			numretbankd = (numretbankd + fnumt)
		if pritokfg==0:
			nullbox=fnumt
		#print (fnumt)
	if allzero==1:
		numretbankd="0"
	numretbankd = numretbankd
	#print (numretbankd.replace("T", "-").replace("1", "+"))
	return (numretbankd.replace("T", "-").replace("1", "+"))


# a "programmable" biased and gate. returns a positive if:
#input a (inpA) = input b (inpB) = polarity line (polarset)
#else it returns zero
def progbiasand(polarset, inpA, inpB):
	if (inpA==polarset and inpB==polarset):
		return("+")
	elif (inpA!=polarset or inpB!=polarset):
		return("0")
#a polarized and gate
#returns + if both input A (inpA) and input B (inpB) = + 
#returns - if both input A (inpA) and input B (inpB) = -
#otherwise it returns zero
def polarityand(inpA, inpB):
	if (inpA=="+" and inpB=="+"):
		return("+")
	elif (inpA=="-" and inpB=="-"):
		return("-")
	elif (inpA!="+" or inpB!="+"):
		return("0")
	elif (inpA!="-" or inpB!="-"):
		return("0")

# a programmable biased or gate returns "+" if either or both inputs equal the pollarity line (polarset)
#else it returns "0"
def progbiasor(polarset, inpA, inpB):
	if (inpA==polarset or inpB==polarset):
		return("+")
	elif (inpA!=polarset or inpB!=polarset):
		return("0")
# a programmable biased orn gate returns "+" if either  equal the pollarity line (polarset)
#returns "0" either if neither or both inputs equal the pollarity line (polarset)
def progbiasnor(polarset, inpA, inpB):
	if (inpA==polarset and inpB==polarset):
		return("0")
	elif (inpA!=polarset and inpB==polarset):
		return("+")
	elif (inpA==polarset and inpB!=polarset):
		return("+")
	elif (inpA!=polarset and inpB!=polarset):
		return("0")

class btint:
	def __init__(self, stringint):
		#store integer in signed decimal integer.
		if type(stringint) is int:
			self.intval=stringint
		else:
			try:
				self.intval=stringint.dec()
			except AttributeError:
				self.intval=BTTODEC(str(stringint))
	def __str__(self):
		return DECTOBT(self.intval)
	def __int__(self):
		return self.intval
	def dec(self):
		return self.intval
	def bt(self):
		return DECTOBT(self.intval)
	#addition
	def __add__(self, other):
		return btint((self.dec() + other.dec()))
	#subtraction
	def __sub__(self, other):
		return btint((self.dec() - other.dec()))
	#division
	def __truediv__(self, other):
		return btint((self.dec() // other.dec()))
	def __div__(self, other):
		return btint((self.dec() // other.dec()))
	def __floordiv__(self, other):
		return btint((self.dec() // other.dec()))
	#multiplication
	def __mul__(self, other):
		return btint((self.dec() * other.dec()))
	#others
	def __abs__(self):
		return btint(abs(self.intval))
	def __neg__(self):
		return btint( - self.intval)
	def __pos__(self):
		return btint( + self.intval)
	def __invert__(self):
		return btint(BTINVERT(DECTOBT(self.intval)))
	def invert(self):
		return btint(BTINVERT(DECTOBT(self.intval)))