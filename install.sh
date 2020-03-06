#!/bin/bash

rpct=~/rpclient
mkdir -p $rpct

curl https://raw.githubusercontent.com/alierkanimrek/rpct/master/upservice.sh>$rpct/upservice.sh
curl https://raw.githubusercontent.com/alierkanimrek/rpct/master/update.sh>$rpct/update.sh

cd $rpct
bash ./update.sh