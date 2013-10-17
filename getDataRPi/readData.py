#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3 as lite

con = None

con = lite.connect('./datosRPi.db')

cur = con.cursor()

sql = ("SELECT * FROM temperaturas")
cur.execute(sql)
data = cur.fetchall()

print(data)