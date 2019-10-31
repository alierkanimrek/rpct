#!/usr/bin/python
# -*- coding: utf-8 -*-




''' This source file is part of the rpclient open source project
    Copyright 2018 Ali Erkan IMREK and project authors
    Licensed under the MIT License 
'''








import json

from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from tornado.httputil import HTTPHeaders
from tornado import escape

from .msg import Stack, Message








URL = {
    "login": "/xhr/ctlogin",
    "ping": "/xhr/ctping",
    "up": "/xhr/ctup"}








class Connection(object):



    def __init__(self, server, uname, nname, atype, acode, log, key, cert):
        self.log = log.job("Connection")
        self._server = server
        self._authData = Stack()
        self._source = {
            "uname": uname, 
            "nname" : nname,
            "name": "",
            "id": uname+"/"+nname+"/"}
        self._authData.append(self._source, {"code" : acode})
        self._headers = HTTPHeaders({"content-type": "application/json"})
        self._request = HTTPRequest(
            url = "",
            method = "POST",
            connect_timeout = 10,
            request_timeout = 10)
        if(key):
            self._request.client_key = key
            self._request.client_cert = cert
            self._request.validate_cert = False
        self.callback = None




    async def __run(self ):
        http_client = AsyncHTTPClient()
        try:
            response = await http_client.fetch(self._request)
        except Exception as e:
            self.log.e(str(e))
            self.callback(False)
        else:
            try:
                msg = json.loads(response.body.decode())
                #if "Set-Cookie" in response.headers:
                #    self._request.set_cookie(response.headers["Set-Cookie"])
                    #self._request.set_header("nid", response.body)
                self.callback(True, msg)
            except Exception as inst:
                self.log.e( type(inst), str(response.body))
                self.callback(False)




    async def auth(self, cb):
        self.callback = cb
        self._request.url = self._server+URL["login"]
        self._request.body = self._msg(self._authData).json()
        await self.__run()




    def _msg(self, data):
        return(
            Message(
                uname=self._source["uname"], 
                nname=self._source["nname"], 
                stack=data))








class Request(object):




    def __init__(self):
        self._conf = conf
        self._headers = HTTPHeaders({"content-type": "application/json"})
        #self._headers.add("Cookie", response.headers["Set-Cookie"].split(";")[0])
        #self._headers.add("rcode", utils.hash_codes(conf.uid, conf.rcode))
        #self._headers.add("nodename", conf.nodename)
        if conf['CLIENT']['client_key'] == "":
            self._request = HTTPRequest(
                url = "",
                method = "POST",
                connect_timeout = 10,
                request_timeout = 10)
        else:
            self._request = HTTPRequest(
                url = "",
                method = "POST",
                validate_cert = False,
                client_key = conf["CLIENT"]["client_key"],
                client_cert = conf["CLIENT"]["client_cert"],
                connect_timeout = 10,
                request_timeout = 10)





    def login(self):
        request = self._request
        request.method = "POST"
        request.url = self._conf["SERVER"]["url"]+"/login"
        request.headers = self._headers
        request.body = self.getJsonData(
            {"rcode" : self._conf["USER"]["rcode"],
            "uname" : self._conf["USER"]["uname"],
            "nodename": self._conf["USER"]["nodename"]})
        return(request)




    def ping(self):
        request = self._request
        request.method = "GET"
        request.url = self._conf["SERVER"]["url"]+"/ping"
        request.headers = self._headers
        request.headers["uname"] = self._conf["USER"]["uname"]
        request.body = None
        return(request)




    def update(self, data = {}):
        request = self._request
        request.method = "POST"
        request.url = self._conf["SERVER"]["url"]+"/update"
        request.headers = self._headers
        request.body = self.getJsonData(data)
        return(request)




    def set_cookie(self, cookie):
        self._headers.add("Cookie", cookie)
        



    def set_header(self, name, data):
        if name in self._headers:
            self._headers[name] = data
        else:
            self._headers.add(name, data)    




    def getJsonData(self, data):
        #return(escape.utf8(json.dumps(data)))
        return(escape.utf8(json.dumps(data,indent=4, separators=(',', ': '))))












class Client(object):




    def __init__(self, conf):
        self._request = Request(conf)
        self.__status = False

    @property
    def running(self):
        return(self.__status)




    def auth(self, callback):
        if self.__status:            return()

        self.__status = True
        self._callback = callback
        AsyncHTTPClient().fetch( self._request.login(), 
            self._code_response)




    def _code_response(self, response):
        if not response.error:
            try:
                msg = json.loads(response.body.decode())
            except:
                self._callback(False, response.body.decode())
            else:
                if "Set-Cookie" in response.headers:
                    self._request.set_cookie(response.headers["Set-Cookie"])
                    #self._request.set_header("nid", response.body)
                    self._callback(True, msg)
                else:
                    self._callback(False, response.body.decode())
        else:
            self._callback(False, str(response.error))
        self.__status = False




    def ping(self, callback):
        if self.__status:            return()        
        self.__status = True
        self._callback = callback
        AsyncHTTPClient().fetch( self._request.ping(), 
            self._ping_response)




    def _ping_response(self, response):
        if not response.error:
            try:
                msg = json.loads(response.body.decode())
            except:
                self._callback(False, response.body.decode())
            else:
                self._callback(True, msg)
        else:
            self._callback(False, str(response.error))
        self.__status = False




    def update(self, callback, data={}):
        if self.__status:            return()
        self._callback = callback
        AsyncHTTPClient().fetch( self._request.update(data), 
            self._update_response)




    def _update_response(self, response):
        if not response.error:
            try:
                msg = json.loads(response.body.decode())
                stack = Stack()
                stack.load(msg["stack"])
                self._callback(True, stack)
            except:
                self._callback(False, response.body.decode())
        else:
            self._callback(False, str(response.error))
