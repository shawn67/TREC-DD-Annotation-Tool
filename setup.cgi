#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

conn = sqlite3.connect('test.db')
cur = conn.cursor()

class dbHandler:

    def __init__(self, dbname):
        this.conn = sqlite3.connect(dbname)
        this.cur = conn.cursor()

    def createTables(self):
        


cur.execute("CREATE TABLE user(userid INTEGER PRIMARY KEY, username TEXT NOT NULL, password TEXT NOT NULL, last_domain_id INTEGER)")

cur.execute("CREATE TABLE domain(domain_id INTEGER PRIMARY KEY, domain_name TEXT, domain_url TEXT)")

cur.execute("CREATE TABLE last_topic(userid INTEGER, domain_id INTEGER, last_topic_id INTEGER, state TEXT, fileID TEXT, PRIMARY KEY(userid, domain_id))")

cur.execute("CREATE TABLE topic(topic_id INTEGER PRIMARY KEY, topic_name TEXT, userid INTEGER, domain_id INTEGER)")

cur.execute("CREATE TABLE subtopic(subtopic_id INTEGER PRIMARY KEY, subtopic_name TEXT, topic_id INTEGER, scroll_position INTEGER)")

cur.execute("CREATE TABLE passage(passage_id INTEGER PRIMARY KEY, passage_name TEXT, docno TEXT, offset_start INTEGER, offset_end INTEGER, grade INTEGER, subtopic_id INTEGER)")

insert = "INSERT INTO domain VALUES(?, ?, ?)"
cur.execute(insert, [1, 'Illicit_Goods', 'http://infosense.cs.georgetown.edu/trec_dd/illicit_goods/lemur.cgi'])
cur.execute(insert, [2, 'Ebola', 'notready.html'])
cur.execute(insert, [3, 'Local_Politics', 'notready.html'])

insert = "INSERT INTO topic VALUES(?, ?, ?, ?)"
cur.execute(insert, [1, 'Illicit_Goods_topic1', 1, 1])
cur.execute(insert, [2, 'Ebola_topic1', 1, 2])
cur.execute(insert, [3, 'Local_Politics_topic1', 1, 3])
cur.execute(insert, [4, 'ig_topic1', 2, 1])
cur.execute(insert, [5, 'eb_topic1', 2, 2])
cur.execute(insert, [6, 'lp_topic1', 2, 3])
cur.execute(insert, [7, 'ig_test1', 3, 1])
cur.execute(insert, [8, 'eb_test1', 3, 2])
cur.execute(insert, [9, 'lp_test1', 3, 3])

insert = "INSERT INTO last_topic VALUES(?, ?, ?, ?, ?)"
cur.execute(insert, [1, 1, 1, 1, 5])
cur.execute(insert, [1, 2, 2, 1, 5])
cur.execute(insert, [1, 3, 3, 1, 5])
cur.execute(insert, [2, 1, 4, 1, 5])
cur.execute(insert, [2, 2, 5, 1, 5])
cur.execute(insert, [2, 3, 6, 1, 5])
cur.execute(insert, [3, 1, 7, 1, 5])
cur.execute(insert, [3, 2, 8, 1, 5])
cur.execute(insert, [3, 3, 9, 1, 5])

'''
cur.execute(insert, [4, 'topic_xx', 2])
cur.execute(insert, [5, 'topic_yy', 2])
cur.execute(insert, [6, 'topic_zz', 2])
cur.execute(insert, [7, 'topic_pp', 3])
cur.execute(insert, [8, 'topic_qq', 3])
cur.execute(insert, [9, 'topic_ww', 3])
'''

'''
insert = "INSERT INTO subtopic VALUES(?, ?, ?, ?)"
cur.execute(insert, [1, 'subtopic_alpha', 1, 0])
cur.execute(insert, [2, 'subtopic_beta', 1, 0])
cur.execute(insert, [3, 'subtopic_xx', 2, 0])
cur.execute(insert, [4, 'subtopic_yy', 2, 0])
cur.execute(insert, [5, 'subtopic_pp', 3, 0])
cur.execute(insert, [6, 'subtopic_qq', 3, 0])

insert = "INSERT INTO passage VALUES(?,?,?,?,?,?,?)"

cur.execute(insert, [1, 'however, bats are considered to be the most likely candidate species.[35] Three types of fruit bats', './ebola/5.txt', 0 ,0 , 3, 1]) 
cur.execute(insert, [2, ' a virion attaching to specific cell-surface receptors such as C-type lectins, DC-SIGN, or integrins, which is followed ', './ebola/6.txt', 0 ,0 , 2, 1]) 
cur.execute(insert, [3, ' including liver cells, fibroblasts, and adrenal gland cells.[69] Viral replication triggers the release of high levels of ', './ebola/7.txt', 0 ,0 , 4, 1]) 
'''

conn.commit()
conn.close()
