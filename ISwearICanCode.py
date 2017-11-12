# Joshua Pollock
# 11/11/17
# Live Coder

import sys
import os
import string
import random

isLinux = sys.platform == 'linux'

if isLinux:
	import tty, termios
	old_settings = termios.tcgetattr(sys.stdin)
	tty.setcbreak(sys.stdin.fileno())
else:
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
			ch = 'a'
	return ch

def output(code, cursor, error):

	next=code[cursor]
	
	if ((next == "\r" or next == "\n" or next == "\t") and error != -1):
		return (cursor, error)
	
	if (next == "\r" or next=="\n"):
		print("\r")
		
	else:
		print(next, end="")
		sys.stdout.flush()
		if (error == cursor):
			error = -1

	return (cursor+1, error)
		
def io(arg):

	with open(arg, "r") as f:
		code = f.read() +"\n"
	return code

def typing(code):

	ch='a'
	cursor=0
	error=-1
	while (ch != '\x1b'):
		ch = getchar()
		
		
		if (ch == '\x08'):
			if (cursor == 0):
				continue
			last = code[cursor-1]
			if (last != '\n' and last != '\r' and last != '\t'):
				print("\b \b", end="")
				sys.stdout.flush()
				cursor-=1
			continue
		
		if ((cursor+1)>=len(code)):
			if (ch == '\n' or ch == '\r'):
				clr()
				return False
			else:
				continue
		
		
		numbers = set(['1','2','3','4','5','6','7','8','9','0'])
		if (ch in numbers):
			next = code[cursor]
			if (next != '\n' and next != '\r' and next != '\t'):
				print(random.choice(string.ascii_lowercase), end="")
				sys.stdout.flush()
				if (error == -1):
					error = cursor
				cursor+=1
			continue
		
		upcoming = code[cursor+1]
		
		if (ch == '\t'):
			while (upcoming !=  ' ' and upcoming != "\n" and upcoming != "\r"):
				(cursor, error) = output(code, cursor, error)
				upcoming = code[cursor+1]
			
		if (ch == '\n' or ch=='\r'):
			while (upcoming != "\n" and upcoming != "\r" and (cursor+2)<len(code)):
				(cursor, error) = output(code, cursor, error)
				upcoming = code[cursor+1]

		(cursor, error) = output(code, cursor, error)

	return True
	
if len(sys.argv)<2:
	sys.exit("Include the files you want to \"code\" as arguements!")

path = os.getcwd()
prompt = ""
done=False

try:
	clr()
	
	for arg in sys.argv[1:]:
		prompt += path + ">"
		print(prompt, end="")
		sys.stdout.flush()
		if typing("vim "+arg+" "):
			done = True
			break
		clr()
		
		prompt += "vim " + arg + "\n"
		
		typing(io(arg))
		clr()
	
	if not done:
		print(prompt[:-1], end="")
		sys.stdout.flush()
		
finally:
	try:
		termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
	except:
		pass