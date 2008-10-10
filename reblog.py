#!/usr/bin/env python

# reblog.py:  posts entries from a syndication feed
#   to a MetaWeblog API blog
#
# This code is part of an article that is
# copyright (c) 2004 William C. Benton
#
# Redistribution, modification, etc. of this code (but not
# the article) are welcome under the terms of the GNU GPL

import feedparser
import xmlrpclib
import sys
import time

def itemize(e):
    """Extracts the properties necessary to make an RSS 2.0 item from a feedparser entry"""
    return {"title" : e.title, "link" : e.link, "pubDate" : e.modified, "modified" : e.modified, "description" : e.content[0].value}


def makePost(server, user, passwd, struct):
    time.sleep(2)           # avoid hammering the server
    return server.metaWeblog.newPost("0", user, passwd, struct, True)

def doReblog(fromUrl, toUrl, user, passwd):
    """ reblogs entries found in feed at fromUrl to XML-RPC interface at toUrl, using username and password provided.  Returns a list of new post ID numbers"""
    
    myServer = xmlrpclib.Server(toUrl)

    toReblog = feedparser.parse(fromUrl)

    return [makePost(myServer, user, passwd, itemize(e)) for e in toReblog.entries]

def main(args):
    if len(args) < 5:
        print "usage:  %s fromUrl toUrl user passwd" % args[0]
        sys.exit()

    newEntries = doReblog(args[1],args[2],args[3],args[4])

    for post in newEntries:
        print "published a post with ID %s" % post

main(sys.argv)
