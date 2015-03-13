#!/usr/bin/env python

import cgi, sqlite3, json
from os import environ

conn = sqlite3.connect("test.db")
curs = conn.cursor()

cookie={}

if 'HTTP_COOKIE' in environ:
	#print 'Conten-type: text/html'
	#print
	#print '1'
	
	for pair in environ['HTTP_COOKIE'].split(';'):
		if pair.startswith('username'):
			(key,value) = pair.strip().split('=')
			cookie[key] = value
			break

form = cgi.FieldStorage()
curs.execute("SELECT userid FROM user WHERE username=?", [cookie['username'], ])
userid, = curs.fetchone()
topic_name = form.getvalue('topic_name', None)
domain_name = form.getvalue('domain_name', None)
new_topic_name = form.getvalue('new_topic_name', None)

if new_topic_name:
	curs.execute("UPDATE topic SET topic_name= ? WHERE topic_name = ?", [new_topic_name, topic_name])
else:
	curs.execute("SELECT domain_id FROM domain WHERE domain_name = ?", [domain_name,])
	domain_id, = curs.fetchone()
	curs.execute("SELECT * FROM topic WHERE topic_name = ?", [topic_name,])
	result = curs.fetchone()
	if not result:
		curs.execute("INSERT INTO topic VALUES(NULL,?,?,?)",[topic_name, userid, domain_id])
print 'Content-type: text/html'
print
print '''
<!DOCTYPE HTML>
<html>
	<head>
		<meta charset=UTF-8>
		<title>data handler</title>
	<body>
	</body>
</html>
'''

conn.commit()
conn.close()
