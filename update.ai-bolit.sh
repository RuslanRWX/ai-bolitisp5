#!/bin/sh
PATH=/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin:/root/bin

path="/root/scripts/ai-bolit/"
if [ ! -d  $path ]; then { mkdir -p $path; } fi

rm -f ${path}ai-bolit-hoster.zip
wget -P ${path}  http://download.cloudscan.tech:28080/partners/ai-bolit-hoster.zip
unzip -o ${path}ai-bolit-hoster.zip -d $path

exit 0

