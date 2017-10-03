#!/usr/bin/env python
# Copyright (c) 2017 Ruslan Variushkin,  ruslan@host4.biz
# Version 0.1

import sys
import os
from urllib2 import urlopen
from xml.dom import minidom
import config
from config import *


def sendmail(email):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    with open(reportfile, "r") as myfile:
        html = myfile.read()
    msg = MIMEMultipart('alternative')
    msg['Subject'] = Subject
    msg['From'] = username
    msg['To'] = email
    part1 = MIMEText(html, 'html', 'utf-8')
    msg.attach(part1)
    s = smtplib.SMTP(serverport)
    s.starttls()
    s.login(username, password)
    s.sendmail(username, email, msg.as_string())
    s.quit()


def Mail(account):
    URLBILL = urlBill + "/billmgr?authinfo=" + \
        userbill + ":" + passbill + "&func=user&out=xml"
    res = urlopen(URLBILL)
    xmldoc = minidom.parse(res)
    for node in xmldoc.getElementsByTagName('elem'):
        for accountBill in node.getElementsByTagName('account'):
            if accountBill.firstChild.nodeValue == account:
                # print accountBill.firstChild.nodeValue, " compare with  ",
                # account
                for email in node.getElementsByTagName('email'):
                    return email.firstChild.nodeValue


def Check(webpath, domain, email, user):
    if email is None:
        return None
    datafile = file(skipfile)
    for line in datafile:
        if email in line:
            return None
        else:
            path = Pathweb + user + "/data/" + webpath
            # print path
            cmd = "php %s --skip=%s --mode=%s --memory=%s --size=%s --delay=%s --report=%s --path=%s > %s" % (
                aibolit, skip, mode, memory, size, delay, reportfile, path, wtf)
            os.system(cmd)
            with open(wtf) as f:
                last = None
                for line in (line for line in f if line.rstrip('\n')):
                    last = line
            code = last.split()
            if int(code[2]) == 2:
                sendmail(email)
            else:
                pass


def print_user(docroot):
    for docroot in docroot:
    webpath = docroot.firstChild.nodeValue
    accountBill = Account(user)
    email = Mail(accountBill)
    print "Start Check, account Bill", accountBill, \
        "  Domain: "  + domain + \
        " Path:  " + webpath + \
        " Email: ", email
    Check(webpath, domain, email, user)


def Checkwebdomain():
    URLISP = urlISP + "/ispmgr?authinfo=" + userISP + \
        ":" + passwordISP + "&func=webdomain&out=xml"
    res = urlopen(URLISP)
    xmldoc = minidom.parse(res)
    for node in xmldoc.getElementsByTagName('elem'):
        #  print node.getElementsByTagName('name')
        for name in node.getElementsByTagName('name'):
            domain = name.firstChild.nodeValue
            for owner in node.getElementsByTagName('owner'):
                user = owner.firstChild.nodeValue
                if len(sys.argv) > 1:
                    if user == sys.argv[1]:
                        print_user(node.getElementsByTagName('docroot'))
                        return
                    else:
                        print "No such user"
                else:
                    print_user(node.getElementsByTagName('docroot'))


def Account(user):
    URLBILL = urlBill + "/billmgr?authinfo=" + \
        userbill + ":" + passbill + "&func=vhost&out=xml"
    res = urlopen(URLBILL)
    xmldoc = minidom.parse(res)
    for node in xmldoc.getElementsByTagName('elem'):
        for usernameBill in node.getElementsByTagName('username'):
            if usernameBill.firstChild.nodeValue == user:
                for account in node.getElementsByTagName('account'):
                    return account.firstChild.nodeValue




def main():
    Checkwebdomain()


if __name__ == "__main__":
    main()
