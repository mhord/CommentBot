CommentBot
==========

Python script to watch the SparkFun comments feed and send e-mail when certain pages get commented upon.

There's a missing file here: credentials.py. It should contain two lines:

    sender = "email@gmail.com"
    password = "passwordgoeshere"
    
These should be the credentials for the e-mail address that is sending the notifications. By default,
I expect that you're using Gmail; if not, that's your own lookout.
