from flask import Flask
from flask import render_template
import sqlite3 as lite

app = Flask(__name__, static_folder='/var/www/flask/static')


@app.route('/graf')
@app.route('/<name>')
def graf(name=None):
    '''
    '''
    con = None
    con = lite.connect('/home/pi/getDataRPi/datosRPi.db')
    cur = con.cursor()
    sql = ("SELECT temp FROM temperaturas")
    cur.execute(sql)
    data = cur.fetchall()
    dataList = []
    for row in data:
        dictData = {}
        dictData = {'fecha': row[2], 'temp': row[1]}
        dataList.append(dictData)

    return render_template('googlegraftemp.html', datos=dataList)

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')



