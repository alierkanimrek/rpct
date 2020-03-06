#!/bin/bash

path=$(dirname $(readlink -f $0))
cd $path

/bin/rm update.sh
curl https://raw.githubusercontent.com/alierkanimrek/rpct/master/update.sh>update.sh

/bin/bash ./update.sh