# -*- coding: utf-8 -*-
from pit import Pit
import tweepy

conf = Pit.get('twitter.com')
auth = tweepy.OAuthHandler(conf['oauth']['consumer_key'], conf['oauth']['consumer_secret'])
auth.set_access_token(conf['oauth']['access_key'], conf['oauth']['access_secret'])   

api = tweepy.API(auth)

api.update_status(u'ほげほげ')
