#!/usr/bin/env python

import sqlite3

def fetch(current_user):
	vcontent = ''
	print current_user
	curs.execute("SELECT userid, last_topic_id FROM user WHERE username = ?", [current_user,])
	(userid, last) = curs.fetchone()
	curs.execute("SELECT topic_id, topic_name FROM topic WHERE userid = ?", [userid,])
	for item in curs.fetchall():
		if item[0] != last:
			vcontent += '<option value=' + item[1].encode('UTF-8') + '>' + item[1].encode('UTF-8') + '</option>\n'
		else:
			vcontent += '<option value=' + item[1].encode('UTF-8') + ' selected="selected"' +'>' + item[1].encode('UTF-8') + '</option>\n'
	return vcontent

conn = sqlite3.connect('test.db')
curs = conn.cursor()
''''
curs.execute("SELECT username, password FROM user")
users = {}
print curs.fetchall()
for item in curs.fetchall():
	(username, password) = item
	users[username.encode('UTF-8')] = password.encode('UTF-8')
print users

print fetch('admin')


curs.execute("UPDATE user SET last_topic_id = ? WHERE username = ?", [3, 'admin'])
conn.commit()
'''
curs.execute("SELECT * from user")
print curs.fetchall()

conn.close()
