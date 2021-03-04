#! /usr/bin/env
# -*- coding: utf-8 -*-

import sqlite3

conn = sqlite3.connect(r'D:/new.db')
cur = conn.cursor()

cur.execute("INSERT INTO new_table (user, password) VALUES ('petr', '753');")
conn.commit()


cur.execute("SELECT *  FROM new_table")

j = 0
while j < cur.arraysize:
    sel = cur.fetchmany(1)
    j += 1
    print(sel)
