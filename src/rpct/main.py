#!/usr/bin/python
# -*- coding: utf-8 -*-




''' This source file is part of the rpclient open source project
    Copyright 2018 Ali Erkan IMREK and project authors
    Licensed under the MIT License 
'''







from tornado import httpclient, ioloop, gen


from .conf import KBConfig
from .log import KBLogger
from .timer import Timer
from .conn import Connection
from .msg import Stack, CommandData





conf = None
log = None








def ctRun(handler):
    if handler.__module__ == "__main__":
        #Init configuration and Log system 
        try:
            print("Client initializing...")

            conf = KBConfig("config","./")
            log = KBLogger(conf.CLIENT.log_file, "rpct")
            log.level = conf.CLIENT.log_level
            
            stage1 = log.job("Stage1")
            stage1.i("Configuration loaded", 
                "log_level:"+conf.CLIENT.log_level)

        except Exception as inst:
            print("Initializing failed")
            print(type(inst))
            print(inst.args)
            print(inst)
            sys.exit(-1)

        mainloop = ioloop.IOLoop.instance()
        mainloop.conf = conf
        mainloop.log = log
        application = handler(mainloop)
        stage1.i("Starting...")
        mainloop.start()









class RPCTMain(object):
    



    def __init__(self, mainloop):
        self.__mainloop = mainloop
        self.__log = mainloop.log.job("Main")
        self.__timer = Timer()
        self.__tasklist = []
        self.__followup = []
        self.__usertask = {}
        self.__taskData = Stack()
        self.__cmds = CommandData()
        self.__conn = Connection(
            server = self.conf.SERVER.url,
            atype = self.conf.USER.auth_type, 
            acode = self.conf.USER.auth_code, 
            uname = self.conf.USER.name, 
            nname = self.conf.NODE.name, 
            log = self.log,
            key = self.conf.CLIENT.key,
            cert = self.conf.CLIENT.cert)
        self.prepare()
        self.__log.i("Starting authentication...")
        self.__timer.start(self.__auth)
       

    @property
    def conf(self):
        return(self.__mainloop.conf)

    @property
    def log(self):
        return(self.__mainloop.log)

    @property
    def tasklist(self):
        return(self.__tasklist)

    @property
    def followup(self):
        return(self.__followup)


    @property
    def usertask(self):
        return(self.__usertask)


    def setTask(self, tname, data):
        if(tname in self.__tasklist):
            self.__taskData.append({
                "uname": self.conf.USER.name, 
                "nname" : self.conf.NODE.name, 
                "name": tname, 
                "id": self.conf.USER.name+"/"+self.conf.NODE.name+"/"+tname},
                data)
    

    def getTask(self, tname):
        return(self.__taskData.data(self.conf.USER.name+"/"+self.conf.NODE.name+"/"+tname))


    def updateTask(self, tname, data):
        self.__taskData.update(self.conf.USER.name+"/"+self.conf.NODE.name+"/"+tname, data)
        if(tname not in self.__tasklist):
            self.__log.w("Task name not found", tname)
    #
    #
    #Initializing
    def prepare(self):
        pass        
    #Ready for update
    async def ready(self):
        pass
    #Runs after login as a thread
    async def wheel(self):        
        pass
    #Updates data before every up
    async def pre_update(self):
        pass
    #Runs after every up, so messages contains commands and followed tasks data
    async def post_update(self):
        pass




    def taskAlias(self, tname):
        return(TaskAlias(self, tname))


    async def __auth(self):
        self.__log.d("Trying authentication")
        self.__timer.pause()
        await self.__conn.auth(self.__authResult)
        



    async def __authResult(self, status, resp={}):
        self.__timer.endtiming()
        stack = Stack()
        if status:
            stack.load(resp["stack"])
            if(stack.data("root/server/xhrclientauth")["result"] == True):
                self.__log.i("Authentication successful, starting ping...")
                await self.__parseCommands(stack)
                self.__timer.start(self.__ping)
                return()
            else:
                self.__log.i("Authentication error...")
        self.__timer.play()




    async def __parseCommands(self, stack):
        try:
            self.__tasklist = stack.data("root/server/command")["tasklist"]
            self.__log.d("Tasklist update", self.tasklist)
            for tname in self.__tasklist:
                if(not self.getTask(tname)):
                    self.setTask(tname, {})
        except: pass
        try:    
            self.__followup = stack.data("root/server/command")["followup"]
            #self.__log.d("Followings update", self.followup)
            self.__cmds.cmd("followup", list(self.__followup.keys()))
        except: pass
        try:    
            self.__usertask = stack.data("root/server/command")["task"]
        except: pass





    async def __ping(self):
        self.__timer.pause()
        #Send followup uri list
        await self.__conn.ping(self.__pingResult, self.__cmds)




    async def __pingResult(self, status, resp={}):
        self.__timer.endtiming()
        stack = Stack()
        if status:
            stack.load(resp["stack"])
            if(stack.data("root/server/xhrclientping")["result"] == True):
                if(stack.data("root/server/xhrclientping")["awake"] == True):
                    self.__log.i("Awakening...")
                    await self.__parseCommands(stack)
                    self.__timer.start(self.__update)
                    return()
                else:
                    self.__timer.play()
        else:
            self.__timer.start(self.__auth)
            




    async def __update(self):
        self.__timer.pause()
        sendData = {}
        sendStack = Stack()
        
        await self.pre_update()
        # Convert data as {"taskname" : {task data...} ,... }
        for tdata in self.__taskData.stack:
            sendData[tdata["name"]] = tdata["data"]
        sendStack.append({
            "uname": self.conf.USER.name, 
            "nname" : self.conf.NODE.name, 
            "name": "", 
            "id": self.conf.USER.name+"/"+self.conf.NODE.name},
            sendData)
        await self.__conn.update(self.__updateResult, sendStack)




    async def __updateResult(self, status, resp={}):
        self.__timer.endtiming()
        stack = Stack()
        if status:
            stack.load(resp["stack"])
            if(stack.data("root/server/xhrclientupdate")["result"] == True):
                if(stack.data("root/server/xhrclientupdate")["awake"] == True):
                    await self.__parseCommands(stack)
                    await self.post_update()
                    self.__usertask = {}
                    self.__timer.play()
                    return()
                else:
                    self.__log.d("Sleeping...")
        self.__timer.start(self.__ping)








class TaskAlias(object):




    def __init__(self, manager, tname):
        super(TaskAlias, self).__init__()
        self.__manager = manager
        self.__name = tname


    @property
    def name(self):
        return(self.__name)
    
    
    @property
    def data(self):
        return(self.__manager.getTask(self.__name))


    @data.setter
    def data(self, data):
        self.__manager.updateTask(self.__name, data)

    