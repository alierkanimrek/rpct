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








class MyNode(RPCTMain):
	



    #Initializing
    def prepare(self):
        pass        




    #Ready for update
    def ready(self):
        pass




    #Runs after login as a thread
    def wheel(self):        
        pass




    #Updates data before every up
    def pre_update(self):
        pass




    #Runs after every up, so messages contains commands and followed tasks data
    def post_update(self, cmds, tasks):
        pass








ctRun(MyNode)