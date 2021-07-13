from flask import (
    Flask,
    render_template, 
    request,
    session,
    redirect,
    flash,
    url_for,
    jsonify
)
import sqlite3
import datetime
# from contain_uncontain import contain,uncontain


app = Flask(__name__)
app.secret_key = 'ASDFGHJKLQWERTYUIOPZXCVBNMMBVCXZPOIUYTREWQLKJHGFDSA)(*&^%$#@!12#$%^&*900'

@app.route('/' , methods = ['GET', 'POST'])
def login():
   if request.method == 'POST':
       username = request.form['username'] 
       password = request.form['password']
       with sqlite3.connect('data.db') as conn:
           cursor = conn.execute('SELECT * from users where username=? and password=?',(username,password,))
           user = cursor.fetchone()
       if user:
           session['username'] = user[0]
           return redirect(url_for('devices')) 
       else:
           flash("User does not Exists")
           return redirect(url_for('login'))
   if 'username' in session:
        return redirect(url_for('devices')) 
   return render_template('login.html')


@app.route('/register', methods =['GET','POST'])
def register():
   if request.method == 'POST':
       username = request.form['username']
       password = request.form['password']
       first_name = request.form['first_name']
       last_name = request.form['last_name']
       date = datetime.datetime.now()
       createDate = date.strftime('%d')+'/'+date.strftime('%m')
       lastLoggedIn = createDate
       with sqlite3.connect('data.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT into users values(?,?,?,?,?,?)",(username,password,first_name,last_name,createDate,lastLoggedIn))
            conn.commit()
            session['username'] = username
            flash("Successfully Registered")
            return redirect(url_for('devices')) 
   return render_template('register.html')


@app.route('/devices')
def devices():
    if 'username' in session:
        with sqlite3.connect('data.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * from devices')
            devices = cursor.fetchall()
        return render_template('devices.html', devices=devices)
    else:
        return redirect(url_for('login'))
    
@app.route('/trustDevice', methods=['POST'])
def trustDevice():
    if request.method == 'POST':
        ip = request.form['ip']
        value = 1
        with sqlite3.connect('data.db') as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE devices set trusted=? where ip=?',(value,ip,))
            conn.commit()
        flash("Device trusted successfully")
        return redirect(url_for('devices'))
    
@app.route('/incidents')
def incidents():
    if 'username' in session:
        with sqlite3.connect('data.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * from incident')
            incidents = cursor.fetchall()
        return render_template('incidents.html', incidents=incidents)
    else:
        return redirect(url_for('login'))
    
@app.route("/incident/<int:incident_id>")
def incident(incident_id):
    if 'username' in session:
        with sqlite3.connect('data.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * from incident where id=?',(incident_id,))
            incident = cursor.fetchone()
        return render_template('incident.html', incident=incident)
    else:
        return redirect(url_for('login'))
    
@app.route('/closeIncident', methods=['POST'])
def closeIncident():
    if request.method == 'POST':
        ip = request.form['ip']
        value = 0
        with sqlite3.connect('data.db') as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE incident set incident_open=? where ip=?',(value,ip,))
            conn.commit()
        flash("Incident closed successfully")
        return redirect(url_for('incidents'))

@app.route('/change-password' , methods = ['GET', 'POST'])
def changePassword():
   if request.method == 'POST':
       password = request.form['password']
       username = session['username']
       with sqlite3.connect('data.db') as conn:
           cursor = conn.execute('UPDATE users set password=? where username=?',(password,username,))
           conn.commit()
           flash("Password changed successfully")
           return redirect(url_for('changePassword'))
   return render_template('change-password.html')

@app.route('/contain-ip',methods=['POST'])
def containip():
    if request.method == 'POST':
        ip = request.form['ip']
        # contain(ip)
        return jsonify({"message":"Contain Success"})
    return jsonify({"message":"Failed"})

@app.route('/uncontain-ip',methods=['POST'])
def uncontainip():
    if request.method == 'POST':
        ip = request.form['ip']
        # uncontain(ip)
        return jsonify({"message":"Uncontain Success"})
    return jsonify({"message":"Failed"})
    
@app.route("/logout")
def logout():
    if 'username' in session:
        session.pop('username',None)
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)