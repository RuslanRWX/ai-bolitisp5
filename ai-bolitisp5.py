#!/usr/bin/env python
# Copyright (c) 2017 Ruslan Variushkin,  ruslan@host4.biz
# Version 0.3

import sys
import os
from urllib2 import urlopen
from xml.dom import minidom
import config
from config import *
from shutil import copyfile
from time import gmtime, strftime
import re
import urllib2,cookielib

reload(sys)
sys.setdefaultencoding('utf-8')

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}


def log(text):
    logf = open(logfile, "a")
    logf.write(text)
    logf.close()

def request_http(query):
    result = urllib2.Request(query, headers=hdr)
    result_api = urlopen(result)
    return  minidom.parse(result_api)


def Checkwebdomain():

    def print_user():
        webpath = name_isp+"/data/www"
        accountBill = Account(name_isp)
        email = User(accountBill, search="email")
        id = User(accountBill, search="account_id")
        lang = Lang(id)
        if email is None:
            text = "error not email user:{user}\n".format(user=name_isp)
            log(text)
            return
        print "Start Check, account Bill", accountBill, \
              " Path:  " + webpath + \
              " Email: ", email + \
              " Lang: ", lang
        Check(webpath, email, name_isp, lang)

    URLISP = urlISP + "/ispmgr?authinfo=" + userISP + \
        ":" + passwordISP + "&func=user&out=xml"
    res = urlopen(URLISP)
    xmldoc = minidom.parse(res)
    for node in xmldoc.getElementsByTagName('elem'):
        #  print node.getElementsByTagName('name')
        for name in node.getElementsByTagName('name'):
            name_isp = name.firstChild.nodeValue
            if len(sys.argv) > 1:
                if name_isp == sys.argv[1]:
                    print_user()
                    return
            else:
                print_user()


def Account(user):
    query = urlBill + "/billmgr?authinfo=" + \
        userbill + ":" + passbill + "&func=vhost&out=xml"
    xmldoc = request_http(query)
    for node in xmldoc.getElementsByTagName('elem'):
        for usernameBill in node.getElementsByTagName('username'):
            if usernameBill.firstChild.nodeValue == user:
                for account in node.getElementsByTagName('account'):
                    return account.firstChild.nodeValue



def User(account,search):
    URLBILL = urlBill + "/billmgr?authinfo=" + \
        userbill + ":" + passbill + "&func=user&out=xml"
    xmldoc = request_http(URLBILL)
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



def sendmail(email, lang):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    with open(reportfile, "r") as myfile:
        html = myfile.read()
    msg = MIMEMultipart('alternative')
    if lang == "eng":
        msg['Subject'] = SubjectEng
    if lang == "ru":
        msg['Subject'] = SubjectRus
    msg['From'] = headerfrom
    msg['To'] = email
    part1 = MIMEText(html, 'html', 'utf-8')
    msg.attach(part1)
    s = smtplib.SMTP(serverport)
    s.starttls()
    s.login(username, password)
    s.sendmail(username, email, msg.as_string())
    s.quit()


def Check(webpath, email, user, lang):
    path=MainPath
    if lang == "en":
        lang = "eng"
        design_path = path +"/ai-design.html.eng"
    else:
        lang = "ru"
        design_path = path + "/ai-design.html.ru"
    datafile = file(skipfile)
    for line in datafile:
        if email in line:
            return
    path = Pathweb + webpath
    try:
        os.path.isdir(path)
    except:
        return
    cmd = "php %s --skip=%s --mode=%s --memory=%s --size=%s --delay=%s --report=%s --path=%s --%s > %s" % (
        aibolit, skip, mode, memory, size, delay, reportfile, path, lang, wtf)
    copyfile(design_path, aibolit_path+"/ai-design.html")
    os.system(cmd)
    date = strftime("%Y-%m-%d %H:%M:%S")
    text = "{date} Found malware on account:{user}  sent email to:{email} path:{path} lang:{lang} \n".format(user=user, \
                                                                                                email=email, \
                                                                                                date=date, \
                                                                                                path=path, \
                                                                                                lang=lang )
    with open(wtf) as f:
        last = None
        for line in (line for line in f if line.rstrip('\n')):
            last = line
    code = last.split()
    if int(code[2]) == 2:
        log(text)
        sendmail(email, lang)
    else:
        pass


def main():
    Checkwebdomain()


if __name__ == "__main__":
    date=strftime("%Y-%m-%d %H:%M:%S")
    text = "\nStart check {date}\n".format(date=date)
    log(text)
    main()
    date=strftime("%Y-%m-%d %H:%M:%S")
    text = "\nStop check {date}\n".format(date=date)
    log(text)
