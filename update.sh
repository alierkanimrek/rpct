#!/bin/bash

path=$(dirname $(readlink -f $0))
repo=$path/.update
backup=$path/.backup/"$(date +%y%m%d%H%M%S)"
cd $path

#Backup
mkdir -p $backup
cp -aRv $path/rpct $backup
cp -aRv $path/axones $backup
cp * $backup

mkdir -p rpct
mkdir -p axones
mkdir -p $repo
rm -rf $repo/*

#Update
cd $repo
git clone https://github.com/alierkanimrek/rpct.git
cd $path

cp -aRv $repo/rpct/src/rpct/* rpct
dirs="$(find $repo/rpct/src/axones/* -type d)"
for d in $dirs
do
    cp -aRv $d axones
done
cp -v $repo/rpct/src/axones/* axones
cp -v $repo/rpct/src/*.py .
cp -v $repo/rpct/src/config.tmp .