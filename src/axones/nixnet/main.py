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








class NixNet(object):




    def __init__(self, delay:int=15):
        self._lancmd = ['cat', '/proc/net/arp']
        self._wancmd = ['wget', '-q', '-O', '-', 'ifconfig.me/ip']
        self._wanip = ""
        self._lanip = []
        self._last = 0
        self._delay = delay
        self.error = ""


    

    async def update(self):
        if int(time.time()) > self._last + self._delay:
            self._wanip = ""
            self._lanip = []
            ifc = ""
            arp = "" 
            self.error = ""
            self._last = int(time.time())
            try:    
                arp = subprocess.check_output(self._lancmd).decode("utf-8")
            except Exception as inst:
                self.error = type(inst)
            try:    
                ifc = subprocess.check_output(self._wancmd).decode("utf-8")
            except Exception as inst:
                self.error = type(inst)
            self._wanip = ifc
            for line in arp.splitlines():
                col = line.split(" ")
                if not col[0].isalpha():
                    self._lanip.append([col[0], col[len(col)-1]])



    @property
    def lanip(self):
        return(self._lanip)



    
    def devip(self, device):
        for ip in self._lanip:
            if ip[1] == device: 
                return(ip[0])
        return("")



    @property
    def wanip(self):
        return(self._wanip)
