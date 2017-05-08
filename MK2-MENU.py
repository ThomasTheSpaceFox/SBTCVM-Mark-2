#!/usr/bin/env python
import time
import os
import sys
import pygame
from pygame.locals import *
import VMSYSTEM.libSBTCVM as libSBTCVM
pygame.display.init()
pygame.font.init()

def textsciter(flookup):
	abt = open(os.path.join("VMSYSTEM", flookup))
	pixcnt1=96
	pixjmp=14
	
	for fnx in abt:
		fnx=fnx.replace('\n', '')
		abttextB=simplefont.render(fnx, True, (0, 0, 0), (0, 127, 255))
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
				if event.type == KEYDOWN:
					evhappenflg2=1
					break

#SBTCVM
windowicon=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'icon64.png'))
pygame.display.set_icon(windowicon)
simplefont = pygame.font.SysFont(None, 16)
simplefontB = pygame.font.SysFont(None, 22)
simplefontC = pygame.font.SysFont(None, 32)
screensurf=pygame.display.set_mode((800, 600))
#
evhappenflg=0
#visual menu item names:
mainmenulst=["Introduction", "Demo Menu", "help", "about", "quit"]
#selection codes:
mainmenucode=["STINTRO", "DEMO", "HELP", "ABT", "QUIT"]
mainmenudesc=["An introduction to SBTCVM.", "A selection of various demo programs.", "How to get help.", "About SBTCVM.", "Quit."]
#number of menu items:
mainmenucnt=5
menudesc="Main Menu"

#demomenu
demomenulst=["Main Menu", "6-trit Color map", "Fibonacci"]
demomenucode=["MAIN", "COLMAP", "FIB"]
demomenudesc=["Return to main menu.", "See a 6-trit color map be calculated.", "The Fibonacci Sequence."]
demomenucnt=3

curmenulst=mainmenulst
curmenucnt=mainmenucnt
curmenucode=mainmenucode
curmenudesc=mainmenudesc

vmlaunchbg=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'VM-LAUNCH.png')).convert()
qflg=0
menuhighnum=1
ixreturn=0
retfromexec=1
while qflg!=1:
	if retfromexec==1:
		print "return from VM execution."
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
			if event.type == KEYDOWN and event.key == K_RIGHT:
				menuhighnum += 1
				evhappenflg=1
			if event.type == KEYDOWN and event.key == K_DOWN:
				menuhighnum += 1
				evhappenflg=1
			if event.type == KEYDOWN and event.key == K_LEFT:
				menuhighnum -= 1
				evhappenflg=1
			if event.type == KEYDOWN and event.key == K_RETURN:
				ixreturn=1
				evhappenflg=1
				break
			if event.type == QUIT:
				sys.exit()
				evhappenflg=1
				break
	if menuhighnum<=0:
		menuhighnum=curmenucnt
	elif menuhighnum>curmenucnt:
		menuhighnum=1
	#print menuhighnum
	if ixreturn==1:
		ixreturn=0
		#launcher operations.
		if curmenucode[(menuhighnum - 1)]=="STINTRO":
			GLOBSTREG="intro.streg"
			VMFILE=open('SBTCVM_MK2.py', 'r')
			EXECVM=compile(VMFILE.read(), 'SBTCVM_MK2.py', 'exec')
			exec(EXECVM)
			retfromexec=1
		if curmenucode[(menuhighnum - 1)]=="FIB":
			GLOBSTREG="fib.streg"
			VMFILE=open('SBTCVM_MK2.py', 'r')
			EXECVM=compile(VMFILE.read(), 'SBTCVM_MK2.py', 'exec')
			exec(EXECVM)
			retfromexec=1
		if curmenucode[(menuhighnum - 1)]=="COLMAP":
			GLOBSTREG="colmap3.streg"
			VMFILE=open('SBTCVM_MK2.py', 'r')
			EXECVM=compile(VMFILE.read(), 'SBTCVM_MK2.py', 'exec')
			exec(EXECVM)
			retfromexec=1
		#quit item
		if curmenucode[menuhighnum - 1]=="QUIT":
			qflg=1
		#text screens
		if curmenucode[menuhighnum - 1]=="ABT":
			textsciter("L_ABT.TXT")
		if curmenucode[menuhighnum - 1]=="HELP":
			textsciter("L_HELP.TXT")
		#Menu Swapping items
		if curmenucode[menuhighnum - 1]=="MAIN":
			menuhighnum=1
			curmenulst=mainmenulst
			curmenucnt=mainmenucnt
			curmenucode=mainmenucode
			curmenudesc=mainmenudesc
			menudesc="Main Menu"
		if curmenucode[menuhighnum - 1]=="DEMO":
			menuhighnum=1
			curmenulst=demomenulst
			curmenucnt=demomenucnt
			curmenucode=demomenucode
			curmenudesc=demomenudesc
			menudesc="Demo Menu"
		
	
	
	
	
	

