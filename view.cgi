#!/usr/bin/env python

import cgi, sqlite3
from os import environ

conn = sqlite3.connect("test.db")
curs = conn.cursor()

form = cgi.FieldStorage()
topic_name = form.getvalue("topic_name", None)
#topic_name = "Illicit_Goods_topic1"
curs.execute("SELECT userid FROM topic WHERE topic_name = ?" ,[topic_name,])
userid, = curs.fetchone()
curs.execute("SELECT username FROM user WHERE userid = ?", [userid,])
username, = curs.fetchone()
filename = open(username + ".csv", 'w')
filename.write("userid,topic_id,topic_name,subtopic_id,subtopic_name,passage_id,passage_name,docno,offset_start,offset_end,grade\n")
curs.execute("SELECT topic_id,topic_name FROM topic WHERE userid=?", [userid,])
topics = curs.fetchall()
for topic_id,topic_name in topics:
	curs.execute("SELECT subtopic_id, subtopic_name FROM subtopic WHERE topic_id = ?", [topic_id, ])
	tmp = curs.fetchall()
	for item in tmp:
		curs.execute("SELECT * FROM passage WHERE subtopic_id =?", [item[0]])
		for passage in curs.fetchall():
			filename.write(','.join([str(userid),str(topic_id),topic_name,str(item[0]),str(item[1]),str(passage[0]),str(passage[1]).replace(',','').replace('\n',''),str(passage[2]),str(passage[3]),str(passage[4]),str(passage[5])])+'\n')
filename.close()
print "Content-type: text/plain"
print 
print username+".csv"

