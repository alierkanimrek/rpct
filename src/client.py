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









from rpct import RPCTMain, ctRun
import random, time






class MyNode(RPCTMain):
	



    #Initializing
    def prepare(self):
        self.my_random_data_1 = self.taskAlias("rnd1")
        self.my_random_data_2 = self.taskAlias("rnd2")        




    #Runs after login as a thread
    async def wheel(self):        
        #Do something
        #time.sleep(1)
        pass




    #Awakening
    async def awake(self):
        pass




    #Updates data before every up
    async def pre_update(self):
        self.my_random_data_1.data = random.randrange(10)
        self.my_random_data_1.data = random.randrange(100)




    #Runs after every up, so messages contains commands and followed tasks data
    # self.usertask = Tasks from user interface as dict
    # self.followup = Follow up tasks from other nodes as dict
    async def post_update(self):
        pass
        #print("Follow up:", self.followup)
        #print("User tasks:", self.usertask.keys)




    #Sleeping
    async def sleep(self):
        pass








ctRun(MyNode)