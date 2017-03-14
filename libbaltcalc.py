#!/usr/bin/env python
import math
#HELPTEXT = ('''commands:
#BTTODEC: convert a number into balancet
#''')
# syntax info:
#trit order is least signifigant digit on right
#1=+
#0=0
#T=-

def numflip(numtoflip):
	return(numtoflip[::-1])

#converts balanced ternary numbers to decimal.
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

#converts decimal numbers to balanced ternary.
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
def btdev(numA, numB):
	numAcon=BTTODEC(numA)
	numBcon=BTTODEC(numB)
	decRes=int(numAcon / numBcon)
	btRes=(DECTOBT(decRes))
	return(btRes)




#inverts the positive and negative numerals in a balanced ternary number, 
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




#prodotype addition function.
#preserved for its interesting logic
#eventually will add longer balanced ternary numbers.
def btaddreal(numA, numB):
	#check to ensure any final carries are preformed.
	numA=("E" + numA)
	numB=("E" + numB)
	numA=(numflip(numA))
	numB=(numflip(numB))
	numAcnt=0
	numBcnt=0
	curregA=1
	curregB=1
	carry="0"
	eotA=0
	eotB=0
	resbt=""
	for anA in numA:
		numAcnt += 1
	for anB in numB:
		numBcnt += 1
	if (numAcnt > numBcnt):
		forlist = numA
		overload=numAcnt
	if (numAcnt < numBcnt):
		forlist = numB
		overload=numBcnt
	if (numAcnt==numBcnt):
		forlist = numA
		overload=numAcnt
	overcnt=1
	for dxpink in forlist:
		loopregA=1
		loopregB=1
		for Areg in numA:
			
			if curregA==loopregA:
				returnedA=1
				Aval = Areg
				break
			loopregA += 1
		for Breg in numB:
			
			if curregB==loopregB:
				returnedB=1
				Bval = Breg
				break
			loopregB += 1
		#print ("A:" + Aval + str(returnedA))
		#print ("B:" + Bval + str(returnedB))
		#Aval=+ rules:
		if Aval=="E":
			eotA=1
			Aval="0"
		if Bval=="E":
			eotB=1
			Bval="0"
		if (Aval=="+" and Bval=="+"):
			if carry=="0":
				resbt = ("-" + resbt)
				carry="+"
			elif carry=="+":
				resbt = ("0" + resbt)
				carry="+"
			elif carry=="-":
				resbt = ("+" + resbt)
				carry="0"
		elif (Aval=="+" and Bval=="0"):
			if carry=="0":
				resbt = ("+" + resbt)
				carry="0"
			elif carry=="+":
				resbt = ("-" + resbt)
				carry="+"
			elif carry=="-":
				resbt = ("0" + resbt)
				carry="0"
		elif (Aval=="+" and Bval=="-"):
			if carry=="0":
				resbt = ("0" + resbt)
				carry="0"
			elif carry=="+":
				resbt = ("+" + resbt)
				carry="0"
			elif carry=="-":
				resbt = ("-" + resbt)
				carry="0"
		#Aval=- rules
		elif (Aval=="-" and Bval=="-"):
			if carry=="0":
				resbt = ("+" + resbt)
				carry="-"
			elif carry=="-":
				resbt = ("0" + resbt)
				carry="-"
			elif carry=="+":
				resbt = ("-" + resbt)
				carry="0"
		elif (Aval=="-" and Bval=="0"):
			if carry=="0":
				resbt = ("-" + resbt)
				carry="0"
			elif carry=="+":
				resbt = ("0" + resbt)
				carry="0"
			elif carry=="-":
				resbt = ("+" + resbt)
				carry="-"
		elif (Aval=="-" and Bval=="+"):
			if carry=="0":
				resbt = ("0" + resbt)
				carry="0"
			elif carry=="+":
				resbt = ("+" + resbt)
				carry="0"
			elif carry=="-":
				resbt = ("-" + resbt)
				carry="0"
		#Aval=0 rules
		elif (Aval=="0" and Bval=="0"):
			if carry=="0":
				resbt = ("0" + resbt)
				carry="0"
			elif carry=="+":
				resbt = ("+" + resbt)
				carry="0"
			elif carry=="-":
				resbt = ("-" + resbt)
				carry="0"
		elif (Aval=="0" and Bval=="-"):
			if carry=="0":
				resbt = ("-" + resbt)
				carry="0"
			elif carry=="+":
				resbt = ("0" + resbt)
				carry="0"
			elif carry=="-":
				resbt = ("+" + resbt)
				carry="-"
		elif (Aval=="0" and Bval=="+"):
			if carry=="0":
				resbt = ("+" + resbt)
				carry="0"
			elif carry=="+":
				resbt = ("-" + resbt)
				carry="+"
			elif carry=="-":
				resbt = ("0" + resbt)
				carry="0"
		curregA += 1
		curregB += 1
		Aval="0"
		Bval="0"
		returnedA=0
		returnedB=0
	#print ()
	buzzt=trailzerostrip(str(resbt))
	vexping=str(buzzt)
	return (buzzt)


#count up based Decimal to balanced ternary converter.
def DECTOBTold(NUMTOCONV1):
	decicnt=0
	prevbtnum="0"
	charlst1=str(NUMTOCONV1)
	for fstdig in charlst1:
		firstsym=fstdig
		break
	if firstsym=="-":
		btcntdig="-"
	elif firstsym!="-":
		btcntdig="+"
	#print("actual decimal count| BT count in decimal | BT count")
	while decicnt!=NUMTOCONV1:
		
		#print (str(decicnt) + "|" +  str(libbaltcalc.BTTODEC(prevbtnum)) + "|" +  prevbtnum)
		prevbtnum=(btadd(prevbtnum, btcntdig))
		vixiestr=prevbtnum
		if firstsym=="-":
			decicnt -= 1
		elif firstsym!="-":
			decicnt += 1
	return (vixiestr)

#print(DECTOBT(19))

#gets a balanced ternary number from the user an parses it based on various 
#balanced ternary notation conventions. currently only the 1,0,T and +,0,- conventions.
def BTstrgetsort():
	NUMPARS = raw_input('>:')
	NUMPARS = NUMPARS.replace("1", "+").replace("T", "-")
	return (NUMPARS)
#gets a sigle-trit balanced ternary number from the user an parses it based on various 
#balanced ternary notation conventions. currently only the 1,0,T and +,0,- conventions.
def BTstrgetsingle():
	NUMPX = BTstrgetsort()
	for fstdig in NUMPX:
		return (fstdig)

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

