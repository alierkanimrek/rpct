#!/usr/bin/python
# -*- coding: utf-8 -*-




''' This source file is part of the rpclient open source project
    Copyright 2018 Ali Erkan IMREK and project authors
    Licensed under the MIT License 
'''









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
        
        self.test3.data = self.sys.cpu_usage
        self.test4.data = self.sys.mem_free
        self.test5.data = self.sys.mem_total
        self.test6.data = self.mlog.utf8
        self.test7.data = self.mlog.file
        self.test8.data = self.mlog.row




    #Runs after every up, so messages contains commands and followed tasks data
    # self.usertask = Tasks from user interface as dict
    # self.followup = Follow up tasks from other nodes as dict
    async def post_update(self):
        #print("Follow up:", self.followup)
        #print("User tasks:", self.usertask.keys)
        if("test8" in self.usertask):
            self.mlog.row = self.usertask["test8"]
        if("test7" in self.usertask):
            self.mlog.file = self.usertask["test7"]







ctRun(MyNode)