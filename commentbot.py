#!/usr/bin/python
import smtplib
from HTMLParser import HTMLParser
import urllib
import time
import os
import credentials

server = 'smtp.gmail.com'
port = 587

sender = credentials.sender
password = credentials.password

sys.exit()

class Comment:
    def __init__(self):
        self.title = []
        self.link = []
        self.time = []
        self.pagetitle = []
        self.text = []

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):

    commentList = []
    inComment = 0
    inTitle = 0
    inLink = 0
    inPubDate = 0
    inDescription = 0

    def handle_starttag(self, tag, attrs):
        if tag == 'item':
            self.inComment = 1
            self.commentList.append(Comment())
        if self.inComment == 1:
            if tag == 'title':
                self.inTitle = 1
            if tag == 'link':
                self.inLink = 1
            if tag == 'pubDate':
                self.inPubDate = 1
            if tag == 'description':
                self.inDescription = 1
    def handle_endtag(self, tag):
        if tag == 'item':
            self.inComment = 0
        if self.inComment == 1:
            if tag == 'title':
                self.inTitle = 0
            if tag == 'link':
                self.inLink = 0
            if tag == 'pubDate':
                self.inPubDate = 0
            if tag == 'description':
                self.inDescription = 0
    def handle_data(self, data):
        if self.inComment == 1:
            if self.inTitle == 1:
                self.commentList[-1].title.append(data)
            if self.inLink == 1:
                self.commentList[-1].link.append(data)
            if self.inPubDate == 1:
                self.commentList[-1].pubDate.append(data)
            if self.inDescription == 1:
                self.commentList[-1].text.append(data)

while True:
##if True:
    session = smtplib.SMTP(server, port)
    session.ehlo()
    session.starttls()
    session.ehlo
    session.login(sender, password)

    page = urllib.urlopen("http://www.sparkfun.com/feeds/comments")
    comment_feed = page.read()
    parser = MyHTMLParser()
    parser.commentList = []
    parser.feed(comment_feed)
    nothing_new = 0
    with open("lastcomment.txt", 'r') as f:
        last_comment = f.readline()
    print last_comment

    if last_comment in parser.commentList[0].link[0]:
        nothing_new = 1
        print "Nothing new!"

    if nothing_new == 0:
        for file_name in os.listdir(""):
            if "mailto" in file_name:
                recipient = file_name[6:-4]
                searchList = []
                with open(file_name, 'r') as f:
                    searchList = f.readlines()
                for j in searchList:
                    for i in parser.commentList:
                        if last_comment in i.link[0]:
                            break
                        elif j.strip() in i.link[0]:
                            subject = i.title
                            body = i.text
                            headers = ["From: " + sender,
                                       "Subject: " + subject[0],
                                       "To: " + recipient,
                                       "MIME-Version: 1.0",
                                       "Content-Type: text/html"]
                            headers = "\r\n".join(headers)
                            session.sendmail(sender, recipient, headers + "\r\n\r\n" + str(body)+"\n"+ str(i.link[0]))

    session.quit()
    with open("lastcomment.txt", 'w') as f:
        f.write(str(parser.commentList[0].link).split('#')[1][:-2])
    time.sleep(1800)


