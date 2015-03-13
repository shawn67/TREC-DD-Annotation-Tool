#!/usr/bin/env python

import cgi, sqlite3, json

conn = sqlite3.connect("test.db")
curs = conn.cursor()

form = cgi.FieldStorage()
json_string = form.getvalue('data', '')
#fileHandler = open("storage.txt", 'w')
#fileHandler.write(json_string)
#fileHandler.close()

data = json.loads(json_string)
curs.execute("SELECT topic_id FROM topic WHERE topic_name = ?", [data[u'topic_name'],])
topic_id, = curs.fetchone()
curs.execute("UPDATE last_topic SET state = ?, fileId = ? WHERE last_topic_id = ?", [data[u'state'], data[u'browseposition'], topic_id])
for i in data[u'delete_passage']:
	curs.execute("DELETE FROM passage WHERE passage_id = ?", [i, ])
for subtopic in data[u'subtopics']:
	curs.execute("SELECT subtopic_id FROM subtopic WHERE subtopic_name = ? AND topic_id = ?", [subtopic[u'subtopic_name'], topic_id])
	result = curs.fetchone()
	if not result:
		curs.execute("INSERT INTO subtopic VALUES(NULL,?,?,NULL)", [subtopic[u'subtopic_name'], topic_id])
		curs.execute("SELECT subtopic_id FROM subtopic WHERE subtopic_name = ? AND topic_id = ?", [subtopic[u'subtopic_name'],topic_id])
		subtopic_id, = curs.fetchone()
	else:
		subtopic_id, = result
	curs.execute("UPDATE subtopic SET scroll_position = ? WHERE subtopic_id = ?", [subtopic[u'position'], subtopic_id])
	for passage in subtopic[u'passages']:
		if not u'passage_id' in passage:
			if not u'grade' in passage: passage[u'grade'] = 5
			curs.execute("INSERT INTO passage VALUES(NULL,?,?,?,?,?,?)", [passage[u'passage_name'], passage[u'url'], passage[u'offset_start'], passage[u'offset_end'], passage[u'grade'], subtopic_id])
		
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
