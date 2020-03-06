#!/usr/bin/python
# -*- coding: utf-8 -*-




''' This source file is part of the rpclient open source project
    Copyright 2018 Ali Erkan IMREK and project authors
    Licensed under the MIT License 
'''








import platform
import subprocess









class NixCat(object):





    def __init__(self, file:str="", row:int=10):
        self.file = file
        self.row = row
        self._raw = ""


    

    async def update(self, file:str="", row:int=-1):
        if(file != ""): self.file = file
        if(row != -1):  self.row = row
        try:
            raw = subprocess.check_output(['tail', '-'+str(self.row), self.file])
            self._raw = raw
        except Exception as inst:
            self._raw = self.file.encode()+b" reading error."
        



    @property
    def data(self):
        data = {
            "raw":self._raw,
            "utf-8":self._raw.decode("utf-8"),
            "html": self._raw.decode("utf-8").replace("\n", "</br>")}
        return(data)

