#!/usr/bin/env python
import time
import os
import sys
import pygame
from pygame.locals import *
import VMSYSTEM.libSBTCVM as libSBTCVM
import VMSYSTEM.libbaltcalc as libbaltcalc
import VMSYSTEM.libvmui as vmui
#SBTCVM MK2 Graphical Tools launcher



try:
	cmd=sys.argv[1]
except:
	cmd=None
if cmd=="-h" or cmd=="--help" or cmd=="help":
	print '''This is MK2-TOOLS.py, a command line tools launcher for SBTCVM Mark 2
commands:
MK2-RUN.py -h (--help) (help): this text
MK2-RUN.py -v (--version)    : version information.
MK2-RUN.py -a (--about)      : about MK2-RUN.py
MK2-RUN.py -l (--list)       : list all tools and their toolnames.
MK2-RUN.py [toolname]        : run tool
'''
elif cmd=="-v" or cmd=="--version":
	print "SBTCVM MK2-TOOLS tool launcher v2.0.1"
elif cmd=="-l" or cmd=="--list":
	print '''List of tools:
[Toolname]  |  [Tool description]
-----------------------------------------------
about       :  show about screen shown in menus
btclock     :  show a balanced ternary clock
pause       :  test VM pause menu
namecrunch [string] : test namecrunch function'''

elif cmd=="-a" or cmd=="--about":
	print '''#SBTCVM Mark 2 tool launcher


v2.0.1

(c)2016-2017 Thomas Leathers and Contributors

  SBTCVM Mark 2 tool launcher is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
  
  SBTCVM Mark 2 tool launcher is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
  GNU General Public License for more details.
 
  You should have received a copy of the GNU General Public License
  along with SBTCVM Mark 2 tool launcher. If not, see <http://www.gnu.org/licenses/>
'''
elif cmd==None:
	print "tip: use MK2-TOOLS.py -h for help."
elif cmd=="namecrunch":
	if cmd=="namecrunch":
		try:
			ncruncharg=sys.argv[2]
		except IndexError:
			ncruncharg="thisisatest"
		print ncruncharg
		print libSBTCVM.namecrunch(ncruncharg, "-tools-test.log")
elif cmd=="about" or cmd=="btclock" or cmd=="pause":
	print "SBTCVM Graphical Tools launcher starting..."
	pygame.display.init()
	pygame.font.init()
	pygame.mixer.init()
	pygame.display.set_caption("SBTCVM Mark 2 | Tools", "SBTCVM Mark 2 | Tools")
	GLOBKIOSK=1
	windowicon=pygame.image.load(os.path.join(os.path.join('VMSYSTEM', 'GFX'), 'icon64.png'))
	pygame.display.set_icon(windowicon)
	#screen fonts
	screensurf=pygame.display.set_mode((800, 600))
	#init VMUI library.
	vmui.initui(screensurf, 1)
	
	if cmd=="about":
		vmui.toolsscreen(1)
		vmui.creditsscroll()
	
	if cmd=="btclock":
		vmui.toolsscreen(1)
		vmui.BTCLOCKDATE()
	if cmd=="pause":
		print "launching SBTCVM VM pause menu."
		#pause menu needs readouts area to be drawn.
		vmui.toolsscreen(3)
		pmenret=vmui.pausemenu()
		if pmenret=="c":
			print "Pause menu reports a continue VM"
		else:
			print 'Pause menu reports a Stop VM / Exit to Main Menu'