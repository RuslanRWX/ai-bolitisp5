#!/usr/bin/env python
# Copyright (c) 2017 Ruslan Variushkin,  ruslan@host4.biz
# Version 0.1 
 
import sys
import os
from urllib2 import urlopen
from xml.dom import minidom

#  ISP url
urlISP='https://ispURL:1500'
# isp accesses, user/password 
userISP='root'
passwordISP='pass'
# local isp path , default is /var/www
Pathweb='/var/www/'
# BILLmanager URL
urlBill='https://billingURL'
#Billmanager accesses , user/password
userbill='userbilling'
passbill='pass'
# Ai-bolit script path 
aibolit='/root/scripts/ai-bolit/ai-bolit.php'

#ai-bolit parameters 
skip='jpg,png,gif,jpeg,JPG,PNG,GIF,bmp,xml,zip,rar,css,avi,mov'
mode='2'
memory='125M'
size='2M'
delay='500'


def Checkwebdomain ():
    URLISP= urlISP+ "/ispmgr?authinfo="+userISP+":"+passwordISP+"&func=webdomain&out=xml"
    res = urlopen(URLISP)
    xmldoc = minidom.parse(res)
    for node in xmldoc.getElementsByTagName('elem'):
        #  print node.getElementsByTagName('name')
        for name in node.getElementsByTagName('name'): 
            domain=name.firstChild.nodeValue
            for owner in node.getElementsByTagName('owner') :
                user=owner.firstChild.nodeValue
                if len(sys.argv) > 1:
                    if user == sys.argv[1]:
                        #print user
                        for docroot in node.getElementsByTagName('docroot') :
                            webpath=docroot.firstChild.nodeValue
                            accountBill=Account(user)
                            email=Mail(accountBill)
                            print "Start Check, account Bill",  accountBill ,"  Domain: "+domain +" Path:  "+webpath+" Email: ", email
                            Check(webpath, domain, email, user)
                            exit (0)
                else:
                    for docroot in node.getElementsByTagName('docroot') :
                        webpath=docroot.firstChild.nodeValue
                        accountBill=Account(user)
                        email=Mail(accountBill)
                        print "Start Check, account Bill",  accountBill ,"  Domain: "+domain +"Path:  "+webpath+" Email: ", email
                        Check(webpath, domain, email, user)

def Account (user):
    URLBILL= urlBill+"/billmgr?authinfo="+userbill+":"+passbill+"&func=vhost&out=xml"
    res = urlopen(URLBILL)
    xmldoc = minidom.parse(res)
    for node in xmldoc.getElementsByTagName('elem'):
         for usernameBill in node.getElementsByTagName('username'):
            if usernameBill.firstChild.nodeValue == user:
                for account in node.getElementsByTagName('account'):
                    return account.firstChild.nodeValue
                    
    
def Mail(account):
    URLBILL= urlBill+"/billmgr?authinfo="+userbill+":"+passbill+"&func=user&out=xml"
    res = urlopen(URLBILL)
    xmldoc = minidom.parse(res)
    for node in xmldoc.getElementsByTagName('elem'):
        for accountBill in node.getElementsByTagName('account'):
            if accountBill.firstChild.nodeValue == account:
                #print accountBill.firstChild.nodeValue, " compare with  ",  account
                for email in node.getElementsByTagName('email'):
                    return  email.firstChild.nodeValue 


def Check(webpath, domain, email, user):
    MyPath=os.getcwd()
    datafile = file('skipemails.txt')
    for line in datafile:
        if email in line:
            pass
        else:
            path=Pathweb + user+"/data/"+ webpath
            #print path
            cmd="php %s --skip=%s --mode=%s --memory=%s --size=%s --delay=%s --report=%s --path=%s"%(aibolit,skip,mode,memory,size,delay,email,path)
            os.system(cmd)

def main():
    Checkwebdomain()

if __name__ == "__main__":
    main()
    
