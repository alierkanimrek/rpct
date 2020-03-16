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









import os



path, filename = os.path.split(os.path.abspath(__file__))




SERVER = {}

SERVER["url"] = {
	"type" : "str", 
	"values": [],	
	"default" : "https://rplexus.net"
	}


CLIENT = {}

CLIENT["run_path"] = {
	"type" : "str", 
	"values": [],
	"default" : path
	}

CLIENT["log_file"] = {
	"type" : "str", 
	"values": [],
	"default" : path+"/rpct.log"
	}

CLIENT["log_level"] = {
	"type" : "str", 
	"values" : ["CRITICAL","ERROR","WARNING","INFO","DEBUG","NOTSET"],
	"default" : "DEBUG"
	}

CLIENT["key"] = {
	"type" : "str", 
	"values": [],	
	"default" : "client-key.pem"
	}

CLIENT["cert"] = {
	"type" : "str", 
	"values": [],	
	"default" : "client-cert.pem"
	}


USER = {}

USER["name"] = {
	"type" : "str", 
	"values": [],
	"default" : ""
	}

USER["auth_type"] = {
	"type" : "str", 
	"values": ["KEY", "CODE"],
	"default" : "CODE"
	}


USER["auth_code"] = {
	"type" : "str", 
	"values": [],
	"default" : ""
	}



NODE = {}

NODE["name"] = {
	"type" : "str", 
	"values": [],
	"default" : ""
	}
