#!/usr/bin/env python

#import VMSYSTEM.libSBTCVM as libSBTCVM
import VMSYSTEM.libbaltcalc as libbaltcalc
import VMSYSTEM.libvmcmdshell as cmdshell
import sys
import os
from subprocess import call
VMSYSROMS=os.path.join("VMSYSTEM", "ROMS")
try:
	cmd=sys.argv[1]
except:
	cmd=None
if cmd=="-h" or cmd=="--help" or cmd=="help":
	print '''This is MK2-CS.py, a command shell for SBTCVM Mark 2
commands:
MK2-CS.py -h (--help) (help): this text
MK2-CS.py -v (--version)
MK2-CS.py -a (--about): about MK2-RUN.py
'''
elif cmd=="-v" or cmd=="--version":
	print cmdshell.versiontext
elif cmd=="-a" or cmd=="--about":
	print cmdshell.abouttext
elif cmd==None:
	qflg=0
	usrinp=""
	#RUNFILE=open('MK2-RUN.py', 'r')
	#EXECRUN=compile(RUNFILE.read(), 'MK2-RUN.py', 'exec')
	print cmdshell.versiontext
	print "ready."
	while qflg!=1:
		userinp=raw_input((':'))
		usercalllst=userinp.split(" ", 1)
		if (usercalllst[0]).lower()=="help":
			print cmdshell.helptext
		if (usercalllst[0]).lower()=="about":
			print cmdshell.abouttext
		if (usercalllst[0]).lower()=="version":
			print cmdshell.versiontext
		if (usercalllst[0]).lower()=="list":
			try:
				if (usercalllst[1]).lower()=="types":
					for typename in cmdshell.keyftypes:
						print typename
				elif (usercalllst[1]).lower()=="paths":
					for typename in cmdshell.pathlist:
						print typename
				elif (usercalllst[1]).lower()=="help":
					print cmdshell.listhelptext
				else:
					for dittype in cmdshell.keyftypes:
						if (usercalllst[1]).lower()==dittype:
							for diter in cmdshell.pathlist:
								for fname in os.listdir(diter):
									fnamelo=fname.lower()
									if fnamelo.endswith(("." + dittype)): 
										print(os.path.join(diter, fname))
			except IndexError:
				for diter in cmdshell.pathlist:
					for fname in os.listdir(diter):
						fnamelo=fname.lower()
						for dittype in cmdshell.keyftypes:
							if fnamelo.endswith("." + dittype):
								print(os.path.join(diter, fname))
		#these simply call another python process altogether to re-use the command line syntax of these utilities:
		if (usercalllst[0]).lower()=="asm":
			try:
				arglst=list((usercalllst[1]).split(" "))
				arglst2=list(["python", "SBTCVM-asm2.py"])
				arglst2.extend(arglst)
				call(arglst2)
			except IndexError:
				call(["python", "SBTCVM-asm2.py"])
			
		if (usercalllst[0]).lower()=="run":
			try:
				arglst=list((usercalllst[1]).split(" "))
				arglst2=list(["python", "MK2-RUN.py"])
				arglst2.extend(arglst)
				call(arglst2)
			except IndexError:
				call(["python", "MK2-RUN.py"])
		if (usercalllst[0]).lower()=="gfx":
			try:
				arglst=list((usercalllst[1]).split(" "))
				arglst2=list(["python", "MK2-GFX.py"])
				arglst2.extend(arglst)
				call(arglst2)
			except IndexError:
				call(["python", "MK2-GFX.py"])
		if (usercalllst[0]).lower()=="quit":
			qflg=1
		if (usercalllst[0]).lower()=="btdec":
			try:
				arg=usercalllst[1]
				print libbaltcalc.BTTODEC(arg)
			except IndexError:
				print "please specify one balanced ternary integer"
		if (usercalllst[0]).lower()=="invert":
			try:
				arg=usercalllst[1]
				print libbaltcalc.BTINVERT(arg)
			except IndexError:
				print "please specify one balanced ternary integer"
		if (usercalllst[0]).lower()=="decbt":
			try:
				arg=usercalllst[1]
				print libbaltcalc.DECTOBT(int(arg))
			except IndexError:
				print "please specify one decimal integer"
			except TypeError:
				print "Please specify one decimal integer."
			except ValueError:
				print "Please specify one decimal integer."
		if (usercalllst[0]).lower()=="mpi":
			try:
				arg=usercalllst[1]
				#calculate the MPI of the user-specifed number of trits
				print int(((3**(int(arg)))-1)/2)
			except IndexError:
				print "please specify one decimal integer"
			except TypeError:
				print "Please specify one decimal integer."
			except ValueError:
				print "Please specify one decimal integer."
		if (usercalllst[0]).lower()=="mcv":
			try:
				arg=usercalllst[1]
				print int(3**(int(arg)))
			except IndexError:
				print "please specify one decimal integer"
			except TypeError:
				print "Please specify one decimal integer."
			except ValueError:
				print "Please specify one decimal integer."
		if (usercalllst[0]).lower()=="add":
			try:
				arg=usercalllst[1]
				arglst=arg.split(" ")
				arg1=arglst[0]
				arg2=arglst[1]
				
				print libbaltcalc.btadd(arg1, arg2)
			except IndexError:
				print "please specify two balanced ternary integers separated by a space."
		if (usercalllst[0]).lower()=="mul":
			try:
				arg=usercalllst[1]
				arglst=arg.split(" ")
				arg1=arglst[0]
				arg2=arglst[1]
				
				print libbaltcalc.btmul(arg1, arg2)
			except IndexError:
				print "please specify two balanced ternary integers separated by a space."
		if (usercalllst[0]).lower()=="sub":
			try:
				arg=usercalllst[1]
				arglst=arg.split(" ")
				arg1=arglst[0]
				arg2=arglst[1]
				
				print libbaltcalc.btsub(arg1, arg2)
			except IndexError:
				print "please specify two balanced ternary integers separated by a space."
		if (usercalllst[0]).lower()=="div":
			try:
				arg=usercalllst[1]
				arglst=arg.split(" ")
				arg1=arglst[0]
				arg2=arglst[1]
				
				print libbaltcalc.btdiv(arg1, arg2)
			except IndexError:
				print "please specify two balanced ternary integers separated by a space."
		
		
		
else:
	print "tip: use MK2-RUN.py -h for help."
#elif cmd=="-s" or cmd=="--shell" or cmd[0]!="-":
	
			