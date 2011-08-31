#-*- coding: utf-8 -*-
import urllib2
import re
import sys

if len(sys.argv)<2:
    print 'usage: stock_price.py [stock_code]'
    exit(-1)

code = sys.argv[1]
res = urllib2.urlopen('http://stocks.finance.yahoo.co.jp/stocks/detail/?code='+code)
str = res.read()
m1 = re.search('<td width="1%" valign="middle" nowrap><span class="yjFL">([0-9,]+)', str)
m2 = re.search('<p class="yjSt"><strong class="(?:red|green)Fin">([-+0-9,]+)</strong>（<strong class="(?:red|green)Fin">([-+0-9\.]+)</strong>%', str)
if not (m1 and m2):
    print '取得できませんでした(stock_code='+code+')';
    exit(-1)

print '%s %s(%s%%)' % (m1.group(1), m2.group(1), m2.group(2))

