#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

conn = sqlite3.connect('test.db')
cur = conn.cursor()

cur.execute("CREATE TABLE user(userid INTEGER PRIMARY KEY, username TEXT NOT NULL, password TEXT NOT NULL, lasttopicid INTEGER)")
insert = "INSERT INTO user VALUES(?, ?, ?, ?)"
cur.execute(insert, [1,'admin','admin',1])
cur.execute(insert, [2,'test', 'test',4])
cur.execute(insert, [3,'infosense', 'senseinfo',7])

cur.execute("CREATE TABLE topic(topic_id INTEGER PRIMARY KEY, topic_name TEXT, userid INTEGER)")
insert = "INSERT INTO topic VALUES(?, ?, ?)"
cur.execute(insert, [1, 'topic_alpha', 1])
cur.execute(insert, [2, 'topic_beta', 1])
cur.execute(insert, [3, 'topic_gamma', 1])
cur.execute(insert, [4, 'topic_xx', 2])
cur.execute(insert, [5, 'topic_yy', 2])
cur.execute(insert, [6, 'topic_zz', 2])
cur.execute(insert, [7, 'topic_pp', 3])
cur.execute(insert, [8, 'topic_qq', 3])
cur.execute(insert, [9, 'topic_ww', 3])

cur.execute("CREATE TABLE subtopic(subtopic_id INTEGER PRIMARY KEY, subtopic_name TEXT, topic_id)")

cur.execute("CREATE TABLE passage(passage_id INTEGER PRIMARY KEY, passage_name TEXT, docno TEXT, offset_start INTEGER, offset_end INTEGER, grade INTEGER, subtopic_id INTEGER)")

insert = "INSERT INTO subtopic VALUES(?, ?, ?)"
cur.execute(insert, [1, 'subtopic_alpha', 1])
cur.execute(insert, [2, 'subtopic_beta', 1])
cur.execute(insert, [3, 'subtopic_xx', 2])
cur.execute(insert, [4, 'subtopic_yy', 2])
cur.execute(insert, [5, 'subtopic_pp', 3])
cur.execute(insert, [6, 'subtopic_qq', 3])
cur.execute(insert, [7, 'subtopic_ww', 3])

insert = "INSERT INTO passage VALUES(?,?,?,?,?,?,?)"

cur.execute(insert, [1, 'however, bats are considered to be the most likely candidate species.[35] Three types of fruit bats', './ebola/5.txt', 0 ,0 , 3, 1]) 
cur.execute(insert, [2, ' a virion attaching to specific cell-surface receptors such as C-type lectins, DC-SIGN, or integrins, which is followed ', './ebola/6.txt', 0 ,0 , 2, 1]) 
cur.execute(insert, [3, ' including liver cells, fibroblasts, and adrenal gland cells.[69] Viral replication triggers the release of high levels of ', './ebola/7.txt', 0 ,0 , 4, 1]) 

conn.commit()
conn.close()
