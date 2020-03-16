#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
    The MIT License:

    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and 
    associated documentation files (the "Software"), to deal in the Software without restriction, 
    including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
    and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, 
    subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies or substantial 
    portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT 
    NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
    WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION 
    WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

    Copyright 2019,2020 Ali Erkan IMREK <alierkanimrek@gmail.com>
'''








import os
import importlib









class KBConfig:



	def __init__(self, fn = "default", path = ""):
		filename = fn
		if path == "":
			path, filename = os.path.split(os.path.abspath(__file__))
			self._fn = os.path.join(path, fn+".conf")
		else:
			self._fn = os.path.join(path, fn+".conf")
		try:
			self._checklist = __import__(filename)
		except:
			self._checklist = None
		self.reload()
		
		
	
	
	def _load(self):
		try:
			fh = open(self._fn, "r")
			lines = fh.read().splitlines()
			raw = []
			for line in lines:
				if len(line.strip()) > 0:
					if line.strip()[0] != "#":
						raw.append(line.strip())
		except OSError:
			raise
		except:
			raise Exception("File error", self._fn)
		return(raw)
		
			
				
		
	def _build(self, raw):
		conf = {}
		section = ""
		class obj:
			pass

		for l in raw:
			if len(l.split("=")) == 2:	v=True
			else:	v=False
			if l[0] == "[" and l[len(l)-1] == "]":	s=True
			else:	s=False

			if v and not s and section != "":
				var = l.split("=")[0].strip()
				val = l.split("=")[1].strip()
				self._makevar(section, var, val)
			elif s and not v:
				section=l[1:len(l)-1]
				if section not in self._checklist.__dir__():
					raise Exception("Section error", section)	
				if section not in self.__dir__():
					vars(self)[section] = obj()
			else:
				raise Exception("Value error", l)

		for s in self._checklist.__dir__():
			if s[0] != "_" and type(vars(self._checklist)[s]) == "dict":
				for v in vars(self._checklist)[s].keys():
					if v not in vars(self)[s].__dir__():
						self._makevar(s, v, vars(self._checklist)[s][v]["default"])


	

	

	def _makevar(self, s, var, val):
		valid, value = self._check(s, var, val)
		if valid:
			vars(vars(self)[s])[var] = value
		else:
			raise Exception("Invalid value", str(var) + " " +str(value))			
	
	
	
	def _check(self, s, var, val):
		if self._checklist == None:
			return(True, val)
		else:
			if vars(self._checklist)[s][var]["values"] != []:
				if val not in vars(self._checklist)[s][var]["values"]:
					return(False, vars(self._checklist)[s][var]["values"])
			try:
				if vars(self._checklist)[s][var]["type"] == "int":
					val = int(val)
			except:
				return(False, vars(self._checklist)[s][var]["type"])
			if vars(self._checklist)[s][var]["type"] == "int":
				if vars(self._checklist)[s][var]["range"] != []:
					r1 = vars(self._checklist)[s][var]["range"][0]
					r2 = vars(self._checklist)[s][var]["range"][1]
					if val not in list(range(r1, r2)):
						return(False, vars(self._checklist)[s][var]["range"])
			return(True, val)
		return(False, "")
		

		
	def reload(self):
		raw = self._load()
		self._build(raw)
	
		
		
		
		
		
		
		
def test():
	import time
	t = KBConfig("testconf")
	print(t.TESTSECTION.testvar)
	print(t.TESTSECTION.testvar2 +5)
	time.sleep(10)
	t.reload()
	print(t.TESTSECTION2.testvar3)
	

	
#test()