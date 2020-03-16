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








import time
from tornado import ioloop







class Timer(object):




	min = 4000




	def __init__(self):
		self._callback = self.__fakecb
		self.looptime = self.min
		self._starttime = 0
		self._endtime = 0
		self.delay = 0
		self._period = ioloop.PeriodicCallback( 
					self._back,
					self.looptime)
		


	def __fakecb(self):
		pass




	def setCallback(self, cb):
		self._callback = cb




	def start(self, cb):
		self._callback = cb
		#self._starttime = 0
		#self._endtime = 0
		#self.looptime = self.min
		self._period.callback_time = self.looptime
		self._period.start()




	async def _back(self):
		if self._starttime > 0:
			self.looptime = (((self._endtime - self._starttime)+self.delay)*1000)+self.min
		if self.looptime <= 0:	self.looptime = self.min
		self._period.callback_time = self.looptime
		self._starttime = int(time.time())
		await self._callback()




	def pause(self):
		self._period.stop()




	def play(self):
		self._period.start()




	def endtiming(self, delay=0):
		self.delay = delay
		self._endtime = int(time.time())




	def is_running(self):
		return(self._period.is_running())