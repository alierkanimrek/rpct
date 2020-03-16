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