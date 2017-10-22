#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import json
from tweepy.streaming import StreamListener
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy import API
from ChatManager import ChatManager

class StreamListenerOverride ( StreamListener ):

    def on_data ( self, data ):

        self.Bot.handleData ( data )

    def on_error ( self, errorCode ):

        print "Error: " + str ( errorCode )

    def setBot ( self, BotToSet ):

        self.Bot = BotToSet


class TwitterBot ( ):

    def __init__ ( self ):

        self.loadConfiguration ( "twitter.ini" )
        self.authorizeAPI ( )
        self.ChatManager          = ChatManager ( )
        self.replyCharacterLimit  = 140
        self.replySuffix          = "..."
        self.splitSuffixLength    = len ( self.replySuffix )

    def loadConfiguration ( self, filePath ): 

        configuration = ConfigParser.ConfigParser ( )
        configuration.read ( filePath )

        self.consumerKey        = configuration.get ( 'consumer', 'key' )
        self.consumerSecret     = configuration.get ( 'consumer', 'secret' )
        self.accessToken        = configuration.get ( 'accessToken', 'token' )
        self.accessTokenSecret  = configuration.get ( 'accessToken', 'secret' )
        self.accountScreenName  = configuration.get ( 'account', 'owner' ).lower() 
        self.accountUserId      = configuration.get ( 'account', 'ownerId' )

    def authorizeAPI ( self ):

        self.AuthHandler = OAuthHandler ( self.consumerKey, self.consumerSecret )
        self.AuthHandler.set_access_token ( self.accessToken, self.accessTokenSecret )
        self.twitterAPI = API ( self.AuthHandler )

    def createStream ( self ):

        self.streamListener  = StreamListenerOverride ( )
        self.streamListener.setBot ( self )
        self.twitterStream   = Stream ( self.getAuthHandle ( ), self.streamListener )
        self.twitterStream.userstream ( _with = 'user' )

    def getAuthHandle ( self ):
        
        return self.AuthHandler

    def handleData ( self, data ):

        print data
        self.tweet = json.loads ( data.strip ( ) )
        self.loadTweet ( )

        if self.tweetId != "None":
            if self.isTweetCreator (  ):
                pass
            else:
                self.replyToTweet ( )

    def loadTweet ( self ):

        self.tweetId     = str ( self.tweet.get ( 'id_str', None ) )
        self.senderName  = str ( self.tweet.get ( 'user', { } ).get ( 'screen_name', None ) )
        self.tweetText   = str ( self.tweet.get ( 'text', None ) )

    def isTweetCreator ( self ):

        userAccountIDFromTweet = self.tweet.get ( 'user', { } ).get ( 'id_str', '' ) 

        return userAccountIDFromTweet == self.accountUserId

    def replyToTweet ( self ):

        self.replyText = self.ChatManager.getReplyToMessage ( self.tweetText )
        self.tagUserInReply ( self.senderName )
        self.calculateReplySplitCount ( )
        self.sendTweets ( )

    def tagUserInReply ( self, userName ):

        self.taggedUserText        = self.getTaggedUserText ( userName ) 
        self.taggedUserTextLength  = len ( self.getTaggedUserText ( userName ) )

    def getTaggedUserText ( self, userName ):

        return '@' + userName + ' '

    def calculateReplySplitCount ( self ):

        textLength            = len ( self.replyText )
        self.tweetSplitCount  = 0

        while ( self.tweetSplitCount * self.replyCharacterLimit ) < textLength:
            self.tweetSplitCount = self.tweetSplitCount + 1
            if self.tweetSplitCount > 1:
                textLength = textLength + len ( self.replySuffix ) + self.taggedUserTextLength
            else:
                textLength = textLength + self.taggedUserTextLength

    def sendTweets ( self ):

        for replyTweetText in self.getTweetsList ( ):
            self.twitterAPI.update_status ( status = replyTweetText, in_reply_to_status_id = self.tweetId )

    def getTweetsList ( self ):

        tweets = []

        if self.tweetSplitCount == 1:
            tweets.append ( self.taggedUserText + self.replyText )
        else:
            for index in range ( 0, self.tweetSplitCount ):

                splitNumber = index + 1 
                text = self.getReplySplitText ( splitNumber )
                tweets.append ( text )

        return tweets

    def getReplySplitText ( self, splitNumber ):

        splitStartIndex   = self.getReplySplitStartIndex ( splitNumber )
        splitEndIndex     = self.getReplySplitEndIndex ( splitNumber ) 
        splitReplySuffix  = self.getReplySplitSuffix ( splitNumber ) 

        return self.taggedUserText + self.replyText [ splitStartIndex : splitEndIndex  ] + splitReplySuffix

    def getReplySplitStartIndex ( self, splitNumber ):

        textStartIndex = 0    

        if splitNumber > 1:
            previousSplitNumber        = splitNumber - 1
            replyCharacterLimitIndex   = self.replyCharacterLimit  * previousSplitNumber
            splitSuffixLengthIndex     = self.splitSuffixLength    * previousSplitNumber
            taggedUserTextLengthIndex  = self.taggedUserTextLength * previousSplitNumber 

            textStartIndex = replyCharacterLimitIndex - splitSuffixLengthIndex - taggedUserTextLengthIndex

        return textStartIndex

    def getReplySplitEndIndex ( self, splitNumber ):

        if splitNumber == self.tweetSplitCount:
            return len ( self.replyText )
        else:
            replyCharacterLimitIndex   = self.replyCharacterLimit  * splitNumber
            splitSuffixLengthIndex     = self.splitSuffixLength    * splitNumber
            taggedUserTextLengthIndex  = self.taggedUserTextLength * splitNumber

            return replyCharacterLimitIndex  - splitSuffixLengthIndex - taggedUserTextLengthIndex

    def getReplySplitSuffix ( self, splitNumber ):

        if splitNumber == self.tweetSplitCount:
            return ""
        else:
            return self.replySuffix

if __name__ == '__main__':

    Bot = TwitterBot ( )
    Bot.createStream ( )

