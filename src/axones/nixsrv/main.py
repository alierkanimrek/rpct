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









import subprocess
import time








class NixSrv(object):




    def __init__(self, delay:int=5):
        self._cmd = ['systemctl', 'list-units', '--type=service', '--state=running', '--no-pager', '--no-legend']
        self._logcmd = ['journalctl', '-n', '', '-u', '', '-x', '--no-pager', '--output=export', '--output-fields=MESSAGE,SYSLOG_TIMESTAMP']
        self._running = []
        self._last = 0
        self._delay = delay


    

    async def _update(self):
        if int(time.time()) > self._last + self._delay:
            self._running = [] 
            self._last = int(time.time())
            raw = subprocess.check_output(self._cmd).decode("utf-8")
            for line in raw.splitlines():
                self._running.append(line.split(" ")[0])




    async def isRunning(self, name):
        await self._update()
        if name+".service" in self._running:    return(True)
        else:   return(False)




    async def start(self, name):
        raw = subprocess.check_output(['systemctl', 'start', name]).decode("utf-8")




    async def stop(self, name):
        raw = subprocess.check_output(['systemctl', 'stop', name]).decode("utf-8")




    async def log(self, name, last:int=5):
        cmd = self._logcmd
        cmd[cmd.index('-u')+1] = name
        cmd[cmd.index('-n')+1] = str(last)
        log = []
        msg = ""
        raw = subprocess.check_output(cmd).decode("utf-8")
        for line in raw.splitlines():
            parsed = line.split("=")
            if parsed[0] == "MESSAGE":
                msg = parsed[1]
            if parsed[0] == "SYSLOG_TIMESTAMP":                
                log.append(parsed[1]+" "+msg)
                msg = ""
        return(log)