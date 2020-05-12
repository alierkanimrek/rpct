#!/bin/bash
# 
# This source file is part of the rpct open source project
#    Copyright 2020 Ali Erkan IMREK and project authors
#    Licensed under the MIT License 





path=$(dirname $(readlink -f $0))
cd $path
OUT=1

#1 Restart 
while [ $OUT -eq 1 ]
do
    python3 client.py
    OUT=$?
    sleep 2
done


