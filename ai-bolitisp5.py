#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import sys
import os
from urllib2 import urlopen
from xml.dom import minidom

urlISP='https://ispURL:1500'
userISP='root'
passwordISP='pass'
Pathweb='/var/www/'
urlBill='https://billingURL'
userbill='userbilling'
passbill='pass'
aibolit='/root/scripts/ai-bolit/ai-bolit.php'


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
                            print "Start Check, account Bill",  accountBill ,"  Domain: "+domain +"Path:  "+webpath+" Email: ", email
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
    path=Pathweb + user+"/date/"+ webpath
    print path
    cmd="%s --exclude=jpg,png,gif --mode=2 --memory=125M --size=2M --delay=500 --report=%s --path=%s"%(aibolit,email,Path)
    os.system(cmd)

def main():
    Checkwebdomain()

if __name__ == "__main__":
    main()
    
