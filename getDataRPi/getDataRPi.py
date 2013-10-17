#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3 as lite
import datetime
import time
import sys
import subprocess


def eth0TxRx():
    ''''''

    p = subprocess.Popen("/sbin/ifconfig eth0 | grep RX\ bytes",
        stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    output = output.strip()
    output = output.replace('RX bytes:', '').replace('TX bytes:', '')
    fields = output.split(' ')
    rx = str(int(fields[0]) / 1024 / 1024)
    tx = str(int(fields[4]) / 1024 / 1024)
    total = str((int(fields[0]) / 1024 / 1024) +
        (int(fields[4]) / 1024 / 1024))
    return rx, tx, total


def temperatura():
    ''''''
    p = subprocess.Popen("cat /sys/class/thermal/thermal_zone0/temp",
        stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    t = float(output) / 1000
    return t

con = None
con = lite.connect('./datosRPi.db')
cur = con.cursor()

#cur.execute('DROP TABLE IF EXISTS temperaturas')
#cur.fetchone()
########### Create Table
try:
    sql = 'CREATE TABLE temperaturas (' + \
        'Id INTEGER PRIMARY KEY AUTOINCREMENT, ' + \
        'temp NUMERIC, rx NUMERIC, tx NUMERIC, total NUMERIC, ' + \
        'fecha DATETIME)'
    cur.execute(sql)
    cur.fetchone()
except:
    print("La tabla ya existe...")

x = 0
while True:
    t = temperatura()
    rx, tx, total = eth0TxRx()
    tiempoAhora = datetime.datetime.now()
    fechaHora = tiempoAhora.strftime("%y-%m-%d %H:%M:%S")
    sql = ("INSERT INTO temperaturas (temp, rx, tx, total, " +
        "fecha) VALUES (%.2f, %s, %s, %s, '%s')" %
        (t, rx, tx, total, fechaHora))
    cur.execute(sql)
    con.commit()
    x += 1
    time.sleep(60)
