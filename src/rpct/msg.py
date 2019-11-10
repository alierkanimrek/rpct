#!/usr/bin/python
# -*- coding: utf-8 -*-


''' All rights reserved (c) 2018 Ali Erkan IMREK <alierkanimrek@gmail.com> '''








import json




def get_uri(uname, nname, name):
    return(uname+"/"+nname+"/"+name)








def get_names_from_uri(uri):
    if uri[0] == "/":
        return(uri[1:].split("/"))
    else:
        return(uri.split("/"))










class Stack(object):



    def __init__(self):
        self._stack = {}



    def append(self, source, data={}):
        checklist = [
            "id", 
            "name", 
            "uname",
            "nname"]
        if type(source) == type({}) and type(data) == type({}):
            for c in checklist:
                if c not in source:
                    return()
        else:
            return()
        src = {
            "uname": source["uname"],
            "nname" : source["nname"],
            "name": source["name"],
            "id": get_uri(source["uname"], source["nname"], source["name"]),
            "data": data}
        if not self.data(src["id"]):
            self._stack[src["id"]] = src




    def update(self, uri, data):
        try:
            self._stack[uri]["data"] = data
        except:
            pass




    def data(self, uri):
        try:
            return(self._stack[uri]["data"])
        except:
            pass




    def delete(self, uri):
        try:
            del self._stack[uri]
        except:
            pass
            



    @property
    def stack(self):
        out = []
        for k in self._stack.keys():
            out.append(self._stack[k])
        return(out)




    def load(self, stacklist):
        self._stack = {}
        for stack in stacklist:
            try:
                self.append(stack, stack["data"])
            except:
                pass




    def id(self, uri):
        try:
            return(self._stack[uri]["id"])
        except:
            pass










class CommandData(object):
    



    def __init__(self, name="", data=""):
        self._data = {}
        if name != "":  
            self.cmd(name, data)




    def cmd(self, name, data):
        self._data[name] = data




    def remove(self, name):
        del self._data[name]




    @property
    def data(self):
        out = {}
        for k in self._data.keys():
            out[k] = self._data[k]
        return(out)






        
class Message(object):



    def __init__(self, uid=None, nid=None, uname=None, nname=None, stack=Stack):
        self._msg = {
            "uid" : uid,
            "nid" : nid,
            "uname" : uname,
            "nname" : nname,
            "stack" : stack.stack
        }





    @property
    def dump(self):
        dump = self.json()
        return(json.loads(dump))



    
    def json(self, human=False):
        if human:
            return(json.dumps(self._msg, indent=4, separators=(',', ': ')))
        else:
            return(json.dumps(self._msg))
    







def jdump(dump):
    try:
        return(json.dumps(dump, indent=4, separators=(',', ': ')))
    except:
        pass





"""
import json


stack = Stack()
stack.append({ 
    "uname":"ali", 
    "nname":"test", 
    "name":"system_statics", 
    "id":"349857"}, 
    {"data":123})
stack.append({"uid":"456", 
    "nid":"123", 
    "uname":"ali", 
    "nname":"test1", 
    "name":"system_dynamics", 
    "id":"349858"}, 
    {"data":9837})
print("____________\n",jdump(stack.stack))
s = stack.stack
stack.delete(uri="ali/test/system_statics")
print("____________\n", jdump(stack.stack))
stack.update("ali/test1/system_dynamics", {"data": 321})
print("____________\n",jdump(stack.stack))
dynamics = stack.data("ali/test1/system_dynamics")
stack.load(s)
print("____________\n",jdump(stack.stack))
msg = Message( uname="ali", nname="test", stack=stack)
print(msg.json(human=True))


c = CommandData("ping", {"d1":"ali"})
print(c.data)
c.cmd("ping", {"d1":"veli"})
c.cmd("ax", {"x":"ali"})
print(c.data)
c.remove("ping")
print(c.data)
"""