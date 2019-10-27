#!/usr/bin/python
# -*- coding: utf-8 -*-









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


    def i(self, msg, *args):
        self.write("I", msg, *args)

    def e(self, msg, *args):
        self.write("E", msg, *args)

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





"""
def test():
    log = KBLogger("test.log", "Test")
    log.level = "INFO"
    testjob = log.job("test", "staticvar1", "staticvar2")
    testjob.i("Info test message...", "var1", "var2", "var3")
    log.level = "ERROR"
    testjob2 = log.job("test2")
    testjob.i("Info test message...")
    testjob2.e("Error test message...")

test()
"""