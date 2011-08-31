require 'rubygems'
require 'twitter'
require 'tmail'
require 'net/smtp'
require 'pp'

CONSUMER_KEY = 'IcWO1rwsHmiAKC5Hwp7JgA'
CONSUMER_SECRET = 'AuUdpuMTPzgVQSfglleLcbmOCdRYr25tbLFSfRmiWI'
# @makiton
ACCESS_TOKEN = '9493982-rkYkDMAaifw98dRpzy6ANCBvRbVt4VGIjnSs21lMw'
ACCESS_SECRET = 'DMID3bOAYKgdb0yHiAeXp8volfgvEAWFhNbtuvmbh4I'

EXCEPT = [
	'jinrotter',
	'favotter503',
	'bot_neko',
	'twneru',
]

oauth = Twitter::OAuth.new(CONSUMER_KEY, CONSUMER_SECRET)
oauth.authorize_from_access(ACCESS_TOKEN, ACCESS_SECRET)
twitter = Twitter::Base.new(oauth)
follower = twitter.follower_ids
following = twitter.friend_ids

remove_names = []
(following - follower).each do |id|
	next if EXCEPT.index(twitter.user(id)['screen_name'])
	screen_name = twitter.friendship_destroy(id)['screen_name']
	remove_names << screen_name
end

follow_names = []
(follower - following).each do |id|
	screen_name = twitter.friendship_create(id)['screen_name']
	follow_names << screen_name
end

# send mail
unless(follow_names.empty? and remove_names.empty?)
  def twitter_url(screen_name)
    'http://twitter.com/'+screen_name
  end 
  body = 'follow:'+"\n"+
  follow_names.map{|name| ' '+twitter_url(name)}.join("\n") + "\n" +
  'remove:'+"\n"+
  remove_names.map{|name| ' '+twitter_url(name)}.join("\n") + "\n"
  print body
end

