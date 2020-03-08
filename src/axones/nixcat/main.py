#!/usr/bin/python
# -*- coding: utf-8 -*-




''' This source file is part of the rpclient open source project
    Copyright 2018 Ali Erkan IMREK and project authors
    Licensed under the MIT License 
'''









import subprocess









class NixCat(object):





    def __init__(self, file:str="", row:int=10):
        self.file = file
        self.row = row
        self.raw = b""
        self.utf8 = ""
        self.html = ""


    

    async def update(self, file:str="", row:int=-1):
        if(file != ""): self.file = file
        if(row != -1):  self.row = row
        try:
            self.raw = subprocess.check_output(['tail', '-'+str(self.row), self.file])
            self.utf8 = self.raw.decode("utf-8")
            self.html = self.raw.decode("utf-8").replace("\n", "</br>")
        except Exception as inst:
            self.raw = self.file.encode()+b" reading error."
            self.utf8 = self.raw.decode("utf-8")
            self.html = self.html