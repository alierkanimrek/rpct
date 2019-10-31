#!/usr/bin/python
# -*- coding: utf-8 -*-


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
