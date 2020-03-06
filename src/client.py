#!/usr/bin/python
# -*- coding: utf-8 -*-




''' This source file is part of the rpclient open source project
    Copyright 2018 Ali Erkan IMREK and project authors
    Licensed under the MIT License 
'''








#import sys
#import os
#spath = os.path.dirname(os.path.realpath(__file__))
#if spath not in sys.path:    sys.path.append(spath)

from rpct import RPCTMain, ctRun
from axones import NixSys, NixCat

import random






class MyNode(RPCTMain):
	



    #Initializing
    def prepare(self):
        self.file = "/home/ali/rplexus2/rpdev/tornado_root/rplexus.log"
        self.row = 10
        self.test = self.taskAlias("test")
        self.test2 = self.taskAlias("test2")
        self.test3 = self.taskAlias("test3") 
        self.test4 = self.taskAlias("test4") 
        self.test5 = self.taskAlias("test5") 
        self.test6 = self.taskAlias("test6") 
        self.test7 = self.taskAlias("test7")
        self.test8 = self.taskAlias("test8")

        self.sys = NixSys()
        self.mlog = NixCat(self.file, self.row)
        



    #Ready for update
    async def ready(self):
        pass




    #Runs after login as a thread
    async def wheel(self):        
        pass




    #Updates data before every up
    async def pre_update(self):
        await self.sys.update()
        await self.mlog.update()

        self.test.data = False
        self.test2.data = False

        if(random.randrange(10) > 5):   self.test.data = True 
        if(random.randrange(10) > 5):   self.test2.data = True 
        
        self.test3.data = self.sys.data["cpu_usage"]
        self.test4.data = self.sys.data["mem_free"]
        self.test5.data = self.sys.data["mem_total"]
        self.test6.data = self.mlog.data["utf-8"]
        self.test7.data = self.file
        self.test8.data = self.row




    #Runs after every up, so messages contains commands and followed tasks data
    async def post_update(self):
        pass
        #print("Follow up:", self.followup)








ctRun(MyNode)