#!/usr/bin/env python

import libSBTCVM
import libbaltcalc
import sys



try:
	cmd=sys.argv[1]
except:
	cmd=None
if cmd=="-h" or cmd=="--help":
	print '''This is MK2-RUN.py, a command line launcher for SBTCVM Mark 2
commands:
MK2-RUN.py -h (--help): this text
MK2-RUN.py -v (--version)
MK2-RUN.py -a (--about): about MK2-RUN.py
MK2-RUN.py -r (--run) [trom file]: run a trom as TROMA
MK2-RUN.py [trom file]: run a trom as TROMA
MK2-RUN.py -r (--run) [streg file]: run specified streg file.
MK2-RUN.py [streg file]: run specified streg file.
'''
elif cmd=="-v" or cmd=="--version":
	print "SBTCVM MK2-RUN launcher v2.0.1"
elif cmd=="-a" or cmd=="--about":
	print '''#SBTCVM Mark 2 commandline launcher


v2.0.1

(c)2016-2017 Thomas Leathers

  SBTCVM Mark 2 commandline launcher is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
  
  SBTCVM Mark 2 commandline launcher is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
  GNU General Public License for more details.
 
  You should have received a copy of the GNU General Public License
  along with SBTCVM Mark 2 commandline launcher. If not, see <http://www.gnu.org/licenses/>
'''
elif cmd==None:
	print "tip: use MK2-RUN.py -h for help."
elif cmd=="-r" or cmd=="--run" or cmd[0]!="-":
	if cmd[0]!="-":
		arg=sys.argv[1]
	else:
		arg=sys.argv[2]
		print arg
	if ((arg.split("."))[1]).lower()=="trom":
		
		GLOBRUNFLG=arg
		VMFILE=open('SBTCVM_MK2.py', 'r')
		EXECVM=compile(VMFILE.read(), 'SBTCVM_MK2.py', 'exec')
		exec(EXECVM)
	elif ((arg.split("."))[1]).lower()=="tasm":
		print "This is an SBTCVM assembly file, you need to build it into a trom first."
	elif ((arg.split("."))[1]).lower()=="streg":
		print "SBTCVM trom execution group file, detected."
		GLOBSTREG=arg
		VMFILE=open('SBTCVM_MK2.py', 'r')
		EXECVM=compile(VMFILE.read(), 'SBTCVM_MK2.py', 'exec')
		exec(EXECVM)
		