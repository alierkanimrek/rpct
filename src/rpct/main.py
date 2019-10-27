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
from .msg import Stack





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
        self.__conn = Connection(
            server = self.conf.SERVER.url,
            atype = self.conf.USER.auth_type, 
            acode = self.conf.USER.auth_code, 
            uname = self.conf.USER.name, 
            nname = self.conf.NODE.name, 
            log = self.log)
        self.prepare()
        self.__log.i("Starting authentication...")
        self.__timer.start(self.__auth)
       

    @property
    def conf(self):
        return(self.__mainloop.conf)

    @property
    def log(self):
        return(self.__mainloop.log)


    #
    #
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




    def __auth(self):
        self.__log.d("Trying authentication")
        self.__conn.auth(self.__loginResult)




    def __authResult(self, status, resp={}):
        self.__conn.pause()
        if status:
            self.__timer.endtiming()
            self.__log.i("Authentication successful, starting ping...")
            stack = Stack()
            stack.load(resp["stack"])
            #tasklist = self.__get_command("tasklist", stack)
            print(stack.stack)
        else:
            self.__timer.endtiming(self.__timer.delay+1000)
        self.__conn.play()




    def __ping(self):
        self.__log.d("Trying authentication")
        self.__conn.auth(self.__loginResult)
