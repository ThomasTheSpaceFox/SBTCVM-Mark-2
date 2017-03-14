#!/usr/bin/env python
import libbaltcalc
import pygame
import array
import math
import time
import os

#SBTCVM common function library.


#used to get linear adress point number in decimal (for example for fiding an adress in the rom)
def numstruct(code):
	strut1=(libbaltcalc.BTTODEC(code))
	strut2=(strut1 + 9842)
	#print strut2
	return strut2

#used by the buzzer (do not use for 9 trit numtructs. use normal numstruct for that!)
def buzznumstruct5(code):
	strut1=(libbaltcalc.BTTODEC(code))
	strut2=(strut1 + 122)
	#print strut2
	return strut2
	
def drawnumstruct3(code):
	strut1=(libbaltcalc.BTTODEC(code))
	strut2=(strut1 + 13)
	#print strut2
	return strut2

def drawnumstruct2(code):
	strut1=(libbaltcalc.BTTODEC(code))
	strut2=(strut1 + 4)
	#print strut2
	return strut2
#raster draw support
def dollytell(lookupcode):
	if lookupcode=="--":
		return("0")
	if lookupcode=="-0":
		return("32")
	if lookupcode=="-+":
		return("64")
	if lookupcode=="0-":
		return("96")
	if lookupcode=="00":
		return("127")
	if lookupcode=="0+":
		return("159")
	if lookupcode=="+-":
		return("191")
	if lookupcode=="+0":
		return("223")
	if lookupcode=="++":
		return("255")


def colorfind(CODE):
	REDBT = (CODE[0] + CODE[1])
	GRNBT = (CODE[2] + CODE[3])
	BLUBT = (CODE[4] + CODE[5])
	REDBIN = (dollytell(REDBT))
	GRNBIN = (dollytell(GRNBT))
	BLUBIN = (dollytell(BLUBT))
	#NAME = datalist
	return((int(REDBIN), int(GRNBIN), int(BLUBIN)))

#returns pygame rectangle from 2 points used to draw vector filled rectangles
def makerectbipoint(Jx1, Jy1, Jx2, Jy2):
	if Jx1>Jx2:
		sizeX=(Jx1-Jx2)
		xval=Jx2
	else:
		sizeX=(Jx2-Jx1)
		xval=Jx1
	if Jy1>Jy2:
		yval=Jy2
		sizeY=(Jy1-Jy2)
	else:
		sizeY=(Jy2-Jy1)
		yval=Jy1
	sizeY += 1
	sizeX += 1
	return(pygame.Rect((xval, yval), (sizeX, sizeY)))

#more intelegent truncation function (used in the math functions for example)
def trunkto6(code):
	codecnt=0
	for fel in code:
		codecnt +=1
	if codecnt<9:
		if codecnt==8:
			return("0" + code)
		if codecnt==7:
			return("00" + code)
		if codecnt==6:
			return("000" + code)
		if codecnt==5:
			return("0000" + code)
		if codecnt==4:
			return("00000" + code)
		if codecnt==3:
			return("000000" + code)
		if codecnt==2:
			return("0000000" + code)
		if codecnt==1:
			return("00000000" + code)
	#print code
	#code=libbaltcalc.BTINVERT(code)
	return((code[0]) + (code[1]) + (code[2]) + (code[3]) + (code[4]) + (code[5]) + (code[6]) + (code[7]) + (code[8]))

def trunkto6math(code):
	codecnt=0
	for fel in code:
		codecnt +=1
	if codecnt<9:
		if codecnt==8:
			return("0" + code)
		if codecnt==7:
			return("00" + code)
		if codecnt==6:
			return("000" + code)
		if codecnt==5:
			return("0000" + code)
		if codecnt==4:
			return("00000" + code)
		if codecnt==3:
			return("000000" + code)
		if codecnt==2:
			return("0000000" + code)
		if codecnt==1:
			return("00000000" + code)
	#print code
	#code=libbaltcalc.BTINVERT(code)

	#print code
	#code=libbaltcalc.BTINVERT(code)
	if codecnt>9:
		print "integer overflow"
		code="---------"
	return((code[0]) + (code[1]) + (code[2]) + (code[3]) + (code[4]) + (code[5]) + (code[6]) + (code[7]) + (code[8]))

