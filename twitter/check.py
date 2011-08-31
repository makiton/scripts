#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy
from pit import Pit
import sys,os
import Growl
import urllib2
import hashlib
import re

users = ['makiton', 'chiroll', 'yucca21', 'hongo', 'noisuled', 'haru_ton', 'umezo', 'mashlon', 'yu_yu_yuyu']

def get_auth():
    conf = Pit.get('twitter.com')
    auth = tweepy.OAuthHandler(conf['oauth']['consumer_key'], conf['oauth']['consumer_secret'])
    auth.set_access_token(conf['oauth']['access_key'], conf['oauth']['access_secret'])   
    return auth

def get_api():
    return tweepy.API(get_auth())

class StreamListener(tweepy.StreamListener):
    def __init__(self):
        self.growl = Growl.GrowlNotifier(applicationName="twitter", notifications=['Watch'])
        self.growl.register()
        self.image_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icon')
        tweepy.StreamListener.__init__(self)

    def get_icon(self,url):
        fname = "%s.%s" % (hashlib.md5(url).hexdigest(),url.split('.')[-1])
        cached_image = os.path.join(self.image_dir,fname)
        image = None
        if os.path.exists(cached_image):
            image = Growl.Image.imageFromPath(cached_image)
        else:
            f = open(cached_image,'wb')
            f.write(urllib2.urlopen(url).read())
            f.close()
            image = Growl.Image.imageFromPath(cached_image)
        return image

    def on_status(self, status):
        if status.user.screen_name == 'makiton':
            return
        if getattr(status, 'retweeted_status', False):
            return
        m = re.search("(http://[A-Za-z0-9\'~+\-=_.,/%\?!;:@#\*&\(\)]+)", status.text)
        if m:
            self.url_handler(m.group(1))
        icon = self.get_icon(status.user.profile_image_url)
        self.growl.notify(noteType='Watch', title='%s(%s)'%(status.user.name,status.user.screen_name), description=status.text, icon=icon, sticky=True)

    shindan_list = {}
    def url_handler(self, url):
        url = urllib2.urlopen(url).geturl()
        m = re.search('http://shindanmaker.com/([0-9]+)', url)
        if m:
            id = m.group(1)
            if self.shindan_list.has_key(id):
                return
            self.shindan_list[id] = True
            m = re.search('<div class="result">\n\t<div style="padding: 10px; font-size: 2em;">\n\t(.+)</div>', urllib2.urlopen(url, data='u=makiton').read())
            if m:
                get_api().update_status(m.group(1).decode('utf_8')+' '+url)
        else:
            os.system('open '+url)

def auto_follow_remove():
    api = get_api()
    followers = set(api.followers_ids())
    friends = set(api.friends_ids())

    try:
        # follow
        for id in list(followers-friends):
            api.create_friendship(user_id=id)

        # unfollow
        for id in list(friends-followers):
            api.destroy_friendship(user_id=id)
    except tweepy.TweepError,e:
        pass

def main():
    stream = tweepy.Stream(get_auth(), StreamListener() )

    auto_follow_remove()

    user_ids = []
    for user in get_api().lookup_users(screen_names=users):
        user_ids.append(user.id)
    stream.filter(follow=user_ids)

if __name__ == '__main__':
    main()
