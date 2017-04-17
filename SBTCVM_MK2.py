#!/usr/bin/env python
import libtrom
import pygame
from pygame.locals import *
import time
import os
import libSBTCVM
import libbaltcalc
import sys
from random import randint
pygame.display.init()

print "SBTCVM Mark 2 Starting up..."

windowicon=pygame.image.load(os.path.join('GFX', 'icon64.png'))
pygame.display.set_icon(windowicon)

screensurf=pygame.display.set_mode((800, 600))
libSBTCVM.glyphoptim(screensurf)
pygame.display.set_caption("SBTCVM Mark 2", "SBTCVM Mark 2")
pygame.font.init()
#used for TTY
simplefont = pygame.font.SysFont(None, 16)
#used for smaller data displays (inst. data etc.)
#smldispfont = pygame.font.SysFont(None, 16)
smldispfont = pygame.font.Font("SBTCVMreadout.ttf", 16)
#used in larger data displays (register displays, etc.)
#lgdispfont = pygame.font.SysFont(None, 20)
lgdispfont = pygame.font.Font("SBTCVMreadout.ttf", 16)
pixcnt1=40
pixjmp=14
USRYN=0
USRWAIT=0

keyintreg="0000"

#graphics:
#background pixmap
vmbg=pygame.image.load(os.path.join('GFX', 'VMBG.png')).convert()
#indicator lamps
#GREEN
LEDGREENON=pygame.image.load(os.path.join('GFX', 'LAMP-GREEN.png')).convert()
LEDGREENOFF=pygame.image.load(os.path.join('GFX', 'LAMP-GREEN-OFF.png')).convert()
#CPU
CPULEDACT=pygame.image.load(os.path.join('GFX', 'LAMP-BLUE.png')).convert()
CPULEDSTANDBY=pygame.image.load(os.path.join('GFX', 'LAMP-ORANGE.png')).convert()

COLORDISP=pygame.image.load(os.path.join('GFX', 'COLORDISP-DEF.png')).convert()
MONODISP=pygame.image.load(os.path.join('GFX', 'MONODISP-DEF.png')).convert()
#this list is what is displayed on the TTY on VM boot.

abt=["SBTCVM", "Mark 2", "v2.0.0", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "ready", ""]
abtpref=["This is different", "Mark 2", "v2.0.0", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "ready", ""]

pygame.mixer.init(frequency=22050 , size=-16)

extradraw=0

wavsp=libSBTCVM.mk1buzz("0-----")
snf=pygame.mixer.Sound(wavsp)
snf.play()

#config defaults
TROMA="intro.trom"
#these are dud roms full of soft stops
TROMB=("DEFAULT.TROM")
TROMC=("DEFAULT.TROM")
TROMD=("DEFAULT.TROM")
TROME=("DEFAULT.TROM")
TROMF=("DEFAULT.TROM")
CPUWAIT=(0.005)
stepbystep=0
scconf=open('BOOTUP.CFG', 'r')
exconf=compile(scconf.read(), 'BOOTUP.CFG', 'exec')

tuibig=1
logromexit=0
logIOexit=0
disablereadouts=0
exec(exconf)

#try:
	#cmd=sys.argv[1]
	#TROMA=cmd
	#libtrom.redefA(cmd)
	#print "Running trom specified in command line..."
#except IndexError:
	#print "no command line run argument found. do normal execution..."

key1=0
key2=0
key3=0
key4=0
key5=0
key6=0
key7=0
key8=0
key9=0
key0=0
keypos=0
keyhyp=0
keyq=0
keyw=0
keye=0
keyr=0
keyt=0
keyy=0
keyu=0
keyi=0
keyo=0
keyp=0
keya=0
keysx=0
keyd=0
keyf=0
keyg=0
keyh=0
keyj=0
keyk=0
keyl=0
keyz=0
keyx=0
keyc=0
keyv=0
keyb=0
keyn=0
keym=0
keyspace=0
keyret=0

TTYrenderflg="0"

if 'GLOBRUNFLG' in globals():
	
	TROMA=GLOBRUNFLG
	libtrom.redefA(TROMA)
	print ("GLOBRUNFLG found... \n running trom: \"" + TROMA + "\" as TROMA")

#tritlength defaults
tritloadlen=9
tritoffset=0
tritdestgnd=0

def tritlen(srcdata, destdata):
	#just return srcdata if tritloadlen=9 and tritoffset=0
	if tritdestgnd==1:
		destdata="000000000"
	if tritloadlen==9 and tritoffset==0:
		#print srcdata
		return (srcdata)
	destdict={}
	destcnt=0
	tritstart=(8 - tritoffset)
	tritstop=(tritstart - tritloadlen)
	#print tritstop
	tritstack=1
	iterlist=[0, 1, 2, 3, 4, 5, 6, 7, 8]
	#parse destination data into a dict
	for f in destdata:
		destdict[destcnt]=f
		destcnt += 1
	#modify destination dict 
	for f in iterlist:
		#print tritstart
		destdict[tritstart]=srcdata[tritstart]
		tritstart -= 1
		tritstack += 1
		if tritstart==tritstop or tritstart==-1:
			break
	#print destdict
	destdataout=""
	#parse destination dict back into string and return result.
	for f in iterlist:
		destdataout=(destdataout + destdict[f])
	#print destdataout
	return destdataout
		
		
	
	



#tritloadlen=1
#tritoffset=0
#dataret=tritlen("---------", "+++++++++")
#print (dataret)
#sys.exit()


TTYBGCOL=libSBTCVM.colorfind("000000")
TTYBGCOLREG="000000"

#print BOOTUPFILE

#4 trit instruct
#6 trit data.
#as such:
#iiiidddddd

colvectorreg="000000"
monovectorreg="000000"

if stepbystep==1:
	STEPLED=LEDGREENON
else:
	STEPLED=LEDGREENOFF



libSBTCVMsurf=pygame.Surface((324, 243)).convert()
libSBTCVMsurf.fill(TTYBGCOL)
#RAMBANK startup begin
RAMbank = {}

#calmlst = open("ORDEREDLIST6.txt")
screensurf.fill((0,127,255))
screensurf.blit(vmbg, (0, 0))
pygame.display.update()

#ramstart
#for ramadr in libSBTCVM.calmlst:
	#print "foobar"
#	ramadr=ramadr.replace("\n", "")
#	RAMbank[ramadr] = "000000"
	#



IOgen="---------"
RAMbank["---------"] = "000000000"
while IOgen!="+++++++++":
	IOgen=libSBTCVM.trunkto6(libbaltcalc.btadd(IOgen, "+"))
	RAMbank[IOgen] = "000000000"
RAMbank["+++++++++"] = "000000000"


tromready=0
print "waiting for libtrom"
while tromready==0:
	tromready=libtrom.initwait()
	time.sleep(0.1)
print "libtrom ready."	

ttyredraw=1

#IO read only list. IO addresses in this list are treated as read only. for example:
#the random integer port is read only.
IOreadonly=["--0------"]