#print(trunkto6("---0+++"))
#print(trunkto6("--0+++"))
#print(trunkto6("-0+++"))
#print(trunkto6("0+++"))
#print(trunkto6("+++"))
#print(trunkto6("++"))
#print(trunkto6("+"))

def abtslackline(receveabt, linetext):
	interx=[(receveabt[1]), (receveabt[2]),(receveabt[3]), (receveabt[4]), (receveabt[5]), (receveabt[6]), (receveabt[7]), (receveabt[8]), (receveabt[9]), (receveabt[10]), (receveabt[11]), (receveabt[12]), (receveabt[13]), (receveabt[14]), (receveabt[15]), (receveabt[16]), (receveabt[17]), (receveabt[18]), (receveabt[19]), (receveabt[20]), (receveabt[21]), (receveabt[22]), (receveabt[23]), (receveabt[24]), (receveabt[25]),(receveabt[26]), (linetext)]
	return interx

def abtcharblit(receveabtb, charblit):
	if charblit=="\n":
		receveabtb=abtslackline(receveabtb, "")
	else:
		charnum=0
		curr=receveabtb[26]
		for f in curr:
			if charnum==36:
				receveabtb=abtslackline(receveabtb, "")
			charnum += 1
		receveabtb[26]=((receveabtb[26]) + charblit)
	return(receveabtb)

#sound functions
	
def mk1buzz(code):
	timechar=code[0]
	#print timechar
	if timechar=="+":
		timemag=60
	elif timechar=="-":
		timemag=20
	else:
		timemag=40
	freqcode=((code[1]) + (code[2]) + (code[3]) + (code[4]) +(code[5]))
	#print freqcode
	baserep=160
	repjump=2
	magn=buzznumstruct5(libbaltcalc.BTINVERT(freqcode))
	magn=(243 - magn + 20)
	
	repadd=(repjump * magn)
	#samplmag=sqblksnd((baserep + repadd), (20))
	#sampltnk=samplmag[:6480]
	if timechar=="+":
		#sampltnk=(sampltnk + sampltnk + sampltnk + sampltnk + sampltnk)
		sampltnk=autosquare(repadd, 0.31)
	elif timechar=="-":
		sampltnk=autosquare(repadd, 0.11)
		#sampltnk=(sampltnk)
		
	else:
		#sampltnk=(sampltnk + sampltnk + sampltnk)
		sampltnk=autosquare(repadd, 0.21)
	#print sampltnk
	return sampltnk

def foobsin(num):
	#return math.sin(math.sin(math.sin(num)))
	#return math.sin(math.sin(num))
	return (math.floor(math.sin(num)) * 4500)


def autosquare(freq, lenth):
	temparray=array.array('f', [(foobsin(2.0 * math.pi * freq * t / 22050)) for t in xrange(0, int(lenth * 22050))])
	return temparray

#SBTC Graphics operations (currently just TUI routines, future plans include actual graphics modes.

pygame.font.init()
simplefont = pygame.font.SysFont(None, 16)


fondir="FONT0"


def abtslackline(receveabt, linetext):
	interx=[(receveabt[1]), (receveabt[2]),(receveabt[3]), (receveabt[4]), (receveabt[5]), (receveabt[6]), (receveabt[7]), (receveabt[8]), (receveabt[9]), (receveabt[10]), (receveabt[11]), (receveabt[12]), (receveabt[13]), (receveabt[14]), (receveabt[15]), (receveabt[16]), (receveabt[17]), (receveabt[18]), (receveabt[19]), (receveabt[20]), (receveabt[21]), (receveabt[22]), (receveabt[23]), (receveabt[24]), (receveabt[25]),(receveabt[26]), (linetext)]
	return interx

def abtcharblit(receveabtb, charblit):
	if charblit=="\n":
		receveabtb=abtslackline(receveabtb, "")
	else:
		charnum=0
		curr=receveabtb[26]
		for f in curr:
			if charnum==36:
				receveabtb=abtslackline(receveabtb, "")
			charnum += 1
		receveabtb[26]=((receveabtb[26]) + charblit)
	return(receveabtb)

def charblit(chsurface, colx, liney, charcode):
	colx=(colx*9)
	liney=(liney*9)
	glifcode=charcodedict.get(charcode)
	#print glifcode
	gliffile=(chargliph.get(glifcode))
	#print gliffile
	glif=pygame.image.load(os.path.join(fondir, (chargliph.get(glifcode))))
	chsurface.blit(glif, (colx, liney))
	return chsurface




