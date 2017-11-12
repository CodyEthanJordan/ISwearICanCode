# Joshua Pollock
# 11/11/17
# Live Coding

import sys
import os

isLinux = sys.platform == 'linux'

try:
	import tty, termios
except:
	import msvcrt

def clr():
	if isLinux:
		os.system('clear')
	else:
		os.system('cls')

def getchar():
	try:
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(1)
	except:
		ch = msvcrt.getch()
		try:
			ch = ch.decode()
		except:
			ch = '0'
	return ch


if len(sys.argv)!=2:
	print (len(sys.argv))
	sys.exit("Incorrect Number of Arguments")

with open(sys.argv[1], "r") as f:

	code = f.read()

clr()

ch='0'
while (ch != '\x1b'):
	ch = getchar()

	if (len(code)>1):
		next=code[0]
		code=code[1:]

		if (next == "\r" or next=="\n"):
			print("\r")


		else:
			print(next, end="")
#			sys.stdout.write(next)
			sys.stdout.flush()

clr()
