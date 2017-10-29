#!/usr/bin/python

from steemdata import SteemData
import datetime
import json
import shelve

start_date = datetime.datetime(2017, 9, 1, 0, 0, 0, 0)
stop_date = datetime.datetime(2017, 10, 29, 0, 0, 0, 0)
tag = "utopian-io"

s = SteemData()
shelf = shelve.open("/steemdata/%s.shelf" % tag)
shelf['posts'] = list(s.Posts.find({'tags': 'utopian-io', 'created': {'$gt': start_date}, 'created': {'$lt': stop_date}}))
shelf['comments'] = list(s.Comments.find({'json_metadata.app': {'$regex': 'utopian'}, 'created': {'$gt': start_date}, 'created': {'$lt': stop_date}}))
shelf.close()
