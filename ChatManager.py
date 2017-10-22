#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

class ChatManager ( ):

    def __init__ ( self ):

        self.phrases = {}
        self.fileLoadphrases ( "phrases.txt" )

    def fileLoadphrases ( self, fileName ):

        with open ( fileName ) as file:

            for line in file:

                if not self. isLineIgnorable ( line ):
                    self.insertLineTophrasesDictionary ( line )

    def isLineIgnorable ( self, line ):

        line = line.strip ( )

        if line == "" or line [0] == "#":
            return True

        return False


    def insertLineTophrasesDictionary ( self, line ):

        OriginalLine    = line.strip ( )
        
        line            = OriginalLine.lower ( ) 
        lineBreakIndex  = self.getLineBreakIndex ( line )

        # This line has phrases that will be used as keys 
        # to check tweets in which we are tagged in
        firstLine       = OriginalLine [ 0:lineBreakIndex ].strip ( )

        # This line is the reply to the messages,
        # separated with comma in the first line
        secondLine      = OriginalLine [ lineBreakIndex+1 : len ( OriginalLine ) ].strip ( )

        self.phrases [ firstLine ] = secondLine

    def getLineBreakIndex ( self, line ):

        lineBreakIndex = None

        for i in range ( 0, len ( line ) ):

            if line [i] == "=":
                lineBreakIndex = i

        return lineBreakIndex

    def getReplyToMessage ( self, message ):

        message    = str ( message ).strip ( ).lower ( )
        replyText  = self.getConcatenatedFoundPhrases ( message )

        return replyText.strip ( )

    def getConcatenatedFoundPhrases ( self, textToSearch ):

        resultText = ""
        for key, value in self.phrases.items():

            phrasesList = key.split(",")

            if self.isTextMatch ( textToSearch, phrasesList ):

                if resultText == "":
                    resultText = value
                else:
                    resultText = resultText + ". " + value

        return resultText

    def isTextMatch ( self, elementToCheck, list ):

        return not all ( re.search(r'\b' + value.lower ( ). strip ( ) + r'\b', elementToCheck) == None for value in list )