#Text encoding tables

charcodedict = {"------": "a", "-----0": "b", "-----+": "c", "----0-": "d", "----00": "e", "----0+": "f", "----+-": "g", "----+0": "h", "----++": "i", "---0--": "j", "---0-0": "k", "---0-+": "l", "---00-": "m", "---000": "n", "---00+": "o", "---0+-": "p", "---0+0": "q", "---0++": "r", "---+--": "s", "---+-0": "t", "---+-+": "u", "---+0-": "v", "---+00": "w", "---+0+": "x", "---++-": "y", "---++0": "z", "---+++": "A", "--0---": "B", "--0--0": "C", "--0--+": "D", "--0-0-": "E", "--0-00": "F", "--0-0+": "G", "--0-+-": "H", "--0-+0": "I", "--0-++": "J", "--00--": "K", "--00-0": "L", "--00-+": "M", "--000-": "N", "--0000": "O", "--000+": "P", "--00+-": "Q", "--00+0": "R", "--00++": "S", "--0+--": "T", "--0+-0": "U", "--0+-+": "V", "--0+0-": "W", "--0+00": "X", "--0+0+": "Y", "--0++-": "Z", "--0++0": "0", "--0+++": "1", "--+---": "2", "--+--0": "3", "--+--+": "4", "--+-0-": "5", "--+-00": "6", "--+-0+": "7", "--+-+-": "8", "--+-+0": "9", "--+-++": "`", "--+0--": "~", "--+0-0": "!", "--+0-+": "@", "--+00-": "#", "--+000": "$", "--+00+": "%", "--+0+-": "^", "--+0+0": "&", "--+0++": "*", "--++--": "(", "--++-0": ")", "--++-+": "-", "--++0-": "=", "--++00": "_", "--++0+": "+", "--+++-": "[", "--+++0": "]", "--++++": "\\", "-0----": "{", "-0---0": "}", "-0---+": "|", "-0--0-": ";", "-0--00": "\'", "-0--0+": ",", "-0--+-": ".", "-0--+0": "/", "-0--++": ":", "-0-0--": '\"', "-0-0-0": "<", "-0-0-+": ">", "-0-00-": "?", "-0-000": "\n", "-0-00+": " "}
#primary character lookup dictionary (returns code of a character)
charlookupdict={"a": "------", "b": "-----0", "c": "-----+", "d": "----0-", "e": "----00", "f": "----0+", "g": "----+-", "h": "----+0", "i": "----++", "j": "---0--", "k": "---0-0", "l": "---0-+", "m": "---00-", "n": "---000", "o": "---00+", "p": "---0+-", "q": "---0+0", "r": "---0++", "s": "---+--", "t": "---+-0", "u": "---+-+", "v": "---+0-", "w": "---+00", "x": "---+0+", "y": "---++-", "z": "---++0", "A": "---+++", "B": "--0---", "C": "--0--0", "D": "--0--+", "E": "--0-0-", "F": "--0-00", "G": "--0-0+", "H": "--0-+-", "I": "--0-+0", "J": "--0-++", "K": "--00--", "L": "--00-0", "M": "--00-+", "N": "--000-", "O": "--0000", "P": "--000+", "Q": "--00+-", "R": "--00+0", "S": "--00++", "T": "--0+--", "U": "--0+-0", "V": "--0+-+", "W": "--0+0-", "X": "--0+00", "Y": "--0+0+", "Z": "--0++-", "0": "--0++0", "1": "--0+++", "2": "--+---", "3": "--+--0", "4": "--+--+", "5": "--+-0-", "6": "--+-00", "7": "--+-0+", "8": "--+-+-", "9": "--+-+0", "`": "--+-++", "~": "--+0--", "!": "--+0-0", "@": "--+0-+", "#": "--+00-", "$": "--+000", "%": "--+00+", "^": "--+0+-", "&": "--+0+0", "*": "--+0++", "(": "--++--", ")": "--++-0", "-": "--++-+", "=": "--++0-", "_": "--++00", "+": "--++0+", "[": "--+++-", "]": "--+++0", "\\": "--++++", "{": "-0----", "}": "-0---0", "|": "-0---+", ";": "-0--0-", "\'": "-0--00", ",": "-0--0+", ".": "-0--+-", "/": "-0--+0", ":": "-0--++", '\"': "-0-0--", "<": "-0-0-0", ">": "-0-0-+", "?": "-0-00-", "\n": "-0-000", " ": "-0-00+"}
#character gliph table.
chargliph={"a": "chara.gif", "b": "charb.gif", "c": "charc.gif", "d": "chard.gif", "e": "chare.gif", "f": "charf.gif", "g": "charg.gif", "h": "charh.gif", "i": "chari.gif", "j": "charj.gif", "k": "chark.gif", "l": "charl.gif", "m": "charm.gif", "n": "charn.gif", "o": "charo.gif", "p": "charp.gif", "q": "charq.gif", "r": "charr.gif", "s": "chars.gif", "t": "chart.gif", "u": "charu.gif", "v": "charv.gif", "w": "charw.gif", "x": "charx.gif", "y": "chary.gif", "z": "charz.gif", "A": "charAc.gif", "B": "charBc.gif", "C": "charCc.gif", "D": "charDc.gif", "E": "charEc.gif", "F": "charFc.gif", "G": "charGc.gif", "H": "charHc.gif", "I": "charIc.gif", "J": "charJc.gif", "K": "charKc.gif", "L": "charLc.gif", "M": "charMc.gif", "N": "charNc.gif", "O": "charOc.gif", "P": "charPc.gif", "Q": "charQc.gif", "R": "charRc.gif", "S": "charSc.gif", "T": "charTc.gif", "U": "charUc.gif", "V": "charVc.gif", "W": "charWc.gif", "X": "charXc.gif", "Y": "charYc.gif", "Z": "charZc.gif", "0": "char0.gif", "1": "char1.gif", "2": "char2.gif", "3": "char3.gif", "4": "char4.gif", "5": "char5.gif", "6": "char6.gif", "7": "char7.gif", "8": "char8.gif", "9": "char9.gif", "`": "characcent.gif", "~": "chartild.gif", "!": "charexclaim.gif", "@": "charAT.gif", "#": "charhash.gif", "$": "charUSD.gif", "%": "charPERC.gif", "^": "charCARROT.gif", "&": "charAND.gif", "*": "charATRISK.gif", "(": "charLPAR.gif", ")": "charRPAR.gif", "-": "charHYPHON.gif", "=": "charEQUAL.gif", "_": "charUNDERSC.gif", "+": "charPLUS.gif", "[": "charLBRAK.gif", "]": "charRBRAK.gif", "\\": "charBKSLASH.gif", "{": "charLCURL.gif", "}": "charRCURL.gif", "|": "charVERTBAR.gif", ";": "charsemicol.gif", "\'": "charapos.gif", ",": "charcomma.gif", ".": "charpereod.gif", "/": "charFDSLASH.gif", ":": "charcol.gif", '\"': "charDUBQTE.gif", "<": "charLESSTHAN.gif", ">": "charGREATTHAN.gif", "?": "charquestion.gif", " ": "charSPACE.gif"}

