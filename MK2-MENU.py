#!/usr/bin/env python
import time
import os
import sys
import pygame
from pygame.locals import *
import VMSYSTEM.libSBTCVM as libSBTCVM
import VMSYSTEM.libbaltcalc as libbaltcalc
print "SBTCVM menu system v2.0.1"

pygame.display.init()
pygame.font.init()
pygame.mixer.init()
pygame.display.set_caption("SBTCVM Mark 2 | Menu", "SBTCVM Mark 2 | Menu")
#put SBTCVM in kiosk mode.
#this adjusts how SBTCVM works in certain cases to better mesh with the menu system.
#such as disabling the wait-on-exit feature.
GLOBKIOSK=1

#SBTCVM Mark 2
#Simple Balanced Ternary Computer Virtual Machine
#
#v2.0.1
#
#(c)2016-2017 Thomas Leathers
#
#  SBTCVM Mark 2 is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  
#  SBTCVM Mark 2 is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with SBTCVM Mark 2. If not, see <http://www.gnu.org/licenses/>

#simple text iterator. loads the refrenced text file from VMSYSTEM.
#(shows the text screens)
def textsciter(flookup):
	abt = open(os.path.join("VMSYSTEM", flookup))
	pixcnt1=96
	pixjmp=16
	
	for fnx in abt:
		fnx=fnx.replace('\n', '')
		abttextB=simplefontA.render(fnx, True, (0, 0, 0), (0, 127, 255))
		screensurf.blit(abttextB, (9, pixcnt1))
		pixcnt1 += pixjmp
	pixcnt1 += pixjmp
	fnx="Press any key to continue"
	abttextB=simplefontB.render(fnx, True, (0, 0, 0), (255, 255, 255))
	screensurf.blit(abttextB, (9, pixcnt1))
	pygame.display.update()
	evhappenflg2=0
	while evhappenflg2==0:
			time.sleep(.1)
			for event in pygame.event.get():
				if event.type == KEYDOWN and event.key == K_F8:
					pygame.image.save(screensurf, (os.path.join('CAP', 'SCREENSHOT-MENU.png')))
					break
				elif event.type == KEYDOWN:
					evhappenflg2=1
					menusound2.play()
					break
#Balanced ternary clock function. (shows clock that is in the extras menu.
def BTCLOCKDATE():
	
	loopend=0
	hourY=227
	minY=227
	secY=227
	ttextY=204
	helplab = simplefontB.render(('''Red=-, violet=0 blue=+'''), True, (255, 255, 255))
	screensurf.blit(helplab, (3, 120))
	prevtime=None
	#quick fix to solve drawing glitches
	scbak=screensurf.copy()
	while loopend==0:
		screensurf.blit(scbak, (0, 0))
		#screensurf.fill((127, 127, 127))
		time.sleep(0.2)
		for event in pygame.event.get():
			if event.type == KEYDOWN and event.key == K_F8:
				pygame.image.save(screensurf, (os.path.join('CAP', 'SCREENSHOT-MENU.png')))
				break
			elif event.type == KEYDOWN:
				loopend=1
			if event.type == QUIT:
				loopend=1
		pygame.event.clear()
		curtim=time.localtime()
		hourdec=curtim[3]
		mindec=curtim[4]
		secdec=curtim[5]
		if prevtime!=secdec:
			menusound3.play()
		prevtime=secdec
		hourbt=libSBTCVM.trunkto4(libbaltcalc.DECTOBT(hourdec))
		minbt=libSBTCVM.trunkto5(libbaltcalc.DECTOBT(mindec))
		secbt=libSBTCVM.trunkto5(libbaltcalc.DECTOBT(secdec))
		hourX=3
		hourtext = simplefont.render(("Hr. " + str(hourdec) + ""), True, (255, 255, 255), (0, 0, 0))
		screensurf.blit(hourtext, (hourX, ttextY))
		for fxg in hourbt:
			if fxg=="0":
				screensurf.blit(GNDlamp, (hourX, hourY))
			if fxg=="+":
				screensurf.blit(POSlamp, (hourX, hourY))
			if fxg=="-":
				screensurf.blit(NEGlamp, (hourX, hourY))
			hourX += 9
		minX=(hourX + 9)
		mintext = simplefont.render(("Min. " + str(mindec) + ""), True, (255, 255, 255), (0, 0, 0))
		screensurf.blit(mintext, (minX, ttextY))
		for fxg in minbt:
			if fxg=="0":
				screensurf.blit(GNDlamp, (minX, minY))
			if fxg=="+":
				screensurf.blit(POSlamp, (minX, minY))
			if fxg=="-":
				screensurf.blit(NEGlamp, (minX, minY))
			minX += 9
		secX=(minX + 9)
		sectext = simplefont.render(("Sec. " + str(secdec) + ""), True, (255, 255, 255), (0, 0, 0))
		screensurf.blit(sectext, (secX, ttextY))
		for fxg in secbt:
			if fxg=="0":
				screensurf.blit(GNDlamp, (secX, secY))
			if fxg=="+":
				screensurf.blit(POSlamp, (secX, secY))
			if fxg=="-":
				screensurf.blit(NEGlamp, (secX, secY))
			secX += 9
		pygame.display.update()

