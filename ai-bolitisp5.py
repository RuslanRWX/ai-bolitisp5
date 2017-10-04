#!/usr/bin/env python
# Copyright (c) 2017 Ruslan Variushkin,  ruslan@host4.biz
# Version 0.1

import sys
import os
from urllib2 import urlopen
from xml.dom import minidom
import config
from config import *
from shutil import copyfile


def Checkwebdomain():

    def print_user():
        for docroot in node.getElementsByTagName('docroot'):
            webpath = docroot.firstChild.nodeValue
            accountBill = Account(user)
            email = User(accountBill, search="email")
            id = User(accountBill, search="account_id")
            lang = Lang(id)
            print "Start Check, account Bill", accountBill, \
                  " Domain: "  + domain + \
                  " Path:  " + webpath + \
                  " Email: ", email + \
                  " Lang: ", lang
            Check(webpath, email, user, lang)

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
                        print_user()
                        return
                else:
                    print_user()


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



def User(account,search):
    URLBILL = urlBill + "/billmgr?authinfo=" + \
        userbill + ":" + passbill + "&func=user&out=xml"
    res = urlopen(URLBILL)
    xmldoc = minidom.parse(res)
    for node in xmldoc.getElementsByTagName('elem'):
        for accountBill in node.getElementsByTagName('account'):
            if accountBill.firstChild.nodeValue == account:
                if search == "email":
                    for email in node.getElementsByTagName('email'):
                        return email.firstChild.nodeValue
                if search == "account_id":
                    for account_id in node.getElementsByTagName('account_id'):
                        return account_id.firstChild.nodeValue

def Lang(id):
    URLBILL = urlBill + "/lang.php?id="+str(id)
    query= urlopen(URLBILL)
    result = query.read()
    return result



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


def Check(webpath, email, user, lang):
    path=os.getcwd()
    if lang == "en":
        lang = "eng"
        design_path = path +"/ai-design.html.eng"
    else:
        lang = "ru"
        design_path = path + "/ai-design.html.ru"
    if email is None:
        return None
    datafile = file(skipfile)
    for line in datafile:
        if email in line:
            return None
        else:
            path = Pathweb + user + "/data/" + webpath
            # print path
            cmd = "php %s --skip=%s --mode=%s --memory=%s --size=%s --delay=%s --report=%s --path=%s --%s > %s" % (
                aibolit, skip, mode, memory, size, delay, reportfile, path, lang, wtf)
            copyfile(design_path, aibolit_path+"/ai-design.html")
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




def main():
    Checkwebdomain()


if __name__ == "__main__":
    main()