#primary character list. use to check if a character has a valid code
charscrossck=["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "`", "~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "=", "_", "+", "[", "]", "\\", "{", "}", "|", ";", "\'", ",", ".", "/", ":", '\"', "<", ">", "?", "\n", " "]

def charcodelook(code):
	return(charcodedict[code])

def charlook(char):
	return(charlookupdict[char])


#keep these lists at the end of the library! no reason, just so someone with 
#word wrap isnt scrolling forever :p
#IO Address list for buffer clear (no longer used)
#chklist = ["+00+--", "+00+-0", "+00+-+", "+00+0-", "+00+00", "+00+0+", "+00++-", "+00++0", "+00+++", "+0+---", "+0+--0", "+0+--+", "+0+-0-", "+0+-00", "+0+-0+", "+0+-+-", "+0+-+0", "+0+-++", "+0+0--", "+0+0-0", "+0+0-+", "+0+00-", "+0+000", "+0+00+", "+0+0+-", "+0+0+0", "+0+0++", "+0++--", "+0++-0", "+0++-+", "+0++0-", "+0++00", "+0++0+", "+0+++-", "+0+++0", "+0++++", "++----", "++---0", "++---+", "++--0-", "++--00", "++--0+", "++--+-", "++--+0", "++--++", "++-0--", "++-0-0", "++-0-+", "++-00-", "++-000", "++-00+", "++-0+-", "++-0+0", "++-0++", "++-+--", "++-+-0", "++-+-+", "++-+0-", "++-+00", "++-+0+", "++-++-", "++-++0", "++-+++", "++0---", "++0--0", "++0--+", "++0-0-", "++0-00", "++0-0+", "++0-+-", "++0-+0", "++0-++", "++00--", "++00-0", "++00-+", "++000-", "++0000", "++000+", "++00+-", "++00+0", "++00++", "++0+--", "++0+-0", "++0+-+", "++0+0-", "++0+00", "++0+0+", "++0++-", "++0++0", "++0+++", "+++---", "+++--0", "+++--+", "+++-0-", "+++-00", "+++-0+", "+++-+-", "+++-+0", "+++-++", "+++0--", "+++0-0", "+++0-+", "+++00-", "+++000", "+++00+", "+++0+-", "+++0+0", "+++0++", "++++--", "++++-0", "++++-+", "++++0-", "++++00", "++++0+", "+++++-", "+++++0", "++++++"]

#main IOBUS List (used at startup to build RAMbank dictionary
#calmlst = ["------", "-----0", "-----+", "----0-", "----00", "----0+", "----+-", "----+0", "----++", "---0--", "---0-0", "---0-+", "---00-", "---000", "---00+", "---0+-", "---0+0", "---0++", "---+--", "---+-0", "---+-+", "---+0-", "---+00", "---+0+", "---++-", "---++0", "---+++", "--0---", "--0--0", "--0--+", "--0-0-", "--0-00", "--0-0+", "--0-+-", "--0-+0", "--0-++", "--00--", "--00-0", "--00-+", "--000-", "--0000", "--000+", "--00+-", "--00+0", "--00++", "--0+--", "--0+-0", "--0+-+", "--0+0-", "--0+00", "--0+0+", "--0++-", "--0++0", "--0+++", "--+---", "--+--0", "--+--+", "--+-0-", "--+-00", "--+-0+", "--+-+-", "--+-+0", "--+-++", "--+0--", "--+0-0", "--+0-+", "--+00-", "--+000", "--+00+", "--+0+-", "--+0+0", "--+0++", "--++--", "--++-0", "--++-+", "--++0-", "--++00", "--++0+", "--+++-", "--+++0", "--++++", "-0----", "-0---0", "-0---+", "-0--0-", "-0--00", "-0--0+", "-0--+-", "-0--+0", "-0--++", "-0-0--", "-0-0-0", "-0-0-+", "-0-00-", "-0-000", "-0-00+", "-0-0+-", "-0-0+0", "-0-0++", "-0-+--", "-0-+-0", "-0-+-+", "-0-+0-", "-0-+00", "-0-+0+", "-0-++-", "-0-++0", "-0-+++", "-00---", "-00--0", "-00--+", "-00-0-", "-00-00", "-00-0+", "-00-+-", "-00-+0", "-00-++", "-000--", "-000-0", "-000-+", "-0000-", "-00000", "-0000+", "-000+-", "-000+0", "-000++", "-00+--", "-00+-0", "-00+-+", "-00+0-", "-00+00", "-00+0+", "-00++-", "-00++0", "-00+++", "-0+---", "-0+--0", "-0+--+", "-0+-0-", "-0+-00", "-0+-0+", "-0+-+-", "-0+-+0", "-0+-++", "-0+0--", "-0+0-0", "-0+0-+", "-0+00-", "-0+000", "-0+00+", "-0+0+-", "-0+0+0", "-0+0++", "-0++--", "-0++-0", "-0++-+", "-0++0-", "-0++00", "-0++0+", "-0+++-", "-0+++0", "-0++++", "-+----", "-+---0", "-+---+", "-+--0-", "-+--00", "-+--0+", "-+--+-", "-+--+0", "-+--++", "-+-0--", "-+-0-0", "-+-0-+", "-+-00-", "-+-000", "-+-00+", "-+-0+-", "-+-0+0", "-+-0++", "-+-+--", "-+-+-0", "-+-+-+", "-+-+0-", "-+-+00", "-+-+0+", "-+-++-", "-+-++0", "-+-+++", "-+0---", "-+0--0", "-+0--+", "-+0-0-", "-+0-00", "-+0-0+", "-+0-+-", "-+0-+0", "-+0-++", "-+00--", "-+00-0", "-+00-+", "-+000-", "-+0000", "-+000+", "-+00+-", "-+00+0", "-+00++", "-+0+--", "-+0+-0", "-+0+-+", "-+0+0-", "-+0+00", "-+0+0+", "-+0++-", "-+0++0", "-+0+++", "-++---", "-++--0", "-++--+", "-++-0-", "-++-00", "-++-0+", "-++-+-", "-++-+0", "-++-++", "-++0--", "-++0-0", "-++0-+", "-++00-", "-++000", "-++00+", "-++0+-", "-++0+0", "-++0++", "-+++--", "-+++-0", "-+++-+", "-+++0-", "-+++00", "-+++0+", "-++++-", "-++++0", "-+++++", "0-----", "0----0", "0----+", "0---0-", "0---00", "0---0+", "0---+-", "0---+0", "0---++", "0--0--", "0--0-0", "0--0-+", "0--00-", "0--000", "0--00+", "0--0+-", "0--0+0", "0--0++", "0--+--", "0--+-0", "0--+-+", "0--+0-", "0--+00", "0--+0+", "0--++-", "0--++0", "0--+++", "0-0---", "0-0--0", "0-0--+", "0-0-0-", "0-0-00", "0-0-0+", "0-0-+-", "0-0-+0", "0-0-++", "0-00--", "0-00-0", "0-00-+", "0-000-", "0-0000", "0-000+", "0-00+-", "0-00+0", "0-00++", "0-0+--", "0-0+-0", "0-0+-+", "0-0+0-", "0-0+00", "0-0+0+", "0-0++-", "0-0++0", "0-0+++", "0-+---", "0-+--0", "0-+--+", "0-+-0-", "0-+-00", "0-+-0+", "0-+-+-", "0-+-+0", "0-+-++", "0-+0--", "0-+0-0", "0-+0-+", "0-+00-", "0-+000", "0-+00+", "0-+0+-", "0-+0+0", "0-+0++", "0-++--", "0-++-0", "0-++-+", "0-++0-", "0-++00", "0-++0+", "0-+++-", "0-+++0", "0-++++", "00----", "00---0", "00---+", "00--0-", "00--00", "00--0+", "00--+-", "00--+0", "00--++", "00-0--", "00-0-0", "00-0-+", "00-00-", "00-000", "00-00+", "00-0+-", "00-0+0", "00-0++", "00-+--", "00-+-0", "00-+-+", "00-+0-", "00-+00", "00-+0+", "00-++-", "00-++0", "00-+++", "000---", "000--0", "000--+", "000-0-", "000-00", "000-0+", "000-+-", "000-+0", "000-++", "0000--", "0000-0", "0000-+", "00000-", "000000", "00000+", "0000+-", "0000+0", "0000++", "000+--", "000+-0", "000+-+", "000+0-", "000+00", "000+0+", "000++-", "000++0", "000+++", "00+---", "00+--0", "00+--+", "00+-0-", "00+-00", "00+-0+", "00+-+-", "00+-+0", "00+-++", "00+0--", "00+0-0", "00+0-+", "00+00-", "00+000", "00+00+", "00+0+-", "00+0+0", "00+0++", "00++--", "00++-0", "00++-+", "00++0-", "00++00", "00++0+", "00+++-", "00+++0", "00++++", "0+----", "0+---0", "0+---+", "0+--0-", "0+--00", "0+--0+", "0+--+-", "0+--+0", "0+--++", "0+-0--", "0+-0-0", "0+-0-+", "0+-00-", "0+-000", "0+-00+", "0+-0+-", "0+-0+0", "0+-0++", "0+-+--", "0+-+-0", "0+-+-+", "0+-+0-", "0+-+00", "0+-+0+", "0+-++-", "0+-++0", "0+-+++", "0+0---", "0+0--0", "0+0--+", "0+0-0-", "0+0-00", "0+0-0+", "0+0-+-", "0+0-+0", "0+0-++", "0+00--", "0+00-0", "0+00-+", "0+000-", "0+0000", "0+000+", "0+00+-", "0+00+0", "0+00++", "0+0+--", "0+0+-0", "0+0+-+", "0+0+0-", "0+0+00", "0+0+0+", "0+0++-", "0+0++0", "0+0+++", "0++---", "0++--0", "0++--+", "0++-0-", "0++-00", "0++-0+", "0++-+-", "0++-+0", "0++-++", "0++0--", "0++0-0", "0++0-+", "0++00-", "0++000", "0++00+", "0++0+-", "0++0+0", "0++0++", "0+++--", "0+++-0", "0+++-+", "0+++0-", "0+++00", "0+++0+", "0++++-", "0++++0", "0+++++", "+-----", "+----0", "+----+", "+---0-", "+---00", "+---0+", "+---+-", "+---+0", "+---++", "+--0--", "+--0-0", "+--0-+", "+--00-", "+--000", "+--00+", "+--0+-", "+--0+0", "+--0++", "+--+--", "+--+-0", "+--+-+", "+--+0-", "+--+00", "+--+0+", "+--++-", "+--++0", "+--+++", "+-0---", "+-0--0", "+-0--+", "+-0-0-", "+-0-00", "+-0-0+", "+-0-+-", "+-0-+0", "+-0-++", "+-00--", "+-00-0", "+-00-+", "+-000-", "+-0000", "+-000+", "+-00+-", "+-00+0", "+-00++", "+-0+--", "+-0+-0", "+-0+-+", "+-0+0-", "+-0+00", "+-0+0+", "+-0++-", "+-0++0", "+-0+++", "+-+---", "+-+--0", "+-+--+", "+-+-0-", "+-+-00", "+-+-0+", "+-+-+-", "+-+-+0", "+-+-++", "+-+0--", "+-+0-0", "+-+0-+", "+-+00-", "+-+000", "+-+00+", "+-+0+-", "+-+0+0", "+-+0++", "+-++--", "+-++-0", "+-++-+", "+-++0-", "+-++00", "+-++0+", "+-+++-", "+-+++0", "+-++++", "+0----", "+0---0", "+0---+", "+0--0-", "+0--00", "+0--0+", "+0--+-", "+0--+0", "+0--++", "+0-0--", "+0-0-0", "+0-0-+", "+0-00-", "+0-000", "+0-00+", "+0-0+-", "+0-0+0", "+0-0++", "+0-+--", "+0-+-0", "+0-+-+", "+0-+0-", "+0-+00", "+0-+0+", "+0-++-", "+0-++0", "+0-+++", "+00---", "+00--0", "+00--+", "+00-0-", "+00-00", "+00-0+", "+00-+-", "+00-+0", "+00-++", "+000--", "+000-0", "+000-+", "+0000-", "+00000", "+0000+", "+000+-", "+000+0", "+000++", "+00+--", "+00+-0", "+00+-+", "+00+0-", "+00+00", "+00+0+", "+00++-", "+00++0", "+00+++", "+0+---", "+0+--0", "+0+--+", "+0+-0-", "+0+-00", "+0+-0+", "+0+-+-", "+0+-+0", "+0+-++", "+0+0--", "+0+0-0", "+0+0-+", "+0+00-", "+0+000", "+0+00+", "+0+0+-", "+0+0+0", "+0+0++", "+0++--", "+0++-0", "+0++-+", "+0++0-", "+0++00", "+0++0+", "+0+++-", "+0+++0", "+0++++", "++----", "++---0", "++---+", "++--0-", "++--00", "++--0+", "++--+-", "++--+0", "++--++", "++-0--", "++-0-0", "++-0-+", "++-00-", "++-000", "++-00+", "++-0+-", "++-0+0", "++-0++", "++-+--", "++-+-0", "++-+-+", "++-+0-", "++-+00", "++-+0+", "++-++-", "++-++0", "++-+++", "++0---", "++0--0", "++0--+", "++0-0-", "++0-00", "++0-0+", "++0-+-", "++0-+0", "++0-++", "++00--", "++00-0", "++00-+", "++000-", "++0000", "++000+", "++00+-", "++00+0", "++00++", "++0+--", "++0+-0", "++0+-+", "++0+0-", "++0+00", "++0+0+", "++0++-", "++0++0", "++0+++", "+++---", "+++--0", "+++--+", "+++-0-", "+++-00", "+++-0+", "+++-+-", "+++-+0", "+++-++", "+++0--", "+++0-0", "+++0-+", "+++00-", "+++000", "+++00+", "+++0+-", "+++0+0", "+++0++", "++++--", "++++-0", "++++-+", "++++0-", "++++00", "++++0+", "+++++-", "+++++0", "++++++"]
