#!/usr/bin/python
# -*- coding: utf-8 -*-




''' This source file is part of the rpclient open source project
    Copyright 2018 Ali Erkan IMREK and project authors
    Licensed under the MIT License 
'''








import time
from tornado import ioloop







class Timer(object):




	min = 2000




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
		self._starttime = 0
		self._endtime = 0
		self.looptime = self.min
		self._period.callback_time = self.looptime
		self._period.start()




	async def _back(self):
		if self._starttime > 0:
			self.looptime = (((self._endtime - self._starttime)+self.delay)*1000)+self.min
		if self.looptime == 0:	self.looptime = self.min
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