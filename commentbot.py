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

##sys.exit()

class Comment:
    def __init__(self):
        self.id = []
        self.link = []
        self.pubDate = []
        self.text = []

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):

    commentList = []
    inComment = 0
    inID = 0
    inLink = 0
    inPubDate = 0
    inDescription = 0

    def handle_starttag(self, tag, attrs):
        if tag == 'entry':
            self.inComment = 1
            self.commentList.append(Comment())
        if self.inComment == 1:
            if tag == 'id':
                self.inID = 1
            if tag == 'link':
                self.commentList[-1].link.append(attrs[0][1])
            if tag == 'updated':
                self.inPubDate = 1
            if tag == 'content':
                self.inDescription = 1
    def handle_endtag(self, tag):
        if tag == 'entry':
            self.inComment = 0
        if self.inComment == 1:
            if tag == 'id':
                self.inID = 0
            if tag == 'updated':
                self.inPubDate = 0
            if tag == 'content':
                self.inDescription = 0
    def handle_data(self, data):
        if self.inComment == 1:
            if self.inID == 1:
                self.commentList[-1].id.append(data)
            if self.inPubDate == 1:
                self.commentList[-1].pubDate.append(data)
            if self.inDescription == 1:
                self.commentList[-1].text.append(data)

while True:
    session = smtplib.SMTP(server, port)
    session.ehlo()
    session.starttls()
    session.ehlo
    session.login(sender, password)

    page = urllib.urlopen("https://www.sparkfun.com/feeds/comments")
    comment_feed = page.read()
    parser = MyHTMLParser()
    parser.commentList = []
    parser.feed(comment_feed)
    if parser.commentList == []:
        break
    nothing_new = 0
    with open("lastcomment.txt", 'r') as f:
        last_comment = f.readline()
##    print "last comment:"
##    print last_comment[0:20]
##    print "most recent comment:"
##    print parser.commentList[0].id[0][0:20]

    if last_comment in parser.commentList[0].id:
        nothing_new = 1
        print "Nothing new!"
        
    if nothing_new == 0:
        print "Something new!"
        for file_name in os.listdir(os.getcwd()):
            if "mailto" in file_name:
                recipient = file_name[6:-4]
                print "Searching for " + recipient
                searchList = []
                with open(file_name, 'r') as f:
                    searchList = f.readlines()
                for j in searchList:
                    for i in parser.commentList:
                        if last_comment in i.id:
                            break
                        elif j.strip() in i.link[0]:
                            print "Sending message for comment " + i.id[0]
                            subject = i.id
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
        f.write(str(parser.commentList[0].id[0]))
    time.sleep(300)


