from flask import Flask
from flask import render_template
import math
import subprocess
import sqlite3 as lite
app = Flask(__name__, static_folder='/var/www/flask/static')


def temperature():
    ''''''
    p = subprocess.Popen("cat /sys/class/thermal/thermal_zone0/temp",
        stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    t = float(output) / 1000
    return "%.2f" % t


def disk():
    ''''''
    p = subprocess.Popen("lsblk --pairs",
        stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    lines = output.replace('"', '').split('\n')
    lista = []
    for l in lines:
        fields = l.split(" ")
        dict1 = {}
        for f in fields:
            if len(f.strip()) >= 1:
                d = f.split("=")
                dict1[d[0]] = d[1]
                print(dict1)
        lista.append(dict1)
    return lista


def storage():
    ''''''
    p = subprocess.Popen('df -T | grep -vE "tmpfs|rootfs|Filesystem"',
        stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    lines = output.replace('  ', ' ').split('\n')
    lines.pop(0)
    print(lines)
    lista = []
    for l in lines:
        fields = l.split(" ")
        lista1 = []
        for f in fields:
            lista1.append(f)
        lista.append([x for x in lista1 if x != ''])
    return lista


def memoria():
    ''''''
    p = subprocess.Popen('free -ht',
        stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    lines = output.replace('  ', ' ').split('\n')
    lines.pop(0)
    print(lines)
    lista = []
    for l in lines:
        fields = l.split(" ")
        lista1 = []
        for f in fields:
            lista1.append(f)
        lista.append([x for x in lista1 if x != ''])
    return lista


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


def upTime():
    ''''''
    uptime = open('/proc/uptime', 'r').readline().split(" ")
    segundos = float(uptime[0])
    y = math.floor(segundos / 60 / 60 / 24 / 365)
    d = math.floor(segundos / 60 / 60 / 24) % 365
    h = math.floor((segundos / 3600) % 24)
    m = math.floor((segundos / 60) % 60)
    s = segundos % 60
    return y, d, h, m, s


def frequency():
    ''''''
    cpuCurFreq = open(
        '/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq',
        'r').readline()
    cpuMinFreq = open(
        '/sys/devices/system/cpu/cpu0/cpufreq/scaling_min_freq',
        'r').readline()
    cpuMaxFreq = open(
        '/sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq',
        'r').readline()
    cpuFreqGovernor = open(
        '/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor',
        'r').readline()
    actual = str(int(cpuCurFreq) / 1000)
    minima = str(int(cpuMinFreq) / 1000)
    maxima = str(int(cpuMaxFreq) / 1000)
    governor = str(cpuFreqGovernor).strip()
    return actual, minima, maxima, governor


@app.route('/')
@app.route('/<name>')
def hello(name=None):
    '''
    '''
    y, d, h, m, s = upTime()
    actual, minima, maxima, governor = frequency()
    rx, tx, total = eth0TxRx()
    posts = disk()
    store = storage()
    temper = temperature()
    memory = memoria()
    return render_template('hello.html', anio=('%02.0f' % y),
        dias=('%02.0f' % d), horas=('%02.0f' % h),
        minutos=('%02.0f' % m), segundos=('%02.0f' % s),
        actual=actual, minima=minima, maxima=maxima, governor=governor,
        rx=rx, tx=tx, total=total, posts=posts, storage=store, temper=temper,
        memory=memory)


@app.route('/graf')
def graf(name=None):
    '''
    '''
    con = None
    con = lite.connect('/home/pi/getDataRPi/datosRPi.db')
    cur = con.cursor()
    sql = ("SELECT * FROM temperaturas")
    cur.execute(sql)
    data = cur.fetchall()
    dataList = []
    for row in data:
        dictData = {}
        dictData = {'fecha': row[2], 'temp': row[1]}
        dataList.append(dictData)

    return render_template('googlegraf.html', datos=dataList)


@app.route('/crew')
def crew(name=None):
    ''''''
    return render_template('aboutme.html')

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')