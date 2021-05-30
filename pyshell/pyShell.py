#!/usr/bin/env python
from __future__ import print_function
from os import listdir
from os.path import isfile, join
import re
import os
import string


while True:
	x=raw_input('\033[92m'+'\033[1m'+os.getcwd()+"$ "+'\033[0m')
	if x=="ls":
		for f in listdir("."):
			print(f, end='\n')
		print()  #done

	if re.match("cd *",x): 
		x=x[3:]
		if len(x)<1:
			os.chdir(".")
		else:
			try:
				os.chdir(x)
				# for f in listdir("."):
				# 	print(f, end=' ')
				# print() 
			except:
				print('\033[91m'+"No such directory exists!"+'\033[0m')  #done

	if x=="pwd":
		print(os.getcwd()) #done

	if re.match("touch *",x): 
		x=x[6:]
		if len(x)<1:
			print('\033[91m'+"enter valid no. of arguments"+'\033[0m')
			continue
		files=x.split() #if more than one file is put in touch
		for f in files:
			f=open(f,'a')
			f.close()   #done  #done
		
	if re.match("head *",x):
		x=x[5:]
		if len(x)<1:
			print('\033[91m'+"enter valid no. of arguments"+'\033[0m')
			continue
		if x[0]=="-":
			y=x[1]
			z=x[3:]
			try:
				isfile(z)
				f=open(z)
				for i in range(int(y)):
					line=f.next()
					line.strip()
					print(line, end='')
				f.close()
			except:
				print('\033[91m'+"give valid file name!"+'\033[0m')
		else:
			try:
				isfile(x)
				size=0
				f=open(x)
				for i in f: #calculate size of file
					size=size+1
				f.close()
				if size>=10:
					f=open(x)
					for i in range(10):
						line=f.next()
						line.strip()
						print(line, end='')
					f.close()
				else:
					f=open(x)
					for i in range(size):
						line=f.next()
						line.strip()
						print(line, end='')
					f.close()
			except:
				print('\033[91m'+"give valid file name!"+'\033[0m')  #done  #done
			

	if re.match("tail *",x):
		x=x[5:]
		if len(x)<1:
			print('\033[91m'+"enter valid no. of arguments"+'\033[0m')
			continue
		if x[0]=="-":
			y=x[1] #tail -2 then y=2
			z=x[3:]
			try:
				isfile(z)
				size=0
				f=open(z)
				for i in f: #calculate size of file
					size=size+1
				f.close()
				y=size-int(y)
				l=[]
				for i in range(int(y),size+1,1): #froming list of line no.s to be printed
					l.append(i)
				f=open(z)
				i=0
				for line in f:
					if i in l:
						print(line, end='')
						i+=1
					else:
						i+=1
				f.close()
				print()
			except:
				print('\033[91m'+"This file does not exist!"+'\033[0m')
		else:
			try:
				isfile(x)
				size=0
				f=open(x)
				for i in f: #calculate size of file
					size=size+1
				f.close()
				if size>=10:
					y=size-10
					l=[]
					for i in range(int(y),size+1,1): #froming list of line no.s to be printed
						l.append(i)
					f=open(x)
					i=0
					for line in f:
						if i in l:
							print(line, end='')
							i+=1
						else:
							i+=1
					f.close()
					print()
				else:
					f=open(x)
					for i in range(size):
						line=f.next()
						line.strip()
						print(line, end='')
					f.close()
			except:
				print('\033[91m'+"This file does not exist!"+'\033[0m')  #done  #done
			
	if re.match("tr *",x): 
		x=x[3:]
		if len(x)<2:
			print('\033[91m'+"enter valid no. of arguments"+'\033[0m')
			continue
		st=x.split()
		fr=st[0]
		to=st[1]
		if fr=="-d":
			while True:
				s=raw_input()
				if s=="exit:":
					break
				else:
					for i in to:
						s=re.sub(i,'',s)
					print(s)
		# print(st[1])
		# print(st[0])
		else:
			if len(fr)!=len(to):
				print('\033[91m'+"both the arguments must be of same length"+'\033[0m')
				continue
			while True:
				s=raw_input()
				if s=="exit:": 
					break
				else:
					print(s.translate(string.maketrans(fr,to)))  #done

	if re.match("grep *",x):
		x=x[5:]
		if len(x)<2:
			print('\033[91m'+"enter valid no. of arguments"+'\033[0m')
			continue
		st=x.split(" ",1)
		s=st[0].strip('\'')
		string=[s,st[1]]
		try:
			isfile(string[1])
			f=open(string[1])
			for line in f:
				if re.search(string[0],line):
					print(line, end="")
				else:
					pass
			f.close()
		except:
			# print(string[0])
			# print(string[1])
			print('\033[91m'+"Enter valid file name"+'\033[0m')  #done #done

	if re.match("sed *",x):
		x=x[4:]
		if len(x)<2:
			print('\033[91m'+"enter valid no. of arguments"+'\033[0m')
			continue
		st=x.split(" ",1)
		# print(st)
		s1=st[0].strip('\'')
		# print(s1)
		s=[]
		s=s1.split("/")
		file=st[1].strip('\'')
		# print(s)

		if s[0]=='s' and s[-1]=='g':
			try:
				isfile(file)
				f=open(file)
				for line in f:
					if re.search(s[1],line):
						print(line.replace(s[1],s[2]), end="")
					else:
						print(line, end="")
				f.close()
			except:
				print('\033[91m'+"Either file name is invalid or command was wrongly typed!"+'\033[0m')
		elif s[0]=='s' and s[-1]=='':
			try:
				isfile(file)
				f=open(file)
				for line in f:
					if re.search(s[1],line):
						print(line.replace(s[1],s[2],1), end="")
					else:
						print(line, end="")
				f.close()
			except:
				print('\033[91m'+"Either file name is invalid or command was wrongly typed!"+'\033[0m')
		else:
			print('\033[91m'+"sed: -e expression #1, char 12: unterminated `s' command"+'\033[0m')
			pass  #done   #done  #done

	if re.match("diff *",x):
		x=x[5:]
		if len(x)<2:
			print('\033[91m'+"enter valid no. of arguments"+'\033[0m')
			continue
		s=x.split(" ")
		if isfile(s[0]) and isfile(s[1]):
			try:
				added=[]
				change=[]
				unchanged=[]
				delete=[]
				indsec=0
				second=open(s[1])
				while True:
					
					line_2=second.readline()
					indchange=0
					if line_2=='':
						break
					
					indfir=0
					first=open(s[0])
					while True:
						line_1=first.readline()
						
						if line_1=='':
							break
						if line_1==line_2:
							indchange=1
							if indfir==indsec:
								unchanged.append(line_1)
								indfir+=1

							if indsec!=indfir:
								change.append(line_1)
								indfir+=1

						else:
							indfir+=1
							continue
					if indchange==0:
						added.append(line_2)
					indsec+=1
					
				first=open(s[0])
				for line in first:
					if line not in change and line not in unchanged:
						delete.append(line)

				if len(added)!=0:
					print('\033[94m'+'\033[1m'+'\033[4m'+"Lines Added:"+'\033[0m')
					for i in added:
						print('> ',i.strip())

				if len(delete)!=0:
					print('\033[94m'+'\033[1m'+'\033[4m'+"Lines Deleted:"+'\033[0m')
					for i in delete:
						print('< ',i.strip())

				if len(change)!=0:
					print('\033[94m'+'\033[1m'+'\033[4m'+"Lines unchanged:"+'\033[0m')
					for i in change:
						print('< ',i.strip())

			except:
				print('\033[91m'+"Error in opening the file!"+'\033[0m')
		else:
			print('\033[91m'+"Enter valid file name!"+'\033[0m')

	if x=="exit()":
		break
	
	else:
		continue
