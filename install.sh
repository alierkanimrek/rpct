#!/bin/bash

rpct=~/rpclient
updir=$rpct/.update
mkdir -p $updir

cd $updir
git clone https://github.com/alierkanimrek/rpct.git

cd rpct
cp -v $updir/rpct/upservice.sh .
cp -v $updir/rpct/rpclient.service .
cd ..
bash ./update.sh
