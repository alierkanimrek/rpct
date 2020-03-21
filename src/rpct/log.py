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








import sys
import traceback
import logging
from logging.handlers import TimedRotatingFileHandler
from logging import handlers









LOG_LEVELS={
    "CRITICAL":50,
    "ERROR":40,
    "WARNING":30,
    "INFO":20,
    "DEBUG":10,
    "NOTSET":0}




LOG_WHEN=["S", "M", "H", "D", "W0", "W1", "W2", "W3", "W4", "W5", "W6", "midnight"]








class KBLogger:



    def __init__(self, fn, name=""):
        self._fn = fn
        self._name = name
        self._level = "DEBUG"
        self._when = "D"
        self._interval = 1
        self._backupCount = 7
        self._format = "%(asctime)s - %(levelname)s - %(message)s"
        self.log = logging.getLogger(self._name)
        self._fh = ""
        self._setup()




    @property
    def level(self):
        return(self._level)

    @level.setter
    def level(self, level):
        if level in LOG_LEVELS.keys():
            self._level = level
            self.log.setLevel(LOG_LEVELS[self._level])

    @property
    def when(self):
        return(self._when)

    @when.setter
    def when(self, when):
        if when in LOG_WHEN:
            self._when = when
            self._setup()

    @property
    def interval(self):
        return(self._interval)

    @interval.setter
    def interval(self, interval):
        self._interval = interval
        self._setup()

    @property
    def backupCount(self):
        return(self._backupCount)

    @backupCount.setter
    def backupCount(self, backupCount):
        self._backupCount = backupCount
        self._setup()

    @property
    def format(self):
        return(self._format)

    @format.setter
    def format(self, format):
        self._format = format
        self._setup()




    def _setup(self):
        fformat = logging.Formatter(self._format)
        if self._fh != "": 
            self.log.removeHandler(self._fh)
        self._fh = handlers.TimedRotatingFileHandler(
            self._fn,
            when = self._when,
            interval = self._interval,
            backupCount = self._backupCount)
        self._fh.setFormatter(fformat)
        self.log.addHandler(self._fh)
        


    def job(self, name, *args):
        return(KBLoggerJob(self, name, list(args)))











class KBLoggerJob:


    def __init__(self, logger, name, args):
        self._logger = logger
        self._job = name
        self._statics = args
        self._lastmsg = ""


    def i(self, msg, *args):
        self.write("I", msg, *args)

    def e(self, msg, *args):
        self.write("E", msg, *args)

    def e_tb(self, msg, inst, *args):
        self.e(msg, *args)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        last = traceback.format_tb(exc_traceback)[len(traceback.format_tb(exc_traceback))-1]
        self.d(type(inst), inst.args, last)

    def c(self, msg, *args):
        self.write("C", msg, *args)

    def w(self, msg, *args):
        self.write("W", msg, *args)

    def d(self, msg, *args):
        self.write("D", msg, *args)


    def write(self, typ, msg, *args):
        msglist = self._statics + [msg] + list(args)
        msg = self._job
        for i in msglist:
            msg += " - " + str(i)
        if self._lastmsg != msg:
            if typ == "C":
                self._log.critical(msg)
            if typ == "E":
                self._logger.log.error(msg)
            if typ == "W":
                self._logger.log.warning(msg)
            if typ == "I":
                self._logger.log.info(msg)
            if typ == "D":
                self._logger.log.debug(msg)
            if typ == "N":
                self._logger.log.notset(msg)
            self._lastmsg = msg
        else:
            self._logger.log.debug(msg)





def test():
    log = KBLogger("test.log", "Test")
    log.level = "INFO"
    testjob = log.job("test", "staticvar1", "staticvar2")
    testjob.i("Info test message...", "var1", "var2", "var3")
    log.level = "ERROR"
    testjob2 = log.job("test2")
    testjob.i("Info test message...")
    testjob2.e("Error test message...")

#test()