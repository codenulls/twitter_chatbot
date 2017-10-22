# Twitter Chatbot

Twitter bot is basically a program/script that controls one or more twitter accounts to perform automated tasks. We all have seen the capabilities of these bots on twitter to some extent. Don't get me wrong, I'm not talking about spam-bots, I'm talking about good-bots that can be used for good reasons.

This is a simple twitter bot that will send a reply in a single or multiple tweets depending on the size of the reply to the tweet in which we were tagged in; thus creating a chatbot. 

### Prerequisites

Python: https://www.python.org/downloads/

Tweepy: 
```
pip install tweepy
```

## Usage

Go to https://apps.twitter.com, and create your application, once your application is created then click on "Keys and Access Tokens" tab, and copy-paste that information in twitter.ini file.  

Once you have downloaded this project, extract the files to a folder if it's a zip file. Create a new python file in that folder, and add this code: 

```
from TwitterBot import TwitterBot

Bot = TwitterBot ( )
Bot.createStream ( )
```