#SBTCVM
windowicon=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'icon64.png'))
GNDlamp=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), '3lampGND.png'))
POSlamp=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), '3lampPOS.png'))
NEGlamp=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), '3lampNEG.png'))

pygame.display.set_icon(windowicon)
#screen fonts
simplefont = pygame.font.SysFont(None, 16)
simplefontA = pygame.font.SysFont(None, 20)
simplefontB = pygame.font.SysFont(None, 22)
simplefontC = pygame.font.SysFont(None, 32)
screensurf=pygame.display.set_mode((800, 600))
#
evhappenflg=0
#visual menu item names:
mainmenulst=["Get Started", "Demo Menu", "Help Menu", "Extras Menu", "Quit"]
#selection codes:
mainmenucode=["GETSTART", "DEMO", "HELP", "EXTRAS", "QUIT"]
mainmenudesc=["Get started with SBTCVM", "A selection of various demo programs.", "Get Help", "A selection of various extras.", "Quit."]
#number of menu items:
mainmenucnt=5
menudesc="Main Menu"
#these use the same squarewave generator as SBTCVM's buzzer.

#sound A
menusound1=pygame.mixer.Sound(libSBTCVM.autosquare(300, 0.1))
#menu select sound
menusound2=pygame.mixer.Sound(libSBTCVM.autosquare(250, 0.1))
#clock widget second sound
menusound3=pygame.mixer.Sound(libSBTCVM.autosquare(280, 0.1))
menusound2.play()

#demomenu
demomenulst=["Main Menu", "6-trit Color map", "Fibonacci", "Flower"]
demomenucode=["MAIN", "COLMAP", "FIB", "FLOWER"]
demomenudesc=["Return to main menu.", "See a 6-trit color map be calculated.", "The Fibonacci Sequence.", "See an example of image conversion."]
demomenucnt=4

#getstartmenu
stmenulst=["Main Menu", "Welcome",  "Intro Program"]
stmenucode=["MAIN", "WELCOME", "STINTRO"]
stmenudesc=["Return to main menu.", "A welcome to SBTCVM.", "An introduction to SBTCVM, that runs in SBTCVM."]
stmenucnt=3

hlpmenulst=["Main Menu", "More help",  "About"]
hlpmenucode=["MAIN", "HLPOVER", "ABT"]
hlpmenudesc=["Return to main menu.", "How to get more help.", "About SBTCVM."]
hlpmenucnt=3

exmenulst=["Main Menu", "Clock"]
exmenucode=["MAIN", "CLOCK"]
exmenudesc=["Return to main menu.", "A balanced ternary clock."]
exmenucnt=2

curmenulst=mainmenulst
curmenucnt=mainmenucnt
curmenucode=mainmenucode
curmenudesc=mainmenudesc