MONODISPBIG=pygame.transform.scale(MONODISP, (144, 144))
COLORDISPBIG=pygame.transform.scale(COLORDISP, (148, 148))
#RAMBANK startup end
colorreg="++++++"
ROMFILE=TROMA
ROMLAMPFLG="A"
stopflag=0
EXECCHANGE=0
#ROMFILE=open(BOOTUPFILE)
EXECADDR="---------"
contaddr="---------"
EXECADDRfall=0
EXECADDRraw=EXECADDR
REG1="000000000"
REG2="000000000"
#status display optimization.
prevREG1="diff"
prevREG2="diff"
prevEXECADDR="diff"
prevROM="diff"
prevINST="diff"
prevDATA="diff"
regsetpoint="000000000"
updtcdisp=1
updtmdisp=1
updtblits=list()
updtrandport=1
screensurf.blit(CPULEDACT, (749, 505))
screensurf.blit(STEPLED, (750, 512))
print "SBTCVM Mark 2 Ready. the VM will now begin."
while stopflag==0:
	curinst=(libtrom.tromreadinst(EXECADDR,ROMFILE))
	curdata=(libtrom.tromreaddata(EXECADDR,ROMFILE))
	#some screen display stuff & general blitting
	#screensurf.fill((0,127,255))
	#draw Background
	
	if disablereadouts==0 or stepbystep==1:
		#screensurf.blit(vmbg, (0, 0))
		#these show the instruction and data in the instruction/data box :)
		if prevINST!=curinst:
			insttext=smldispfont.render(curinst, True, (0, 255, 255), (0, 0, 0)).convert()
			prevINST=curinst
			upt=screensurf.blit(insttext, (8, 522))
			updtblits.extend([upt])
		if prevDATA!=curdata:
			datatext=smldispfont.render(curdata, True, (0, 255, 127), (0, 0, 0)).convert()
			prevDATA=curdata
			upt=screensurf.blit(datatext, (8, 566))
			updtblits.extend([upt])
		
		#these draw the register displays :)
		if prevREG1!=REG1:
			reg1text=lgdispfont.render(REG1, True, (255, 0, 127), (0, 0, 0)).convert()
			prevREG1=REG1
			upt=screensurf.blit(reg1text, (219, 521))
			updtblits.extend([upt])
		if prevREG2!=REG2:
			reg2text=lgdispfont.render(REG2, True, (255, 127, 0), (0, 0, 0)).convert()
			prevREG2=REG2
			upt=screensurf.blit(reg2text, (219, 564))
			updtblits.extend([upt])
		
		
		#and here is what draws the ROM address display :)
		ROMadrtex=lgdispfont.render(EXECADDR, True, (0, 127, 255), (0, 0, 0)).convert()
		upt=screensurf.blit(ROMadrtex, (425, 564))
		updtblits.extend([upt])
		#and the current rom display :)
		CURROMTEXT=(ROMLAMPFLG)
		if prevROM!=CURROMTEXT:
			curROMtex=lgdispfont.render(CURROMTEXT, True, (255, 0, 255), (0, 0, 0)).convert()
			prevROM=CURROMTEXT
			upt=screensurf.blit(curROMtex, (126, 522))
			updtblits.extend([upt])
	#LED LAMPS
	#CPU
	#screensurf.blit(CPULEDACT, (749, 505))
	#STEP
	
	if updtcdisp==1:
		updtcdisp=0
		upt=screensurf.blit(COLORDISPBIG, (649, 1))
		updtblits.extend([upt])
	if updtmdisp==1:
		updtmdisp=0
		upt=screensurf.blit(MONODISPBIG, (649, 150))
		updtblits.extend([upt])
	#TTY drawer :)
	#for fnx in abt:
	#	fnx=fnx.replace('\n', '')
	#	abttext=simplefont.render(fnx, True, (0, 127, 255), (0, 0, 0))
	#	screensurf.blit(abttext, (45, pixcnt1))
	#	pixcnt1 += pixjmp
	#pixcnt1=40
	if abtpref!=abt or ttyredraw==1:
		abtpref=abt
		ttyredraw=0
		lineq=0
		libSBTCVMsurf.fill(TTYBGCOL)
		for fnx in abt:
			fnx=fnx.replace('\n', '')
			colq=0
			for qlin in fnx:
				#print qlin
				charq=libSBTCVM.charlookupdict.get(qlin)
				#print charq
				libSBTCVM.charblit(libSBTCVMsurf, colq, lineq, charq)
				colq +=1
			lineq +=1
		
		#screensurf.blit(libSBTCVMsurf, (45, 40))
		biglibSBTCVM=pygame.transform.scale(libSBTCVMsurf, (648, 486))
		upt=screensurf.blit(biglibSBTCVM, (0, 0))
		updtblits.extend([upt])
	#aaaaannnnddd update display! :D
	pygame.display.update(updtblits)
	updtblits=list()
	#ROM READ (first register)
	if curinst=="------":
		REG1=(tritlen(libtrom.tromreaddata(curdata,ROMFILE), REG1))
		#print("----")
	#ROM READ (second register)
	elif curinst=="-----0":
		REG2=(tritlen(libtrom.tromreaddata(curdata,ROMFILE), REG2))
		#print("---0")
	#IO READ REG1
	elif curinst=="-----+":
		REG1=tritlen(RAMbank[curdata], REG1)
		if curdata=="--0------":
			updtrandport=1
		#print("---+")
	#IO READ REG2
	elif curinst=="----0-":
		REG2=tritlen(RAMbank[curdata], REG2)
		if curdata=="--0------":
			updtrandport=1
		#print("--0-")
	#IO WRITE REG1
	elif curinst=="----00":
		if curdata not in IOreadonly:
			rambnkcur=RAMbank[curdata]
			RAMbank[curdata] = tritlen(REG1, rambnkcur)
		else:
			print "address \"" + curdata + "\" is read-only."
	#IO WRITE REG2
	elif curinst=="----0+":
		if curdata not in IOreadonly:
			rambnkcur=RAMbank[curdata]
			RAMbank[curdata] = tritlen(REG2, rambnkcur)
		else:
			print "address \"" + curdata + "\" is read-only."
	#swap primary Registers
	elif curinst=="----+-":
		REGTEMP = REG1
		REG1 = REG2
		REG2 = REGTEMP 
	#copy Register 1 to register 2
	elif curinst=="----+0":
		REG2 = REG1
	#copy Register 2 to register 1
	elif curinst=="----++":
		REG1 = REG2
	#invert register 1
	elif curinst=="---0--":
		REG1 = (libbaltcalc.BTINVERT(REG1))
	#invert register 2
	elif curinst=="---0-0":
		REG2 = (libbaltcalc.BTINVERT(REG2))
	#add both registers, load awnser into REG1
	elif curinst=="---0-+":
		#print REG1
		#print REG2
		#print "bla"
		REG1 = (libSBTCVM.trunkto6math(libbaltcalc.btadd(REG1, REG2)))
	#sub both registers, load awnser into REG1
	elif curinst=="---00-":
		REG1 = (libSBTCVM.trunkto6math(libbaltcalc.btsub(REG1, REG2)))
	#mul both registers, load awnser into REG1
	elif curinst=="---000":
		REG1 = (libSBTCVM.trunkto6math(libbaltcalc.btmul(REG1, REG2)))
	#dev both registers, load awnser into REG1
	elif curinst=="---00+":
		REG1 = (libSBTCVM.trunkto6math(libbaltcalc.btdev(REG1, REG2)))
	#set REG1
	elif curinst=="---0+-":
		REG1 = curdata
	#set REG2
	elif curinst=="---0+0":
		REG2 = curdata
	#set inst
	elif curinst=="---0++":
		instsetto=(REG1[0] + REG1[1] + REG1[2] + REG1[3] + REG1[4] + REG1[5])
		libtrom.tromsetinst(curdata, instsetto, ROMFILE)
	#set data
	elif curinst=="---+--":
		libtrom.tromsetdata(curdata, tritlen(REG1, libtrom.tromreaddata(curdata, ROMFILE)), ROMFILE)
	#continue
	elif curinst=="---+++":
		EXECADDRNEXT=contaddr
		EXECCHANGE=1
	#color draw
	elif curinst=="--0---":
		updtcdisp=1
		jx=libSBTCVM.drawnumstruct3((curdata[3] + curdata[4] + curdata[5]))
		jy=libSBTCVM.drawnumstruct3((curdata[6] + curdata[7] + curdata[8]))
		RGBcol=libSBTCVM.colorfind(colorreg)
		#print monocol
		pygame.draw.line(COLORDISP, RGBcol, [jx, jy], [jx, jy], 1)
		COLORDISPBIG=pygame.transform.scale(COLORDISP, (148, 148))
	#set PPU color Register
		
	elif curinst=="--0--0":
		updtcdisp=1
		colorreg=(curdata[3] + curdata[4] + curdata[5] + curdata[6] + curdata[7] + curdata[8])
	elif curinst=="--0--+":
		updtcdisp=1
		RGBcol=libSBTCVM.colorfind((curdata[3] + curdata[4] + curdata[5] + curdata[6] + curdata[7] + curdata[8]))
		#print monocol
		COLORDISP.fill(RGBcol)
		COLORDISPBIG=pygame.transform.scale(COLORDISP, (148, 148))
	#set PPU color vector Register
		
	elif curinst=="--0-0-":
		updtcdisp=1
		colvectorreg=(curdata[3] + curdata[4] + curdata[5] + curdata[6] + curdata[7] + curdata[8])
	elif curinst=="--0-00":
		updtcdisp=1
		#print curdata
		jx=libSBTCVM.drawnumstruct3((curdata[3] + curdata[4] + curdata[5]))
		jy=libSBTCVM.drawnumstruct3((curdata[6] + curdata[7] + curdata[8]))
		kx=libSBTCVM.drawnumstruct3((colvectorreg[0] + colvectorreg[1] + colvectorreg[2]))
		ky=libSBTCVM.drawnumstruct3((colvectorreg[3] + colvectorreg[4] + colvectorreg[5]))
		RGBcol=libSBTCVM.colorfind(colorreg)
		#print monocol
		pygame.draw.line(COLORDISP, RGBcol, [jx, jy], [kx, ky], 1)
		COLORDISPBIG=pygame.transform.scale(COLORDISP, (148, 148))
	#color draw rect
	elif curinst=="--0-0+":
		updtcdisp=1
		#print curdata
		jx=libSBTCVM.drawnumstruct3((curdata[3] + curdata[4] + curdata[5]))
		jy=libSBTCVM.drawnumstruct3((curdata[6] + curdata[7] + curdata[8]))
		kx=libSBTCVM.drawnumstruct3((colvectorreg[0] + colvectorreg[1] + colvectorreg[2]))
		ky=libSBTCVM.drawnumstruct3((colvectorreg[3] + colvectorreg[4] + colvectorreg[5]))
		RGBcol=libSBTCVM.colorfind(colorreg)
		#print monocol
		#pygame.draw.line(COLORDISP, RGBcol, [jx, jy], [kx, ky], 1)
		COLORDISP.fill(RGBcol, (libSBTCVM.makerectbipoint(jx, jy, kx, ky)))
		COLORDISPBIG=pygame.transform.scale(COLORDISP, (148, 148))
	
	#mono draw
	#mono draw pixel
	elif curinst=="--0-+-":
		updtmdisp=1
		jx=libSBTCVM.drawnumstruct2((curdata[3] + curdata[4]))
		jy=libSBTCVM.drawnumstruct2((curdata[5] + curdata[6]))
		monocol=(int(libSBTCVM.dollytell((curdata[7] + curdata[8]))))
		#print monocol
		pygame.draw.line(MONODISP, (monocol, monocol, monocol), [jx, jy], [jx, jy], 1)
		MONODISPBIG=pygame.transform.scale(MONODISP, (144, 144))
	#mono fill
	elif curinst=="--0-+0":
		updtmdisp=1
		monocol=(int(libSBTCVM.dollytell((curdata[7] + curdata[8]))))
		#print monocol
		MONODISP.fill((monocol, monocol, monocol))
		MONODISPBIG=pygame.transform.scale(MONODISP, (144, 144))
	#set PPU mono vector Register
	elif curinst=="--0-++":
		updtmdisp=1
		monovectorreg=(curdata[3] + curdata[4] + curdata[5] + curdata[6] + curdata[7] + curdata[8])
	#draw mono line
	elif curinst=="--00--":
		updtmdisp=1
		jx=libSBTCVM.drawnumstruct2((curdata[3] + curdata[4]))
		jy=libSBTCVM.drawnumstruct2((curdata[5] + curdata[6]))
		kx=libSBTCVM.drawnumstruct2((monovectorreg[0] + monovectorreg[1]))
		ky=libSBTCVM.drawnumstruct2((monovectorreg[2] + monovectorreg[3]))
		monocol=(int(libSBTCVM.dollytell((curdata[7] + curdata[8]))))
		#print monocol
		pygame.draw.line(MONODISP, (monocol, monocol, monocol), [jx, jy], [kx, ky], 1)
		MONODISPBIG=pygame.transform.scale(MONODISP, (144, 144))
	#mono draw rect
	elif curinst=="--00-0":
		updtmdisp=1
		jx=libSBTCVM.drawnumstruct2((curdata[3] + curdata[4]))
		jy=libSBTCVM.drawnumstruct2((curdata[5] + curdata[6]))
		kx=libSBTCVM.drawnumstruct2((monovectorreg[0] + monovectorreg[1]))
		ky=libSBTCVM.drawnumstruct2((monovectorreg[2] + monovectorreg[3]))
		monocol=(int(libSBTCVM.dollytell((curdata[7] + curdata[8]))))
		#print monocol
		#pygame.draw.line(MONODISP, (monocol, monocol, monocol), [jx, jy], [kx, ky], 1)
		MONODISP.fill((monocol, monocol, monocol), (libSBTCVM.makerectbipoint(jx, jy, kx, ky)))
		MONODISPBIG=pygame.transform.scale(MONODISP, (144, 144))
	#SHUTDOWN VM
	elif curinst=="--000-":
		stopflag=1
		abt=libSBTCVM.abtslackline(abt, "VM SYSHALT:")
		abt=libSBTCVM.abtslackline(abt, "soft stop.")
		ttyredraw=1
	#NULL INSTRUCTION (DOES NOTHING) USE WHEN YOU WISH TO DO NOTHING :p
	#elif curinst=="--0000":
		#commented out due to doing nothing.
		#print("")
	#goto rom adress specified by CURRENT DATA
	elif curinst=="--000+":
		EXECADDRNEXT=curdata
		EXECCHANGE=1
	#goto rom adress specified by Register 1
	elif curinst=="--00+-":
		EXECADDRNEXT=REG1
		EXECCHANGE=1
	
	elif curinst=="--00+0":
		if REG1==REG2:
			EXECADDRNEXT=curdata
			EXECCHANGE=1
	elif curinst=="--00++":
		waitchop=curdata[5]
		if waitchop=="+":
			waitmagn=0.3
		elif waitchop=="-":
			waitmagn=0.1
		else:
			waitmagn=0.2
		time.sleep(( waitmagn))
	#asks user if goto to adress is desired
	elif curinst=="--0+--":
		abt=libSBTCVM.abtslackline(abt, ("GOTO: (" + curdata + ") Y or N?"))
		ttyredraw=1
		USRYN=1
		extradraw=1	
	#user wait
	elif curinst=="--0+-0":
		abt=libSBTCVM.abtslackline(abt, ("Press enter to continue."))
		ttyredraw=1
		USRWAIT=1
		extradraw=1	
	#TTY clear
	elif curinst=="--0+-+":
		abt=["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
	#Goto data if Reg 1 greater
	elif curinst=="--0+0-":
		if libbaltcalc.BTTODEC(REG1)>libbaltcalc.BTTODEC(REG2):
			EXECADDRNEXT=curdata
			EXECCHANGE=1
	
	
	#note these swap TROMS
	#TROMA: goto rom adress on TROMA specified by CURRENT DATA
	elif curinst=="--+---":
		EXECADDRNEXT=curdata
		EXECCHANGE=1
		ROMFILE=TROMA
		ROMLAMPFLG="A"
	#conditional GOTO
	elif curinst=="--+--0":
		if REG1==REG2:
			EXECADDRNEXT=curdata
			EXECCHANGE=1
			ROMFILE=TROMA
			ROMLAMPFLG="A"
	#TROMB: goto rom adress on TROMB specified by CURRENT DATA
	elif curinst=="--+--+":
		EXECADDRNEXT=curdata
		EXECCHANGE=1
		ROMFILE=TROMB
		ROMLAMPFLG="B"
	elif curinst=="--+-0-":
		if REG1==REG2:
			EXECADDRNEXT=curdata
			EXECCHANGE=1
			ROMFILE=TROMB
			ROMLAMPFLG="B"
	#TROMC: goto rom adress on TROMC specified by CURRENT DATA
	elif curinst=="--+-00":
		EXECADDRNEXT=curdata
		EXECCHANGE=1
		ROMFILE=TROMC
		ROMLAMPFLG="C"
	#conditional GOTO
	elif curinst=="--+-0+":
		if REG1==REG2:
			EXECADDRNEXT=curdata
			EXECCHANGE=1
			ROMFILE=TROMC
			ROMLAMPFLG="C"
	#TROMD: goto rom adress on TROMD specified by CURRENT DATA
	elif curinst=="--+-+-":
		EXECADDRNEXT=curdata
		EXECCHANGE=1
		ROMFILE=TROMD
		ROMLAMPFLG="D"
	#conditional GOTO
	elif curinst=="--+-+0":
		if REG1==REG2:
			EXECADDRNEXT=curdata
			EXECCHANGE=1
			ROMFILE=TROMD
			ROMLAMPFLG="D"
	#TROME: goto rom adress on TROME specified by CURRENT DATA
	elif curinst=="--+-++":
		EXECADDRNEXT=curdata
		EXECCHANGE=1
		ROMFILE=TROME
		ROMLAMPFLG="E"
	#conditional GOTO
	elif curinst=="--+0--":
		if REG1==REG2:
			EXECADDRNEXT=curdata
			EXECCHANGE=1
			ROMFILE=TROME
			ROMLAMPFLG="E"
	#TROMF: goto rom adress on TROMF specified by CURRENT DATA
	elif curinst=="--+0-0":
		EXECADDRNEXT=curdata
		EXECCHANGE=1
		ROMFILE=TROMF
		ROMLAMPFLG="F"
	#conditional GOTO
	elif curinst=="--+0-+":
		if REG1==REG2:
			EXECADDRNEXT=curdata
			EXECCHANGE=1
			ROMFILE=TROMF
			ROMLAMPFLG="F"
	
	
	#dump register 1 to TTY
	elif curinst=="--++0+":
		print ("REG1 DUMP:" + REG1 + " " + str(libbaltcalc.BTTODEC(REG1)))
		ttyredraw=1
		abt=libSBTCVM.abtslackline(abt, ("REG1 DUMP:" + REG1 + " " + str(libbaltcalc.BTTODEC(REG1))))
	#dump Register 2 to TTY
	elif curinst=="--+++-":
		print ("REG2 DUMP:" + REG2 + " " + str(libbaltcalc.BTTODEC(REG2)))
		ttyredraw=1
		abt=libSBTCVM.abtslackline(abt, ("REG2 DUMP:" + REG2 + " " + str(libbaltcalc.BTTODEC(REG2))))
	#tty write port (direct)
	elif curinst=="--+++0":
		abt=libSBTCVM.abtcharblit(abt, (libSBTCVM.charcodelook((curdata[3] + curdata[4] + curdata[5] + curdata[6] + curdata[7] + curdata[8]))))
		if TTYrenderflg=="0":
			ttyredraw=1
		else:
			if libSBTCVM.getnewlstate()==1:
				ttyredraw=1
			
	#Buzzer (direct)
	elif curinst=="--++++":
		snf.stop()
		#print "derp"
		wavsp=libSBTCVM.mk1buzz((curdata[3] + curdata[4] + curdata[5] + curdata[6] + curdata[7] + curdata[8]))
		snf=pygame.mixer.Sound(wavsp)
		snf.play()
		timechop=curdata[0]
		if timechop=="+":
			time.sleep(0.3)
		elif timechop=="-":
			time.sleep(0.1)
		else:
			time.sleep(0.2)
	#set regset pointer
	elif curinst=="-0-000":
		regsetpoint=curdata
	#regset
	elif curinst=="-0-00+":
		if regsetpoint=="---------":
			TTYBGCOLREG=(curdata[3] + curdata[4] + curdata[5] + curdata[6] + curdata[7] + curdata[8])
			TTYBGCOL=libSBTCVM.colorfind(TTYBGCOLREG)
			ttyredraw=1
		if regsetpoint=="--------0":
			TTYrenderflg=curdata[8]
			if TTYrenderflg=="-":
				TTYrenderflg="0"
	#offset length
	elif curinst=="-0-++0":
		offlen1=(curdata[7] + curdata[8])
		offlen2=(curdata[5] + curdata[6])
		offlen3=(curdata[4])
		if offlen3=="+":
			tritdestgnd=1
		else:
			tritdestgnd=0
		if offlen2=="--":
			tritoffset=0
		elif offlen2=="-0":
			tritoffset=1
		elif offlen2=="-+":
			tritoffset=2
		elif offlen2=="0-":
			tritoffset=3
		elif offlen2=="00":
			tritoffset=4
		elif offlen2=="0+":
			tritoffset=5
		elif offlen2=="+-":
			tritoffset=6
		elif offlen2=="+0":
			tritoffset=7
		elif offlen2=="++":
			tritoffset=8
		
		if offlen1=="--":
			tritloadlen=1
		elif offlen1=="-0":
			tritloadlen=2
		elif offlen1=="-+":
			tritloadlen=3
		elif offlen1=="0-":
			tritloadlen=4
		elif offlen1=="00":
			tritloadlen=5
		elif offlen1=="0+":
			tritloadlen=6
		elif offlen1=="+-":
			tritloadlen=7
		elif offlen1=="+0":
			tritloadlen=8
		elif offlen1=="++":
			tritloadlen=9
	
	
	
	
	#set ketinterupt register
	elif curinst=="-0-+++":
		keyintreg=(curdata[5] + curdata[6] + curdata[7] + curdata[8])
	#keyinterupt activate
	elif curinst=="-00---":
		if keyintreg=="----":
			key1=1
			key1adr=curdata
		if keyintreg=="---0":
			key2=1
			key2adr=curdata
		if keyintreg=="---+":
			key3=1
			key3adr=curdata
		if keyintreg=="--0-":
			key4=1
			key4adr=curdata
		if keyintreg=="--00":
			key5=1
			key5adr=curdata
		if keyintreg=="--0+":
			key6=1
			key6adr=curdata
		if keyintreg=="--+-":
			key7=1
			key7adr=curdata
		if keyintreg=="--+0":
			key8=1
			key8adr=curdata
		if keyintreg=="--++":
			key9=1
			key9adr=curdata
		if keyintreg=="-0--":
			key0=1
			key0adr=curdata
		if keyintreg=="-0-0":
			keyhyp=1
			keyhypadr=curdata
		if keyintreg=="-0-+":
			keypos=1
			keyposadr=curdata
		if keyintreg=="-00-":
			keya=1
			keyaadr=curdata
		if keyintreg=="-000":
			keyb=1
			keybadr=curdata
		if keyintreg=="-00+":
			keyc=1
			keycadr=curdata
		if keyintreg=="-0+-":
			keyd=1
			keydadr=curdata
		if keyintreg=="-0+0":
			keye=1
			keyeadr=curdata
		if keyintreg=="-0++":
			keyf=1
			keyfadr=curdata
		if keyintreg=="-+--":
			keyg=1
			keygadr=curdata
		if keyintreg=="-+-0":
			keyh=1
			keyhadr=curdata
		if keyintreg=="-+-+":
			keyi=1
			keyiadr=curdata
		if keyintreg=="-+0-":
			keyj=1
			keyjadr=curdata
		if keyintreg=="-+00":
			keyk=1
			keykadr=curdata
		if keyintreg=="-+0+":
			keyl=1
			keyladr=curdata
		if keyintreg=="-++-":
			keym=1
			keymadr=curdata
		if keyintreg=="-++0":
			keyn=1
			keynadr=curdata
		if keyintreg=="-+++":
			keyo=1
			keyoadr=curdata
		if keyintreg=="0---":
			keyp=1
			keypadr=curdata
		if keyintreg=="0--0":
			keyq=1
			keyqadr=curdata
		if keyintreg=="0--+":
			keyr=1
			keyradr=curdata
		if keyintreg=="0-0-":
			keysx=1
			keysadr=curdata
		if keyintreg=="0-00":
			keyt=1
			keytadr=curdata
		if keyintreg=="0-0+":
			keyu=1
			keyuadr=curdata
		if keyintreg=="0-+-":
			keyv=1
			keyvadr=curdata
		if keyintreg=="0-+0":
			keyw=1
			keywadr=curdata
		if keyintreg=="0-++":
			keyx=1
			keyxadr=curdata
		if keyintreg=="00--":
			keyy=1
			keyyadr=curdata
		if keyintreg=="00-0":
			keyz=1
			keyzadr=curdata
		if keyintreg=="00-+":
			keyspace=1
			keyspaceadr=curdata
		if keyintreg=="000-":
			keyret=1
			keyretadr=curdata
		
		
		
		
	#clear keyinterupt
	elif curinst=="-00--0":
		if curdata[8]=="+":
			key1=0
			key2=0
			key3=0
			key4=0
			key5=0
			key6=0
			key7=0
			key8=0
			key9=0
			key0=0
			keypos=0
			keyhyp=0
			keyq=0
			keyw=0
			keye=0
			keyr=0
			keyt=0
			keyy=0
			keyu=0
			keyi=0
			keyo=0
			keyp=0
			keya=0
			keysx=0
			keyd=0
			keyf=0
			keyg=0
			keyh=0
			keyj=0
			keyk=0
			keyl=0
			keyz=0
			keyx=0
			keyc=0
			keyv=0
			keyb=0
			keyn=0
			keym=0
			keyspace=0
			keyret=0
		else:
			if keyintreg=="----":
				key1=0
			if keyintreg=="---0":
				key2=0
			if keyintreg=="---+":
				key3=0
			if keyintreg=="--0-":
				key4=0
			if keyintreg=="--00":
				key5=0
			if keyintreg=="--0+":
				key6=0
			if keyintreg=="--+-":
				key7=0
			if keyintreg=="--+0":
				key8=0
			if keyintreg=="--++":
				key9=0
			if keyintreg=="-0--":
				key0=0
			if keyintreg=="-0-0":
				keyhyp=0
			if keyintreg=="-0-+":
				keypos=0
			if keyintreg=="-00-":
				keya=0
			if keyintreg=="-000":
				keyb=0
			if keyintreg=="-00+":
				keyc=0
			if keyintreg=="-0+-":
				keyd=0
			if keyintreg=="-0+0":
				keye=0
			if keyintreg=="-0++":
				keyf=0
			if keyintreg=="-+--":
				keyg=0
			if keyintreg=="-+-0":
				keyh=0
			if keyintreg=="-+-+":
				keyi=0
			if keyintreg=="-+0-":
				keyj=0
			if keyintreg=="-+00":
				keyk=0
			if keyintreg=="-+0+":
				keyl=0
			if keyintreg=="-++-":
				keym=0
			if keyintreg=="-++0":
				keyn=0
			if keyintreg=="-+++":
				keyo=0
			if keyintreg=="0---":
				keyp=0
			if keyintreg=="0--0":
				keyq=0
			if keyintreg=="0--+":
				keyr=0
			if keyintreg=="0-0-":
				keysx=0
			if keyintreg=="0-00":
				keyt=0
			if keyintreg=="0-0+":
				keyu=0
			if keyintreg=="0-+-":
				keyv=0
			if keyintreg=="0-+0":
				keyw=0
			if keyintreg=="0-++":
				keyx=0
			if keyintreg=="00--":
				keyy=0
			if keyintreg=="00-0":
				keyz=0
			if keyintreg=="00-+":
				keyspace=0
			if keyintreg=="000-":
				keyret=0
		
		
	#NULL INSTRUCTION (new variant) (compilers should use this in place of the legacy code.)
	#elif curinst=="000000":
	#	
	#	print("")
	if updtrandport==1:
		updtrandport=0
		RAMbank["--0------"]=libSBTCVM.trunkto6(libbaltcalc.DECTOBT(randint(-9841,9841)))
	
	
	
	#needed by user quering opcodes such as 0+--	
	if extradraw==1:
		#screensurf.blit(vmbg, (0, 0))
		#these show the instruction and data in the instruction/data box :)
		insttext=smldispfont.render(curinst, True, (0, 255, 255), (0, 0, 0))
		datatext=smldispfont.render(curdata, True, (0, 255, 127), (0, 0, 0))
		screensurf.blit(insttext, (8, 522))
		screensurf.blit(datatext, (8, 566))
		#these draw the register displays :)
		reg1text=lgdispfont.render(REG1, True, (255, 0, 127), (0, 0, 0))
		reg2text=lgdispfont.render(REG2, True, (255, 127, 0), (0, 0, 0))
		screensurf.blit(reg1text, (219, 521))
		screensurf.blit(reg2text, (219, 564))
		#and here is what draws the ROM address display :)
		ROMadrtex=lgdispfont.render(EXECADDR, True, (0, 127, 255), (0, 0, 0))
		screensurf.blit(ROMadrtex, (425, 564))
		#and the current rom display :)
		CURROMTEXT=(ROMLAMPFLG)
		curROMtex=lgdispfont.render(CURROMTEXT, True, (255, 0, 255), (0, 0, 0))
		screensurf.blit(curROMtex, (126, 522))
		#LED LAMPS
		#CPU
		screensurf.blit(CPULEDACT, (749, 505))
		#STEP
		screensurf.blit(STEPLED, (750, 512))
		screensurf.blit(COLORDISPBIG, (649, 1))
		screensurf.blit(MONODISPBIG, (649, 150))
		#TTY drawer :)
		#for fnx in abt:
		#	fnx=fnx.replace('\n', '')
		#	abttext=simplefont.render(fnx, True, (0, 127, 255), (0, 0, 0))
		#	screensurf.blit(abttext, (45, pixcnt1))
		#	pixcnt1 += pixjmp
		#pixcnt1=40
		lineq=0
		
		libSBTCVMsurf.fill(TTYBGCOL)
		for fnx in abt:
			fnx=fnx.replace('\n', '')
			colq=0
			for qlin in fnx:
				#print qlin
				charq=libSBTCVM.charlookupdict.get(qlin)
				#print charq
				libSBTCVM.charblit(libSBTCVMsurf, colq, lineq, charq)
				colq +=1
			lineq +=1
		if tuibig==0:
			screensurf.blit(libSBTCVMsurf, (45, 40))
		else:
			biglibSBTCVM=pygame.transform.scale(libSBTCVMsurf, (648, 486))
			screensurf.blit(biglibSBTCVM, (0, 0))
		pygame.display.update()
		#abt=libSBTCVM.abtslackline(abt, jline)
		extradraw=0
	if USRWAIT==1:
		evhappenflg2=0
		while evhappenflg2==0:
			time.sleep(.1)
			for event in pygame.event.get():
				if event.type == KEYDOWN and event.key == K_RETURN:
					evhappenflg2=1
					break
				if event.type == KEYDOWN and event.key == K_ESCAPE:
					evhappenflg2=1
					stopflag=1
					abt=libSBTCVM.abtslackline(abt, "")
					abt=libSBTCVM.abtslackline(abt, "VM SYSHALT:")
					abt=libSBTCVM.abtslackline(abt, "User stop.")
					break
				if event.type == KEYDOWN and event.key == K_F7:
					pygame.image.save(COLORDISP, (os.path.join('CAP', 'COLORDISP-OUT.png')))
					pygame.image.save(MONODISP, (os.path.join('CAP', 'MONODISP-OUT.png')))
					break
				if event.type == KEYDOWN and event.key == K_F8:
					pygame.image.save(screensurf, (os.path.join('CAP', 'SCREENSHOT.png')))
					break
				if event.type == KEYDOWN and event.key == K_F2:
					stepbystep=1
					STEPLED=LEDGREENON
					upt=screensurf.blit(STEPLED, (750, 512))
					updtblits.extend([upt])
					break
				if event.type == KEYDOWN and event.key == K_F10:
					ramdmp=open((os.path.join('CAP', 'IOBUSman.dmp')),  'w')
					for IOitm in RAMbank:
						ramdmp.write("A:" + str(IOitm) + " D:" + RAMbank[IOitm] + "\n")
					ramdmp.close()
					libtrom.manualdumptroms()
					break
				if event.type == KEYDOWN and event.key == K_F4:
					if disablereadouts==1:
						disablereadouts=0
						print "readouts enabled"
					elif disablereadouts==0:
						print "readouts disabled"
						disablereadouts=1
					#STEPLED=LEDGREENON
					break
		abt=libSBTCVM.abtslackline(abt, ("\n"))
		USRWAIT=0
	
	
	if USRYN==1:
		evhappenflg2=0
		while evhappenflg2==0:
			time.sleep(.1)
			for event in pygame.event.get():
				if event.type == KEYDOWN and event.key == K_y:
					EXECADDRNEXT=curdata
					EXECCHANGE=1
					evhappenflg2=1
					break
				if event.type == KEYDOWN and event.key == K_n:
					evhappenflg2=1
					break
				if event.type == KEYDOWN and event.key == K_ESCAPE:
					evhappenflg2=1
					stopflag=1
					abt=libSBTCVM.abtslackline(abt, "")
					abt=libSBTCVM.abtslackline(abt, "VM SYSHALT:")
					abt=libSBTCVM.abtslackline(abt, "User stop.")
					break
				if event.type == KEYDOWN and event.key == K_F7:
					pygame.image.save(COLORDISP, (os.path.join('CAP', 'COLORDISP-OUT.png')))
					pygame.image.save(MONODISP, (os.path.join('CAP', 'MONODISP-OUT.png')))
					break
				if event.type == KEYDOWN and event.key == K_F8:
					pygame.image.save(screensurf, (os.path.join('CAP', 'SCREENSHOT.png')))
					break
				if event.type == KEYDOWN and event.key == K_F2:
					stepbystep=1
					STEPLED=LEDGREENON
					upt=screensurf.blit(STEPLED, (750, 512))
					updtblits.extend([upt])
					break
				if event.type == KEYDOWN and event.key == K_F10:
					ramdmp=open((os.path.join('CAP', 'IOBUSman.dmp')),  'w')
					for IOitm in RAMbank:
						ramdmp.write("A:" + str(IOitm) + " D:" + RAMbank[IOitm] + "\n")
					ramdmp.close()
					libtrom.manualdumptroms()
					break
				if event.type == KEYDOWN and event.key == K_F4:
					if disablereadouts==1:
						disablereadouts=0
						print "readouts enabled"
					elif disablereadouts==0:
						print "readouts disabled"
						disablereadouts=1
					#STEPLED=LEDGREENON
					break
		abt=libSBTCVM.abtslackline(abt, ("\n"))
		USRYN=0
	
	#print(EXECADDR)
	if stepbystep==1:
		#this is used when step-by-step mode is enabled
		evhappenflg2=0
		while evhappenflg2==0:
			time.sleep(.1)
			for event in pygame.event.get():
				if event.type == KEYDOWN and event.key == K_RETURN:
					evhappenflg2=1
					break
				if event.type == KEYDOWN and event.key == K_ESCAPE:
					stopflag=1
					
					abt=libSBTCVM.abtslackline(abt, "VM SYSHALT:")
					abt=libSBTCVM.abtslackline(abt, "User stop.")
					evhappenflg2=1
					break
				if event.type == KEYDOWN and event.key == K_F7:
					pygame.image.save(COLORDISP, (os.path.join('CAP', 'COLORDISP-OUT.png')))
					pygame.image.save(MONODISP, (os.path.join('CAP', 'MONODISP-OUT.png')))
					break
				if event.type == KEYDOWN and event.key == K_F8:
					pygame.image.save(screensurf, (os.path.join('CAP', 'SCREENSHOT.png')))
					break
				if event.type == KEYDOWN and event.key == K_F2:
					stepbystep=0
					STEPLED=LEDGREENOFF
					upt=screensurf.blit(STEPLED, (750, 512))
					updtblits.extend([upt])
					evhappenflg2=1
					break
				if event.type == KEYDOWN and event.key == K_F10:
					ramdmp=open((os.path.join('CAP', 'IOBUSman.dmp')),  'w')
					for IOitm in RAMbank:
						ramdmp.write("A:" + str(IOitm) + " D:" + RAMbank[IOitm] + "\n")
					ramdmp.close()
					libtrom.manualdumptroms()
					break
				
		
	else:
		#...otherwise this is used to passivly check for imput
		for event in pygame.event.get():
			if event.type == KEYDOWN and event.key == K_ESCAPE:
				stopflag=1
				abt=libSBTCVM.abtslackline(abt, "VM SYSHALT:")
				abt=libSBTCVM.abtslackline(abt, "User stop.")
				break
			if event.type == KEYDOWN and event.key == K_F7:
				pygame.image.save(COLORDISP, (os.path.join('CAP', 'COLORDISP-OUT.png')))
				pygame.image.save(MONODISP, (os.path.join('CAP', 'MONODISP-OUT.png')))
				break
			if event.type == KEYDOWN and event.key == K_F8:
				pygame.image.save(screensurf, (os.path.join('CAP', 'SCREENSHOT.png')))
				break
			if event.type == KEYDOWN and event.key == K_F10:
				ramdmp=open((os.path.join('CAP', 'IOBUSman.dmp')),  'w')
				for IOitm in RAMbank:
					ramdmp.write("A:" + str(IOitm) + " D:" + RAMbank[IOitm] + "\n")
				ramdmp.close()
				libtrom.manualdumptroms()
				break
			if event.type == KEYDOWN and event.key == K_F2:
				stepbystep=1
				STEPLED=LEDGREENON
				upt=screensurf.blit(STEPLED, (750, 512))
				updtblits.extend([upt])
				break
			if event.type == KEYDOWN and event.key == K_F4:
				if disablereadouts==1:
					disablereadouts=0
					print "readouts enabled"
				elif disablereadouts==0:
					print "readouts disabled"
					disablereadouts=1
				#STEPLED=LEDGREENON
				break
			if event.type == KEYDOWN and (event.key == K_1 or event.key == K_KP1) and key1 == 1:
				EXECADDRNEXT=key1adr
				EXECCHANGE=1
				break
			if event.type == KEYDOWN and (event.key == K_2 or event.key == K_KP2) and key2 == 1:
				EXECADDRNEXT=key2adr
				EXECCHANGE=1
				break
			if event.type == KEYDOWN and (event.key == K_3 or event.key == K_KP3) and key3 == 1:
				EXECADDRNEXT=key3adr
				EXECCHANGE=1
				break
			if event.type == KEYDOWN and (event.key == K_4 or event.key == K_KP4) and key4 == 1:
				EXECADDRNEXT=key4adr
				EXECCHANGE=1
				break
			if event.type == KEYDOWN and (event.key == K_5 or event.key == K_KP5) and key5 == 1:
				EXECADDRNEXT=key5adr
				EXECCHANGE=1
				break
			if event.type == KEYDOWN and (event.key == K_6 or event.key == K_KP6) and key6 == 1:
				EXECADDRNEXT=key6adr
				EXECCHANGE=1
				break
			if event.type == KEYDOWN and (event.key == K_7 or event.key == K_KP7) and key7 == 1:
				EXECADDRNEXT=key7adr
				EXECCHANGE=1
				break
			if event.type == KEYDOWN and (event.key == K_8 or event.key == K_KP8) and key8 == 1:
				EXECADDRNEXT=key8adr
				EXECCHANGE=1
				break
			if event.type == KEYDOWN and (event.key == K_9 or event.key == K_KP9) and key9 == 1:
				EXECADDRNEXT=key9adr
				EXECCHANGE=1
				break
			if event.type == KEYDOWN and (event.key == K_0 or event.key == K_KP0) and key0 == 1:
				EXECADDRNEXT=key0adr
				EXECCHANGE=1
				break
			if event.type == KEYDOWN and (event.key == K_MINUS or event.key == K_UNDERSCORE or event.key == K_KP_MINUS) and keyhyp == 1:
				EXECADDRNEXT=keyhypadr
				EXECCHANGE=1
				break
			if event.type == KEYDOWN and (event.key == K_PLUS or event.key == K_EQUALS or event.key == K_KP_PLUS) and keypos == 1:
				EXECADDRNEXT=keyposadr
				EXECCHANGE=1
				break
			if event.type == KEYDOWN and event.key == K_a and keya == 1:
				EXECADDRNEXT=keyaadr
				EXECCHANGE=1
				break
			if event.type == KEYDOWN and event.key == K_b and keyb == 1:
				EXECADDRNEXT=keybadr
				EXECCHANGE=1
				break
			if event.type == KEYDOWN and event.key == K_c and keyc == 1:
				EXECADDRNEXT=keycadr
				EXECCHANGE=1
				break
			if event.type == KEYDOWN and event.key == K_d and keyd == 1:
				EXECADDRNEXT=keydadr
				EXECCHANGE=1
				break
			if event.type == KEYDOWN and event.key == K_e and keye == 1:
				EXECADDRNEXT=keyeadr
				EXECCHANGE=1
				break
			if event.type == KEYDOWN and event.key == K_f and keyf == 1:
				EXECADDRNEXT=keyfadr
				EXECCHANGE=1
				break
			if event.type == KEYDOWN and event.key == K_g and keyg == 1:
				EXECADDRNEXT=keygadr
				EXECCHANGE=1
				break
			if event.type == KEYDOWN and event.key == K_h and keyh == 1:
				EXECADDRNEXT=keyhadr
				EXECCHANGE=1
				break
			if event.type == KEYDOWN and event.key == K_i and keyi == 1:
				EXECADDRNEXT=keyiadr
				EXECCHANGE=1
				break
			if event.type == KEYDOWN and event.key == K_j and keyj == 1:
				EXECADDRNEXT=keyjadr
				EXECCHANGE=1
				break
			if event.type == KEYDOWN and event.key == K_k and keyk == 1:
				EXECADDRNEXT=keykadr
				EXECCHANGE=1
				break
			if event.type == KEYDOWN and event.key == K_l and keyl == 1:
				EXECADDRNEXT=keyladr
				EXECCHANGE=1
				break
			if event.type == KEYDOWN and event.key == K_m and keym == 1:
				EXECADDRNEXT=keymadr
				EXECCHANGE=1
				break
			if event.type == KEYDOWN and event.key == K_n and keyn == 1:
				EXECADDRNEXT=keynadr
				EXECCHANGE=1
				break
			if event.type == KEYDOWN and event.key == K_o and keyo == 1:
				EXECADDRNEXT=keyoadr
				EXECCHANGE=1
				break
			if event.type == KEYDOWN and event.key == K_p and keyp == 1:
				EXECADDRNEXT=keypadr
				EXECCHANGE=1
				break
			if event.type == KEYDOWN and event.key == K_q and keyq == 1:
				EXECADDRNEXT=keyqadr
				EXECCHANGE=1
				break
			if event.type == KEYDOWN and event.key == K_r and keyr == 1:
				EXECADDRNEXT=keyradr
				EXECCHANGE=1
				break
			if event.type == KEYDOWN and event.key == K_s and keysx == 1:
				EXECADDRNEXT=keysadr
				EXECCHANGE=1
				break
			if event.type == KEYDOWN and event.key == K_t and keyt == 1:
				EXECADDRNEXT=keytadr
				EXECCHANGE=1
				break
			if event.type == KEYDOWN and event.key == K_u and keyu == 1:
				EXECADDRNEXT=keyuadr
				EXECCHANGE=1
				break
			if event.type == KEYDOWN and event.key == K_v and keyv == 1:
				EXECADDRNEXT=keyvadr
				EXECCHANGE=1
				break
			if event.type == KEYDOWN and event.key == K_w and keyw == 1:
				EXECADDRNEXT=keywadr
				EXECCHANGE=1
				break
			if event.type == KEYDOWN and event.key == K_x and keyx == 1:
				EXECADDRNEXT=keyxadr
				EXECCHANGE=1
				break
			if event.type == KEYDOWN and event.key == K_y and keyy == 1:
				EXECADDRNEXT=keyyadr
				EXECCHANGE=1
				break
			if event.type == KEYDOWN and event.key == K_z and keyz == 1:
				EXECADDRNEXT=keyzadr
				EXECCHANGE=1
				break
			if event.type == KEYDOWN and event.key == K_SPACE and keyspace == 1:
				EXECADDRNEXT=keyspaceadr
				EXECCHANGE=1
				break
			if event.type == KEYDOWN and (event.key == K_RETURN or event.key == K_KP_ENTER) and keyret == 1:
				EXECADDRNEXT=keyretadr
				EXECCHANGE=1
				break
			
	#pygame.event.clear()
	
	
	
	#aaaaannnnddd update display! :D
	pygame.display.update()
	
	if curinst=="--":
		stopflag=1
		abt=libSBTCVM.abtslackline(abt, "VM SYSHALT:")
		abt=libSBTCVM.abtslackline(abt, "End Of Rom.")
	#check the current rom. 
	if EXECADDRraw=="+------":
		topflag=1
		abt=libSBTCVM.abtslackline(abt, "VM SYSHALT:")
		abt=libSBTCVM.abtslackline(abt, "End Of RomBus.")
	#print "eek " + EXECADDRNEXT
	EXECADDR=libbaltcalc.btadd(EXECADDR, "+")
	EXECADDRraw=EXECADDR
	#print EXECADDR
	EXECADDR=libSBTCVM.trunkto6(EXECADDR)
	#print "ook " + EXECADDRNEXT
	if EXECCHANGE==1:
		EXECCHANGE=0
		#print("ding")
		contaddr=EXECADDR
		EXECADDR=EXECADDRNEXT
		EXECADDRraw=EXECADDR
		#print EXECADDR
	if stopflag==1:
		abt=libSBTCVM.abtslackline(abt, "Press enter to exit.")
		#screensurf.fill((0,127,255))
		#screensurf.blit(vmbg, (0, 0))
	
		#these show the instruction and data in the instruction/data box :)
		insttext=smldispfont.render(curinst, True, (0, 255, 255), (0, 0, 0))
		datatext=smldispfont.render(curdata, True, (0, 255, 127), (0, 0, 0))
		screensurf.blit(insttext, (8, 522))
		screensurf.blit(datatext, (8, 566))
		#these draw the register displays :)
		reg1text=lgdispfont.render(REG1, True, (255, 0, 127), (0, 0, 0))
		reg2text=lgdispfont.render(REG2, True, (255, 127, 0), (0, 0, 0))
		screensurf.blit(reg1text, (219, 521))
		screensurf.blit(reg2text, (219, 564))
		#and here is what draws the ROM address display :)
		ROMadrtex=lgdispfont.render(EXECADDR, True, (0, 127, 255), (0, 0, 0))
		screensurf.blit(ROMadrtex, (425, 564))
		#and the current rom display :)
		CURROMTEXT=(ROMLAMPFLG)
		curROMtex=lgdispfont.render(CURROMTEXT, True, (255, 0, 255), (0, 0, 0))
		screensurf.blit(curROMtex, (126, 522))
		#LED LAMPS
		screensurf.blit(CPULEDSTANDBY, (749, 505))
		#STEP
		screensurf.blit(STEPLED, (750, 512))
		screensurf.blit(COLORDISPBIG, (649, 1))
		screensurf.blit(MONODISPBIG, (649, 150))
		CURROMTEXT=("ROM " + ROMLAMPFLG)
		reg2text=lgdispfont.render(CURROMTEXT, True, (255, 0, 255), (0, 0, 0))
		#screensurf.blit(reg2text, (558, 198))
		
		#screensurf.blit(CPULEDSTANDBY, (605, 433))
		#screensurf.blit(STEPLED, (605, 440))
		#for fnx in abt:
		#	fnx=fnx.replace('\n', '')
		#	abttext=simplefont.render(fnx, True, (0, 127, 255), (0, 0, 0))
		#	screensurf.blit(abttext, (45, pixcnt1))
		#	pixcnt1 += pixjmp
		#pixcnt1=38
		lineq=0
		libSBTCVMsurf.fill(TTYBGCOL)
		for fnx in abt:
			fnx=fnx.replace('\n', '')
			colq=0
			for qlin in fnx:
				#print qlin
				charq=libSBTCVM.charlookupdict.get(qlin)
				#print charq
				libSBTCVM.charblit(libSBTCVMsurf, colq, lineq, charq)
				colq +=1
			lineq +=1
		#screensurf.blit(libSBTCVMsurf, (45, 40))
		if tuibig==0:
			screensurf.blit(libSBTCVMsurf, (45, 40))
		else:
			biglibSBTCVM=pygame.transform.scale(libSBTCVMsurf, (648, 486))
			screensurf.blit(biglibSBTCVM, (0, 0))
		#print "fbuff"
	
	pygame.display.update()
	#clear buffer secion of IObus
	#this means: DONT USE THE BUFFER SECTION OF THE IObus AS RAM :|
	#chklist = open("ORDEREDLIST6REGISTER.txt")
	#for ramadr in libSBTCVM.chklist:
	#	#print "foobar"
	#	ramadr=ramadr.replace("\n", "")
	#	RAMbank[ramadr] = "000000"
	#	#
	
	
	time.sleep(CPUWAIT)
	
	evhappenflg2=0

#print "foobar"
if logromexit==1:
	print "logging TROM MEMORY into CAP dir..."
	libtrom.dumptroms()
#print "postlog"
if logIOexit==1:
	print "logging final IObus state into CAP dir..."
	ramdmp=open((os.path.join('CAP', 'IOBUS.dmp')),  'w')
	for IOitm in RAMbank:
		ramdmp.write("A:" + str(IOitm) + " D:" + RAMbank[IOitm] + "\n")
	ramdmp.close()
#"exitloop"
evhappenflg3=0
while evhappenflg3==0:
		time.sleep(.1)
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				evhappenflg3=1
				break
