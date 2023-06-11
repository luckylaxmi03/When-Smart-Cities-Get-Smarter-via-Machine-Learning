from flask import Flask, render_template, request, session, flash
import mysql.connector as mysql
app = Flask(__name__)



mydb = mysql.connect(
  host="localhost",
  user="root",
  password="root",
  database="vtpai08_2021"
)

app.secret_key = 'your secret key'

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/manager')
def manager():
    return render_template('manager.html')

@app.route('/robot')
def robot():
    return render_template('robot.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('index.html')

@app.route('/alogin', methods = ['POST', 'GET'])
def alogin():
    if request.method == 'POST':
        uid = request.form['uid']
        pwd = request.form['pwd']
        if uid == 'admin' and pwd == 'admin':
            return render_template('ahome.html')
        else:
            return render_template('admin.html')

@app.route('/mlogin', methods = ['POST', 'GET'])
def mlogin():
    if request.method == 'POST':
        uid = request.form['uid']
        pwd = request.form['pwd']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM manager WHERE email = %s AND password = %s', (uid, pwd))
        account = cursor.fetchone()
        if account:
            session['uid'] = request.form['uid']
            session['name'] = account[0]
            return render_template('mhome.html', result = account[0])
        else:
            return render_template('manager.html')

@app.route('/rlogin', methods = ['POST', 'GET'])
def rlogin():
    if request.method == 'POST':
        uid = request.form['uid']
        pwd = request.form['pwd']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM robot WHERE rid = %s AND password = %s', (uid, pwd))
        account = cursor.fetchone()
        if account:
            session['uid'] = request.form['uid']
            session['name'] = account[0]
            session['man'] = account[4]
            return render_template('rhome.html', result = account[0])
        else:
            return render_template('robot.html')
        
@app.route('/ahome')
def ahome():
    return render_template('ahome.html')

@app.route('/addmanager')
def addmanager():
    return render_template('addmanager.html')

@app.route('/addman', methods = ['POST', 'GET'])
def addman():
    if request.method == 'POST':
        name = request.form['name']
        uid = request.form['uid']
        pwd = request.form['pwd']
        mob = request.form['mob']
        dep = request.form['dep']
        loc = request.form['loc']
        var = (name, uid, pwd, mob, dep, loc)
        cursor = mydb.cursor()
        cursor.execute('insert into manager values (%s, %s, %s, %s, %s, %s)', var)
        mydb.commit()
        if cursor.rowcount == 1:
            flash("Manager Added Successfuly") 
            return render_template('addmanager.html')
        else:
            flash("Invalid Details, Manager not Added") 
            return render_template('addmanager.html')

@app.route('/amanager')
def amanager():
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM manager')
    data = cursor.fetchall()
    return render_template('amanager.html', result = data)

@app.route('/addrobot')
def addrobot():
    return render_template('addrobot.html')

@app.route('/addrobo', methods = ['POST', 'GET'])
def addrobo():
    if request.method == 'POST':
        name = request.form['name']
        uid = request.form['uid']
        pwd = request.form['pwd']
        dep = request.form['dep']
        loc = request.form['man']
        var = (name, uid, pwd, dep, loc)
        cursor = mydb.cursor()
        cursor.execute('insert into robot values (%s, %s, %s, %s, %s)', var)
        mydb.commit()
        if cursor.rowcount == 1:
            flash("Robot Added Successfuly") 
            return render_template('addrobot.html')
        else:
            flash("Invalid Details, Robot not Added")
            return render_template('addrobot.html')
            
@app.route('/arobot')
def arobot():
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM robot')
    data = cursor.fetchall()
    return render_template('arobot.html', result = data)

@app.route('/aprod')
def aprod():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM product")
    data = cursor.fetchall()
    return render_template('aprod.html', result = data)

@app.route('/mhome')
def mhome():
    uid = session['name']
    return render_template('mhome.html', result = uid)

@app.route('/mrobot')
def mrobot():
    uid = session['uid']
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM robot where manager='"+uid+"'")
    data = cursor.fetchall()
    return render_template('mrobot.html', result = data)
    
@app.route('/mprod')
def mprod():
    uid = session['uid']
    cursor = mydb.cursor()
    cursor.execute("SELECT rid FROM robot where manager='"+uid+"'")
    data = cursor.fetchall()
    return render_template('mprod.html', result = data)

@app.route('/send', methods = ['POST', 'GET'])
def send():
    uid = session['uid']
    if request.method == 'POST':
        mat = request.form['mat']
        mam = request.form['msm']
        spc = request.form['spc']
        part = request.form['part']
        robot = request.form['rid']
        var = (mat, mam, spc, part, robot, uid, 'pending')
        cursor = mydb.cursor()
        cursor.execute('insert into parts values(0, %s, %s, %s, %s, %s, %s, %s)', var)
        mydb.commit()
        if cursor.rowcount == 1:
            flash("Part Details Sent Successfuly") 
            cursor.execute("SELECT rid FROM robot where manager='"+uid+"'")
            data = cursor.fetchall()
            return render_template('mprod.html', result = data)
        else:
            flash("Invalid Details, Part Details not Sent")
            cursor.execute("SELECT rid FROM robot where manager='"+uid+"'")
            data = cursor.fetchall()
            return render_template('mprod.html', result = data)
        
@app.route('/mpart')
def mpart():
    uid = session['uid']
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM parts where manager='"+uid+"'")
    data = cursor.fetchall()
    return render_template('mpart.html', result = data)
    
@app.route('/mrev')
def mrev():
    uid = session['uid']
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM product where manager='"+uid+"' and status='pending'")
    data = cursor.fetchall()
    return render_template('mrev.html', result = data)

@app.route('/rhome')
def rhome():
    name = session['name']
    return render_template('rhome.html', result = name)

@app.route('/rparts')
def rparts():
    uid = session['uid']
    cursor = mydb.cursor()
    cursor.execute("select * from parts where robot='"+uid+"' and status='pending'")
    data = cursor.fetchall()
    return render_template('rparts.html', result = data)

@app.route('/rprod')
def rprod():
    uid = session['uid']
    cursor = mydb.cursor()
    cursor.execute("select part from parts where robot='"+uid+"' and status='Approved'")
    data = cursor.fetchall()
    return render_template('rprod.html', result = data)

@app.route('/rrev/<string:id>')
def rrev(id):
    uid = session['uid']
    cursor = mydb.cursor()
    cursor.execute("select * from parts where id="+id)
    data = cursor.fetchone()
    cursor.execute("select * from material where part='"+data[4]+"'")
    d = cursor.fetchone()
    if d[0] == data[1] and d[1] == data[2] and d[2] == data[3]:
        cursor.execute("update parts set status='Approved' where id="+id)
        mydb.commit()
        if cursor.rowcount == 1:
            cursor.execute("select * from parts where robot='"+uid+"' and status='pending'")
            data = cursor.fetchall()
            return render_template('rparts.html', result = data)
        else:
            cursor.execute("select * from parts where robot='"+uid+"' and status='pending'")
            data = cursor.fetchall()
            return render_template('rparts.html', result = data)
    else:
        cursor.execute("update parts set status='Rejected' where id="+id)
        mydb.commit()
        if cursor.rowcount == 1:
            cursor.execute("select * from parts where robot='"+uid+"' and status='pending'")
            data = cursor.fetchall()
            return render_template('rparts.html', result = data)
        else:
            cursor.execute("select * from parts where robot='"+uid+"' and status='pending'")
            data = cursor.fetchall()
            return render_template('rparts.html', result = data)

@app.route('/rsent', methods = ['POST', 'GET'])
def rsent():
    uid = session['uid']
    man = session['man']
    if request.method == 'POST':
        part = request.form['part']
        da = request.form['da']
        var = (man, uid, part, da, 'pending')
        cursor = mydb.cursor()
        cursor.execute('insert into product values(0, %s, %s, %s, %s, %s)', var)
        mydb.commit()
        if cursor.rowcount == 1:
            flash("Final Product Sent Successfuly")
            cursor.execute("select part from parts where robot='"+uid+"' and status='Approved'")
            data = cursor.fetchall()
            return render_template('rprod.html', result = data)
        else:
            flash("Final Product Details not Sent")
            cursor.execute("select part from parts where robot='"+uid+"' and status='Approved'")
            data = cursor.fetchall()
            return render_template('rprod.html', result = data)

@app.route('/mapprove/<string:id>')
def mapprove(id):
    uid = session['uid']
    cursor = mydb.cursor()
    cursor.execute('update product set status="Approved" where id='+id)
    mydb.commit()
    if cursor.rowcount == 1:
        cursor.execute("SELECT * FROM product where manager='"+uid+"' and status='pending'")
        data = cursor.fetchall()
        return render_template('mrev.html', result = data)
    else:
        cursor.execute("SELECT * FROM product where manager='"+uid+"' and status='pending'")
        data = cursor.fetchall()
        return render_template('mrev.html', result = data)
    
@app.route('/mreject/<string:id>')
def mreject(id):
    uid = session['uid']
    cursor = mydb.cursor()
    cursor.execute('update product set status="Approved" where id='+id)
    mydb.commit()
    if cursor.rowcount == 1:
        cursor.execute("SELECT * FROM product where manager='"+uid+"' and status='pending'")
        data = cursor.fetchall()
        return render_template('mrev.html', result = data)
    else:
        cursor.execute("SELECT * FROM product where manager='"+uid+"' and status='pending'")
        data = cursor.fetchall()
        return render_template('mrev.html', result = data)

if __name__ == '__main__':
   app.run()