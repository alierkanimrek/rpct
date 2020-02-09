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

import random






class MyNode(RPCTMain):
	



    #Initializing
    def prepare(self):
        self.test = self.taskAlias("test")
        self.test2 = self.taskAlias("test2")
        self.test3 = self.taskAlias("test3") 
        self.test4 = self.taskAlias("test4") 




    #Ready for update
    async def ready(self):
        pass




    #Runs after login as a thread
    async def wheel(self):        
        pass




    #Updates data before every up
    async def pre_update(self):
        self.test.data = False
        self.test2.data = False

        if(random.randrange(10) > 5):   self.test.data = True 
        if(random.randrange(10) > 5):   self.test2.data = True 
        
        self.test3.data = random.randrange(1000)
        self.test4.data = random.randrange(10000)




    #Runs after every up, so messages contains commands and followed tasks data
    async def post_update(self):
        print("Follow up:", self.followup)








ctRun(MyNode)