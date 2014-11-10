__author__ = 'antoniocastro'

import urllib2
sqlfile = urllib2.urlopen("https://s3.amazonaws.com/littlesis/public-data/littlesis-data.sql")
output = open('../littlesis-data.sql','wb')
output.write(sqlfile.read())
output.close()