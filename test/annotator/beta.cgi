#!/usr/bin/env python

import cgi, cgitb, time, sqlite3
from os import environ

#users = {'admin':'admin', 'test':'test', 'infosense':'infosense'}
users = {}
conn = sqlite3.connect('test.db')
curs = conn.cursor()
curs.execute("SELECT username, password FROM user")
for item in curs.fetchall():
	(username, password) = item
	users[username.encode('UTF-8')] = password.encode('UTF-8')

cookie = {}

#print 'Conten-type: text/html'
#print
#print '0'

def fetch(current_user):
	vcontent = ''
	curs.execute("SELECT userid, lasttopicid FROM user WHERE username = ?", [current_user,]) #unicode??
	(userid, last) = curs.fetchone()
	curs.execute("SELECT topic_id, topic_name FROM topic WHERE userid = ?", [userid,])
	for item in curs.fetchall():
		if item[0] != last:
			vcontent += '<option value=' + item[1].encode('UTF-8') + '>' + item[1].encode('UTF-8') + '</option>\n'
		else:
			vcontent += '<option value=' + item[1].encode('UTF-8') + ' selected="selected"' +'>' + item[1].encode('UTF-8') + '</option>\n'
	curs.execute("SELECT subtopic_name FROM subtopic WHERE topic_id = ?", [last,])
	sidecontent = ''
	subtopics = curs.fetchall()
	for item in subtopics:
		sidecontent += '<div class="droppable" ondragover="return false" ondrop="annotate(event)">\n'
		sidecontent += '<h2>' + item[0] + '</h2>\n'
		sidecontent += '<input class="editbox" style="display: none;">\n' 
		sidecontent += '<div class="edit">edit</div>\n'
		sidecontent += '<div class="confirmEdit" style="display: none;">confirm</div>\n'
		sidecontent += '<div style="clear:both; padding-bottom:10px;"></div>'
		curs.execute("SELECT subtopic_id FROM subtopic WHERE subtopic_name= ?", [item[0],])
		tmpid, = curs.fetchone()
		curs.execute("SELECT passage_id, passage_name, docno, grade FROM passage WHERE subtopic_id = ? ORDER BY passage_id ASC", [tmpid,])
		tmp = curs.fetchall()
		for passage in tmp:
			sidecontent += '<div class="annotating" style="display: block;">\n'
			sidecontent += passage[1]
			sidecontent += '<div class="docinfo">'
			sidecontent += 'FROM DOC: ' + passage[2]
			sidecontent += '</div>\n'
			sidecontent += '<form>\n'
			for i in range(1,5):
				if i == passage[3]:
					sidecontent += str(i) + '<input type="radio" class="eval" name="score" value=%d checked>\n'%i
				else:
					sidecontent += str(i) + '<input type="radio" class="eval" name="score" value=%d>\n'%i
			sidecontent += '<img src="./img/trash.png" class="remove"/>'
			sidecontent += '</form>\n'
			sidecontent += '</div>\n'
		sidecontent += '</div>'
	return (vcontent, sidecontent)

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

if 'HTTP_COOKIE' in environ and 'username' in cookie and cookie['username'] in users:
#if True:
#	cookie = {}
#	cookie['username'] = 'admin'
#	select = 'topic_beta'
	select = form.getvalue('select', None)
	print 'Content-type: text/html'
	print
	fileContent = open("./index.html",'r')
	if select:
		curs.execute("SELECT topic_id FROM topic WHERE topic_name = ?", (select,))
		lasttopicid,  = curs.fetchone()
		curs.execute("UPDATE user SET lasttopicid = ? WHERE username = ?", [lasttopicid, cookie['username']]) #[] or ()??
		conn.commit()
	vcontent, sidecontent = fetch(cookie['username']) 
	print fileContent.read()%(vcontent, cookie['username'], sidecontent)
		
else:
	#print 'Content-type: text/html'
	#print 
	#print '2'
	username = form.getvalue('username', None)
	password = form.getvalue('password', None)
	if (username == None) and (password == None):
		fileContent = open("./login.html",'r')
		print 'Content-type: text/html'
		print
		print fileContent.read()%''
	else: 
		if (username, password) in users.items():
			fileContent = open("./index.html",'r')	
			expires = time.time() + 24 * 3600
			vcontent, sidecontent= fetch(username)
			print 'Set-Cookie:username=%s;Expires=%s'%(username,time.strftime("%a, %d-%b-%Y %T GMT", time.gmtime(expires)))	
			print 'Content-type: text/html'
			print
			print fileContent.read()%(vcontent, username, sidecontent)
		else:
			fileContent = open("./login.html",'r')	
			print 'Content-type: text/html'
			print
			print fileContent.read()%"invalid username or password"
conn.close()
