#!/usr/bin/python

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

def getDomainContent(last_domain_id):
	domain_content = ""
	curs.execute("SELECT * FROM domain");
	for item in curs.fetchall():
		if item[0] != last_domain_id:
			domain_content += '<option value=' + item[1].encode('UTF-8') + '>' + item[1].encode('UTF-8') + '</option>\n'
		else:
			domain_content += '<option value=' + item[1].encode('UTF-8') + ' selected="selected"' +'>' + item[1].encode('UTF-8') + '</option>\n'
	return domain_content

def fetch(current_user):
	topic_content = ''
	curs.execute("SELECT userid, last_domain_id FROM user WHERE username = ?", [current_user,]) #unicode??
	userid, last_domain_id = curs.fetchone()
	curs.execute("SELECT last_topic_id FROM last_topic WHERE userid = ? AND domain_id = ?",[userid, last_domain_id])
	result_last_topic = curs.fetchone()
	curs.execute("SELECT topic_id, topic_name FROM topic WHERE userid = ? AND domain_id = ?", [userid, last_domain_id])
	result_topics = curs.fetchall()
	if result_topics:
		if result_last_topic:
			last_topic_id = result_last_topic[0]
		else:
			last_topic_id = result_topics[0][0]
	for item in result_topics:
		if item[0] != last_topic_id:
			topic_content += '<option value=' + item[1].encode('UTF-8') + '>' + item[1].encode('UTF-8') + '</option>\n'
		else:
			topic_content += '<option value=' + item[1].encode('UTF-8') + ' selected="selected"' +'>' + item[1].encode('UTF-8') + '</option>\n'
	domain_content = getDomainContent(last_domain_id)
	
	curs.execute("SELECT domain_url FROM domain WHERE domain_id = ?", [last_domain_id,])
	
	domain_url, = curs.fetchone()
	
	sidecontent = ''
	
	if result_topics:
		curs.execute("SELECT subtopic_name, scroll_position FROM subtopic WHERE topic_id = ? ORDER BY subtopic_id DESC", [last_topic_id,])
		subtopics = curs.fetchall()
		for item in subtopics:
			sidecontent += '<div class="droppable" ondragover="return false" ondrop="annotate(event)">\n'
			sidecontent += '<span style="display:none">%s</span>\n'% item[1]
			sidecontent += '<h2>' + item[0] + '</h2>\n'
			sidecontent += '<input class="editbox" style="display: none;">\n' 
			sidecontent += '<div class="edit">edit</div>\n'
			sidecontent += '<div class="confirmEdit" style="display: none;">confirm</div>\n'
			sidecontent += '<div style="clear:both; padding-bottom:10px;"></div>'
			curs.execute("SELECT subtopic_id FROM subtopic WHERE subtopic_name= ? AND topic_id = ?", [item[0],last_topic_id])
			tmpid, = curs.fetchone()
			curs.execute("SELECT passage_id, passage_name, docno, grade FROM passage WHERE subtopic_id = ? ORDER BY passage_id ASC", [tmpid,])
			for passage in curs.fetchall():
				sidecontent += '<div class="annotated passage" style="display: block;">\n'
				sidecontent += '<p>' + passage[1] + '</p>\n'
				sidecontent += '<div class="passage_id" style="display:none">' + str(passage[0]) + '</div>\n'
				sidecontent += '''<div class="docinfo" onclick="goback('%s')">''' % passage[2]
				sidecontent += 'FROM DOC: <a>' + passage[2]
				sidecontent += '</a></div>\n'
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
		curs.execute("SELECT state, fileId FROM last_topic WHERE last_topic_id = ?", [last_topic_id,])
		state, fileId = curs.fetchone()
		sidecontent += "<div id='state' style='display:none;'>" + state + "</div>"
		sidecontent += "<div id='fileId' style='display:none;'>" + fileId + "</div>"
	return (domain_content, domain_url, topic_content, sidecontent)

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
	domain = form.getvalue('domain', None)
	topic = form.getvalue('topic', None)
	print 'Content-type: text/html'
	print
	fileContent = open("./index.html",'r')
	if domain:
		curs.execute("SELECT domain_id FROM domain WHERE domain_name = ?", [domain,])
		new_domain_id,  = curs.fetchone()
		curs.execute("UPDATE user SET last_domain_id = ? WHERE username = ?", [new_domain_id, cookie['username']]) #[] or ()??
		conn.commit()
	else:
		if topic:
			curs.execute("SELECT last_domain_id FROM user WHERE username = ?", [cookie['username'],])
			last_domain_id, = curs.fetchone()
			curs.execute("SELECT topic_id FROM topic WHERE topic_name = ?", [topic,])
			new_topic_id, = curs.fetchone()
			curs.execute("SELECT userid FROM user WHERE username = ?", [cookie['username'],])
			userid, = curs.fetchone()
			curs.execute("UPDATE last_topic SET last_topic_id = ? WHERE userid = ? AND domain_id = ?", [new_topic_id, userid, last_domain_id] )
			conn.commit()
	
	domain_content, domain_url, topic_content, sidecontent = fetch(cookie['username'])
	print (fileContent.read()%(domain_content, cookie['username'], domain_url, topic_content, sidecontent)).encode("UTF-8")
		
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
		print (fileContent.read()%'').encode("UTF-8")
	else: 
		if (username, password) in users.items():
			fileContent = open("./index.html",'r')	
			expires = time.time() + 24 * 3600
			domain_content, domain_url, topic_content, sidecontent= fetch(username)
			
			print 'Set-Cookie:username=%s;Expires=%s'%(username,time.strftime("%a, %d-%b-%Y %T GMT", time.gmtime(expires)))	
			print 'Content-type: text/html'
			print
			print (fileContent.read()%(domain_content, username, domain_url, topic_content, sidecontent)).encode("UTF-8")
		else:
			fileContent = open("./login.html",'r')	
			print 'Content-type: text/html'
			print
			print (fileContent.read()%"invalid username or password").encode("UTF-8")
conn.close()
