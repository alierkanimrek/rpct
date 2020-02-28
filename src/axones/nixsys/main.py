#!/usr/bin/python
# -*- coding: utf-8 -*-




''' This source file is part of the rpclient open source project
    Copyright 2018 Ali Erkan IMREK and project authors
    Licensed under the MIT License 
'''








import platform
import subprocess









class NixSys(object):





    def __init__(self):
        uname = platform.uname()
        arch = platform.architecture()
        self.name = uname.node
        self.release = uname.release
        self.version = uname.version
        self.machine = uname.machine
        self.arch = arch[0]
        self.cpu_model = ""
        self.cpu_processor = ""
        self.cpu_mhz = ""

        #CPU INFO
        cpuinfo = open('/proc/cpuinfo')
        cpuraw = cpuinfo.read()
        for line in cpuraw.splitlines():
            line = line.split(":")
            line[0] = line[0].strip("\t")
            if len(line) > 1:
                line[1] = line[1].strip("\t")
                if line[0] == "model name":
                    self.cpu_model = line[1]
                elif line[0] == "processor":
                    self.cpu_processor = line[1]
                elif line[0] == "cpu MHz":
                    self.cpu_mhz = line[1]

        self._prev_idle = 0
        self._prev_total = 0
        self.mem_total = 0
        self.mem_free = 0
        self.cpu_usage = 0
        #await self._cpu()
        #await self._ram()




    
    async def _ram(self):
        meminfo = open('/proc/meminfo')
        memraw = meminfo.read()
        for line in memraw.splitlines():
            line = line.split(":")
            line[0] = line[0].strip("\t")
            if len(line) > 1:
                line[1] = line[1].strip("\t")
                if line[0] == "MemTotal":
                    self.mem_total = line[1].strip(" kB")
                    self.mem_total = str(int(int(self.mem_total)/1024))
                if line[0] == "MemFree":
                    self.mem_free = line[1].strip(" kB")
                    self.mem_free = str(int(int(self.mem_free)/1024))




    
    async def _cpu(self):
        self.cpu_usage = 1

        stat = open('/proc/stat')
        raw = stat.read()
        cpu = raw.splitlines()[0].split(" ")
        user = int(cpu[2])
        nice = int(cpu[3])
        sys = int(cpu[4])
        idle = int(cpu[5])
        iow = int(cpu[6])
        irq = int(cpu[7])
        sirq = int(cpu[8])
        steal = int(cpu[9])
        current_idle = idle + iow
        current_nonidle = user + nice + sys + irq + sirq + steal
        current_total = current_idle + current_nonidle

        total = current_total - self._prev_total
        idled = current_idle - self._prev_idle
        self.cpu_usage =  int((total - idled)/total*100)
        self._prev_idle = current_idle
        self._prev_total = current_total




    
    async def _top(self):
        self.cpu_usage = 1
        self.mem_total = 100
        self.mem_free = 1
        try:
            raw = subprocess.check_output(['top','-b','-n 1'])
            lines = raw.splitlines()
            
            #MEM
            mem = str(lines[3])
            mem2 = mem.replace("  ", " ").replace("  ", " ").replace("  ", " ").split(" ")
            self.mem_total = mem2[2]
            self.mem_free = mem2[6]

            #CPU
            usage_index = str(lines[6]).index("%CPU")-1
            total = 0
            for i in range(7,len(lines)):
                total += float(str(lines[i])[usage_index:usage_index+5])
        except:
            pass




    
    async def update(self):
        r = await self._ram()
        r = await self._cpu()




    @property
    def data(self):
        data = {
            "name" : self.name,
            "release" : self.release,
            "version" : self.version,
            "machine" : self.machine,
            "arch" : self.arch,
            "cpu_model" : self.cpu_model,
            "cpu_processor" : self.cpu_processor,
            "cpu_mhz" : self.cpu_mhz,
            "mem_total" : self.mem_total,
            "mem_free": self.mem_free,
            "cpu_usage" : self.cpu_usage}
        return(data)