vmlaunchbg=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'VM-LAUNCH.png')).convert()
qflg=0
menuhighnum=1
ixreturn=0
retfromexec=0
while qflg!=1:
	if retfromexec==1:
		print "----------------"
		print "return from VM execution."
		print "----------------"
		retfromexec=0
		pygame.display.set_caption("SBTCVM Mark 2 | Menu", "SBTCVM Mark 2 | Menu")
	#starting point for menu
	texhigcnt=2
	#separation between each line of text's origin
	texhigjump=22
	#menu line count variable. should be set to 1 here.
	indlcnt=1
	screensurf.blit(vmlaunchbg, (0, 0))
	for indx in curmenulst:
		if indlcnt==menuhighnum:
			textit=simplefontB.render(indx, True, (0, 0, 0), (255, 255, 255))
		else:
			textit=simplefontB.render(indx, True, (0, 0, 0), (127, 127, 255))
		screensurf.blit(textit, (650, texhigcnt))
		texhigcnt += texhigjump
		indlcnt += 1
	menulabel=simplefontC.render(menudesc, True, (0, 0, 0), (255, 255, 255))
	screensurf.blit(menulabel, (158, 4))
	itemlabel=simplefontB.render(curmenudesc[(menuhighnum - 1)], True, (0, 0, 0), (255, 255, 255))
	screensurf.blit(itemlabel, (170, 34))
	pygame.display.update()
	pygame.event.pump()
	pygame.event.clear()
	#reads keyboard controlls, moves cursers when instructed by up/down arrow keys.
	#sets ixreturn to 1 when return is pressed.
	evhappenflg=0
	while evhappenflg==0:
		time.sleep(.1)
		for event in pygame.event.get():
			if event.type == KEYDOWN and event.key == K_UP:
				menuhighnum -= 1
				evhappenflg=1
				#menusound2.play()
				break
			if event.type == KEYDOWN and event.key == K_RIGHT:
				menuhighnum += 1
				evhappenflg=1
				#menusound2.play()
				break
			if event.type == KEYDOWN and event.key == K_DOWN:
				menuhighnum += 1
				evhappenflg=1
			#	menusound2.play()
				break
			if event.type == KEYDOWN and event.key == K_LEFT:
				menuhighnum -= 1
				evhappenflg=1
				#menusound2.play()
				break
			if event.type == KEYDOWN and event.key == K_RETURN:
				ixreturn=1
				evhappenflg=1
				menusound2.play()
				break
			if event.type == KEYDOWN and event.key == K_F8:
				pygame.image.save(screensurf, (os.path.join('CAP', 'SCREENSHOT-MENU.png')))
				break
			if event.type == QUIT:
				sys.exit()
				evhappenflg=1
				break
	#makes menus "roll over"
	if menuhighnum<=0:
		menuhighnum=curmenucnt
	elif menuhighnum>curmenucnt:
		menuhighnum=1
	#print menuhighnum
	#when a menu item is chosen (return) this section determines the action to preform based on the menuitem code for that menu item
	if ixreturn==1:
		ixreturn=0
		#launcher operations.
		if curmenucode[(menuhighnum - 1)]=="STINTRO":
			GLOBSTREG="intro.streg"
			VMFILE=open('SBTCVM_MK2.py', 'r')
			EXECVM=compile(VMFILE.read(), 'SBTCVM_MK2.py', 'exec')
			print "----------------"
			print "starting VM..."
			print "----------------"
			exec(EXECVM)
			retfromexec=1
		if curmenucode[(menuhighnum - 1)]=="FIB":
			GLOBSTREG="fib.streg"
			VMFILE=open('SBTCVM_MK2.py', 'r')
			EXECVM=compile(VMFILE.read(), 'SBTCVM_MK2.py', 'exec')
			print "----------------"
			print "starting VM..."
			print "----------------"
			exec(EXECVM)
			retfromexec=1
		if curmenucode[(menuhighnum - 1)]=="COLMAP":
			GLOBSTREG="colmap3.streg"
			VMFILE=open('SBTCVM_MK2.py', 'r')
			EXECVM=compile(VMFILE.read(), 'SBTCVM_MK2.py', 'exec')
			print "----------------"
			print "starting VM..."
			print "----------------"
			exec(EXECVM)
			retfromexec=1
		if curmenucode[(menuhighnum - 1)]=="FLOWER":
			GLOBSTREG="flower.streg"
			VMFILE=open('SBTCVM_MK2.py', 'r')
			EXECVM=compile(VMFILE.read(), 'SBTCVM_MK2.py', 'exec')
			print "----------------"
			print "starting VM..."
			print "----------------"
			exec(EXECVM)
			retfromexec=1
		#quit item
		if curmenucode[menuhighnum - 1]=="QUIT":
			qflg=1
		#text screens
		if curmenucode[menuhighnum - 1]=="ABT":
			textsciter("L_ABT.TXT")
		if curmenucode[menuhighnum - 1]=="CLOCK":
			BTCLOCKDATE()
		if curmenucode[menuhighnum - 1]=="HLPOVER":
			textsciter("L_HELP.TXT")
		if curmenucode[menuhighnum - 1]=="WELCOME":
			textsciter("L_WEL.TXT")
		#this code action id unfinished
		if curmenucode[menuhighnum - 1]=="DEMOMODE":
			#textsciter("L_WEL.TXT")
			GLOBSTREG="colmap3.streg"
			VMFILE=open('SBTCVM_MK2.py', 'r')
			EXECVM=compile(VMFILE.read(), 'SBTCVM_MK2.py', 'exec')
			print "----------------"
			print "starting VM..."
			print "----------------"
			exec(EXECVM)
			retfromexec=1
		#Menu Swapping items
		#this is how the menu system is able to run many menus with one instance of code.
		if curmenucode[menuhighnum - 1]=="MAIN":
			menuhighnum=1
			curmenulst=mainmenulst
			curmenucnt=mainmenucnt
			curmenucode=mainmenucode
			curmenudesc=mainmenudesc
			menudesc="Main Menu"
		elif curmenucode[menuhighnum - 1]=="DEMO":
			menuhighnum=1
			curmenulst=demomenulst
			curmenucnt=demomenucnt
			curmenucode=demomenucode
			curmenudesc=demomenudesc
			menudesc="Demo Menu"
		elif curmenucode[menuhighnum - 1]=="GETSTART":
			menuhighnum=1
			curmenulst=stmenulst
			curmenucnt=stmenucnt
			curmenucode=stmenucode
			curmenudesc=stmenudesc
			menudesc="Get Started"
		elif curmenucode[menuhighnum - 1]=="HELP":
			menuhighnum=1
			curmenulst=hlpmenulst
			curmenucnt=hlpmenucnt
			curmenucode=hlpmenucode
			curmenudesc=hlpmenudesc
			menudesc="Help Menu"
		elif curmenucode[menuhighnum - 1]=="EXTRAS":
			menuhighnum=1
			curmenulst=exmenulst
			curmenucnt=exmenucnt
			curmenucode=exmenucode
			curmenudesc=exmenudesc
			menudesc="Extras Menu"
	
	
	
	
	

