from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def main():
	return render_template('web.html')

@app.route('/index1')
def index1():
	conn = sqlite3.connect('main.db')
	cur = conn.cursor()
	conn.commit()
	conn.close()
	return render_template('web.html')

@app.route('/index')
def index():
	return render_template('web.html')

@app.route('/showlogin')
def showlogin():
	return render_template('login.html')

@app.route('/showgg/<user>')
def showgg(user):
	conn = sqlite3.connect('main.db')
	cur = conn.cursor()
	cur.execute("SELECT gmem FROM users WHERE usern = ?",(user,))
	var = cur.fetchone()
	i = var[0]
	conn.commit()
	conn.close()
	if (i == 0):
		return render_template('create.html',user = user)
	else:
		conn = sqlite3.connect('group.db')
		cur = conn.cursor()
		cur.execute("SELECT grname FROM {} ".format(user))
		var1 = cur.fetchall()
		conn.commit()
		conn.close()
		return render_template('mgroup.html',groupn = var1,user = user)
	

@app.route('/login', methods=['POST'])
def login():
	conn = sqlite3.connect('main.db')
	cur = conn.cursor()
	usern = request.form['usern']
	password = request.form['password']
	cur.execute("SELECT usern FROM users WHERE usern = ? AND password= ?",(usern,password,))
	var = cur.fetchone()
	conn.commit()
	conn.close()
	if var:
		conn = sqlite3.connect('main.db')
		cur = conn.cursor()
		cur.execute("SELECT bod,bio,stud,work FROM {} WHERE usnm = ?".format(usern),(usern,))
		var3 = cur.fetchone()
		cur.execute("SELECT gname FROM deltemp WHERE uname = ?",(usern,))
		var5 = cur.fetchone()
		conn.commit()
		conn.close()
		conn = sqlite3.connect('group.db')
		cur = conn.cursor()
		cur.execute("SELECT gname FROM delgrus WHERE uname = ?",(usern,))
		var4 = cur.fetchall()
		cur.execute("SELECT gname FROM delgr WHERE uname = ?",(usern,))
		var1 = cur.fetchone()
		conn.commit()
		conn.close()
		if var5:
			if var3:
				if var4:
					if var1:
						return render_template('user.html',user = var,dec = var5,prof = var3,dell = var4,adm = var1)
					else:
						return render_template('user.html',user = var,dec = var5,prof = var3,dell = var4)
				else:
					if var1:
						return render_template('user.html',user = var,dec = var5,prof = var3,adm = var1)
					else:
						return render_template('user.html',user = var,dec = var5,prof = var3)
			else:
				if var1:
					return render_template('user.html',user = var,dec = var5,adm = var1)
				else:
					return render_template('user.html',user = var,dec = var5)
		else :
			if var3:
				if var4:
					if var1:
						return render_template('user.html',user = var,prof =var3,dell = var4,adm = var1)
					else:
						return render_template('user.html',user = var,prof =var3,dell = var4)
				else:
					if var1:
						return render_template('user.html',user = var,prof =var3,adm = var1)
					else:
						return render_template('user.html',user = var,prof =var3)
			else:
				if var1:
					return render_template('user.html',user = var,adm = var1)
				else:
					return render_template('user.html',user = var)

				
	elif ((usern=="admin") & (password == "admin")):
		conn = sqlite3.connect('main.db')
		cur = conn.cursor()
		cur.execute("SELECT * FROM groups") 
		var2 = cur.fetchall()
		cur.execute("SELECT groupn,admin FROM groups WHERE del = ?",("Yes",))
		vrr = cur.fetchall()
		conn.commit()
		conn.close()
		conn = sqlite3.connect('feedback.db')
		cur = conn.cursor()
		cur.execute("SELECT name,feeds FROM feedst") 
		vrrx = cur.fetchall()
		if vrr:
			if vrrx:
				return render_template('admin.html',group = var2,req = vrr,feeds = vrrx)
			else:
				return render_template('admin.html',group = var2,req = vrr)
			
		else:
			if vrrx:
				return render_template('admin.html',group = var2,feeds= vrrx)
			else:
				return render_template('admin.html',group = var2)
	else:
		return render_template('login.html',message = "Invalid username or password")
	
@app.route('/showsignup')
def showsignup():
	return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
	email = request.form['email']
	usern = request.form['usern']
	password = request.form['password']
	p = request.form['p']
	conn = sqlite3.connect('main.db')
	cur = conn.cursor()
	cur.execute("INSERT INTO users VALUES(?,?,?,?,?)",(email,usern,password,0,"No",))
	cur.execute("CREATE TABLE {} (usnm TEXT,bod CHAR[20],bio TEXT,stud TEXT,work TEXT)".format(usern))
	cur.execute("INSERT INTO {}(usnm) VALUES(?)".format(usern),(usern,))
	cur.execute("SELECT usern FROM users WHERE usern = ? AND password=?",(usern,password,))
	var = cur.fetchone()
	conn.commit()
	conn.close()
	if(password == p):
		conn = sqlite3.connect('group.db')
		cur = conn.cursor()
		cur.execute("CREATE TABLE {}(grname TEXT,mem TEXT)".format(usern))
		conn.commit()
		conn.close()
		return render_template('user.html',user = var,message = "Welcome to FCW")
	else:
		conn = sqlite3.connect('main.db')
		cur = conn.cursor()
		cur.execute("DELETE FROM users WHERE usern = ?",(usern,))
		cur.execute("DROP TABLE {}".format(usern))
		conn.commit()
		conn.close()
		return render_template('signup.html',message = "Error in password confirmation")
	
@app.route('/search/<user>', methods=['POST','GET'])
def search(user):
	search = request.form['search']
	conn = sqlite3.connect('main.db')
	cur = conn.cursor()
	cur.execute("SELECT groupn FROM groups WHERE groupn LIKE ? AND admin != ?",('%'+search+'%',user,))
	var = cur.fetchall()
	conn.commit()
	conn.close()
	return render_template('group.html',groupn = var,user = user)

@app.route('/create/<user>', methods=['POST'])
def create(user):
	groupn = request.form['groupn']
	conn = sqlite3.connect('main.db')
	cur = conn.cursor()
	cur.execute("SELECT adm FROM users WHERE usern = ?",(user,))
	var1 = cur.fetchone()
	conn.commit()
	conn.close()
	if(var1[0] == "No"):
		conn = sqlite3.connect('main.db')
		cur = conn.cursor()
		cur.execute("CREATE TABLE {}(guser TEXT,sex TEXT,father TEXT)".format(groupn))
		cur.execute("INSERT INTO groups VALUES(?,?,?)",(groupn,user,"No"))
		cur.execute("UPDATE users SET adm = ? WHERE usern = ?",("Yes",user))
		conn.commit()
		conn.close()
		conn = sqlite3.connect('group.db')
		cur = conn.cursor()
		cur.execute("CREATE TABLE {}(post TEXT,usern TEXT,mem TEXT)".format(groupn))
		conn.commit()
		conn.close()
		return render_template('new.html',groupn = groupn,message = "No new requests",user = user)
	else:
		return render_template('create.html',message = "Already an admin",user = user)

@app.route('/join/<user>', methods=['POST','GET'])
def join(user):
	gname = request.form['groupn']
	conn = sqlite3.connect('main.db')
	cur = conn.cursor()
	cur.execute("INSERT INTO adtemp VALUES(?,?)",(gname,user))
	cur.execute("SELECT father,mother,spouse,fmname FROM familydet WHERE usern = ?",(user,))
	var2 = cur.fetchone()
	if var2:
		cur.execute("INSERT INTO familytem VALUES(?,?,?,?,?,?)",(user,gname,var2[0],var2[1],var2[2],var2[3]))
		conn.commit()
		conn.close()
		return render_template('group.html',message = "Request send!!!",user = user)
	else:
		return render_template('group.html',message = "Edit your family details",user = user)

@app.route('/showmg/<user>')
def showmg(user):
	conn = sqlite3.connect('main.db')
	cur = conn.cursor()
	cur.execute("SELECT groupn FROM groups WHERE admin = ?",(user,))
	var1 = cur.fetchone()
	if var1:
		cur.execute("SELECT * FROM {} ".format(var1[0]))
		var2 =cur.fetchall()
		cur.execute("SELECT usern,father,mother,spouse,fmname FROM familytem WHERE groupn = ?",(var1[0],))
		var4 = cur.fetchall()
		conn.commit()
		conn.close()
		if var4:
			return render_template('new.html',groupn = var1[0],reqst = var4,mems = var2,user = user)
		else:
			return render_template('new.html',groupn = var1[0],message = "No new requests",mems = var2,user =user)
	else:
		return render_template('void.html',message = "Not an admin of any group",user = user)

@app.route('/showprof/<user>')
def showprof(user):
	conn = sqlite3.connect('main.db')
	cur = conn.cursor()
	cur.execute("SELECT usern FROM users WHERE usern = ?",(user,))
	var = cur.fetchone()
	cur.execute("SELECT bod,bio,stud,work FROM {} WHERE usnm = ?".format(user),(user,))
	var1 = cur.fetchone()
	cur.execute("SELECT gname FROM deltemp WHERE uname = ?",(user,))
	var2 = cur.fetchall()
	conn.commit()
	conn.close()
	conn = sqlite3.connect('group.db')
	cur = conn.cursor()
	cur.execute("SELECT gname FROM delgrus WHERE uname = ?",(user,))
	var3 = cur.fetchall()
	conn.commit()
	conn.close()
	if var1:
		if var2:
			if var3:
				return render_template('user.html',user = var,prof = var1,dec = var2, dell =var3)
			else:
				return render_template('user.html',user = var,prof = var1,dec = var2)
		else:
			if var3:
				return render_template('user.html',user = var,dec = var2, dell =var3)
			else:
				return render_template('user.html',user = var,dec = var2)
	else:
		return render_template('user.html',user = var)

@app.route('/accept/<usern>/<gname>/<user>')
def accept(usern,gname,user):
	conn = sqlite3.connect('main.db')
	cur = conn.cursor()
	cur.execute("SELECT father FROM familydet WHERE usern = ?",(usern,))
	v = cur.fetchone()
	cur.execute("INSERT INTO {} VALUES(?,?,?)".format(gname),(usern,"Daughter",v[0]))
	cur.execute("DELETE FROM familytem WHERE usern = ? AND groupn = ?",(usern,gname,))
	cur.execute("SELECT gmem FROM users WHERE usern = ?",(usern,))
	var = cur.fetchone()
	i = var[0]
	i += 1
	cur.execute("UPDATE users SET gmem = ? WHERE usern = ?",(i,usern))
	cur.execute("SELECT usern,father,mother,spouse,fmname FROM familytem WHERE groupn = ?",(gname,))
	var1 = cur.fetchall()
	cur.execute("SELECT * FROM {} ".format(gname))
	var2 = cur.fetchall()
	conn.commit()
	conn.close()
	conn = sqlite3.connect('group.db')
	cur = conn.cursor()
	cur.execute("INSERT INTO {} VALUES(?,?)".format(usern),(gname,"Yes",))
	conn.commit()
	conn.close()
	if var1:
		return render_template('new.html',groupn = gname,reqst = var1,mems = var2,user = user)
	else:
		return render_template('new.html',groupn = gname,message = "No new requests",mems = var2,user = user)


@app.route('/edit/<user>')
def edit(user):
	return render_template('edit.html',user = user)

@app.route('/update/<user>',methods =['POST'])
def update(user):
	bod = request.form['bod']
	work = request.form['work']
	stud = request.form['stud']
	bio = request.form['bio']
	conn = sqlite3.connect('main.db')
	cur = conn.cursor()
	cur.execute("SELECT usnm FROM {} WHERE usnm = ?".format(user),(user,))
	var = cur.fetchone()
	cur.execute("UPDATE {} SET bod = ?,bio = ?,stud = ?,work =? WHERE usnm = ?".format(user),(bod,bio,stud,work,user))
	conn.commit()
	cur.execute("SELECT bod,bio,stud,work FROM {} WHERE usnm = ?".format(user),(user,))
	var1 = cur.fetchone()
	conn.commit()
	conn.close()
	return render_template('user.html',user = var,prof = var1)

@app.route('/goto/<group>/<user>',methods =['POST'])
def goto(group,user):
	conn = sqlite3.connect('main.db')
	cur = conn.cursor()
	cur.execute("SELECT * FROM {} ".format(group))
	var2 = cur.fetchall()
	conn.commit()
	conn.close()
	conn = sqlite3.connect('group.db')
	cur = conn.cursor()
	cur.execute("SELECT mem FROM {} WHERE grname = ?".format(user),(group,))
	var = cur.fetchone()
	conn.commit()
	conn.close()
	if var:
		if var2:
			return render_template('new.html',user = user,groupn = group,visit = var,mems = var2)
		else:
			return render_template('new.html',user = user,groupn = group,visit = var)

@app.route('/posts/<user>/<group>')
def posts(user,group):
	conn = sqlite3.connect('group.db')
	cur = conn.cursor()
	cur.execute("SELECT post,usern FROM {}".format(group))
	var = cur.fetchall()
	conn.commit()
	conn.close()
	if var:
		return render_template('posts.html',user = user,group = group,post = var)
	else:	
		return render_template('posts.html',user = user,group = group)

@app.route('/status/<user>/<group>',methods =['POST'])
def status(user,group):
	status = request.form['status']
	conn = sqlite3.connect('group.db')
	cur = conn.cursor()
	cur.execute("INSERT INTO {} VALUES(?,?,?)".format(group),(status,user,"Yes",))
	conn.commit()
	cur.execute("SELECT post,usern FROM {}".format(group))
	var = cur.fetchall()
	conn.commit()
	conn.close()
	if var:
		return render_template('posts.html',user = user,group = group,post = var)
	else:
		return render_template('posts.html',user = user,group = group)

@app.route('/searchu/<user>', methods=['POST','GET'])
def searchu(user):
	search = request.form['search']
	conn = sqlite3.connect('main.db')
	cur = conn.cursor()
	cur.execute("SELECT groupn FROM groups WHERE groupn LIKE ? AND admin != ?",('%'+search+'%',user,))
	var = cur.fetchall()
	cur.execute("SELECT usern FROM users WHERE usern LIKE ? AND usern != ?",('%'+search+'%',user,))
	var1 = cur.fetchall()
	conn.commit()
	conn.close()
	return render_template('group.html',groupn = var,user = user,searchu = var1)


@app.route('/decline/<usern>/<gname>/<user>')
def decline(usern,gname,user):
	conn = sqlite3.connect('main.db')
	cur = conn.cursor()
	cur.execute("DELETE FROM adtemp WHERE uname = ?",(usern,))
	cur.execute("SELECT uname FROM adtemp WHERE gname = ?",(gname,))
	var1 = cur.fetchall()
	cur.execute("INSERT INTO deltemp VALUES(?,?,?)",(gname,usern,"Yes"))
	cur.execute("SELECT * FROM {} ".format(gname))
	var2 = cur.fetchall()
	conn.commit()
	conn.close()
	if var1:
		return render_template('new.html',groupn = gname,reqst = var1,mems = var2,user = user)
	else:
		return render_template('new.html',groupn = gname,message = "No new requests",mems = var2,user = user)

@app.route('/close/<usern>/<group>')
def close(usern,group):
	conn = sqlite3.connect('main.db')
	cur = conn.cursor()
	cur.execute("DELETE FROM deltemp WHERE gname = ?",(group,))
	cur.execute("SELECT usern FROM users WHERE usern = ?",(usern,))
	var = cur.fetchone()
	cur.execute("SELECT bod,bio,stud,work FROM {} WHERE usnm = ?".format(usern),(usern,))
	var1 = cur.fetchone()
	cur.execute("SELECT gname FROM deltemp WHERE uname = ?",(usern,))
	var2 = cur.fetchall()
	conn.commit()
	conn.close()
	conn = sqlite3.connect('group.db')
	cur = conn.cursor()
	cur.execute("DELETE FROM delgrus WHERE gname = ?",(group,))
	cur.execute("DELETE FROM delgr WHERE gname = ?",(group,))
	conn.commit()
	conn.close()
	if var1:
		if var2:
			return render_template('user.html',user = var,dec = var2,prof = var1)
		else:
			return render_template('user.html',user = var,prof = var1)
	else:
		return render_template('user.html',user = var)

@app.route('/deleteg/<user>/<groupn>')
def deleteg(user,groupn):
	conn = sqlite3.connect('main.db')
	cur = conn.cursor()
	cur.execute("UPDATE groups SET del = ? WHERE admin = ?",("Yes",user))
	conn.commit()
	cur.execute("SELECT del FROM groups WHERE admin = ?",(user,))
	var = cur.fetchone()
	cur.execute("SELECT uname FROM adtemp WHERE gname = ?",(groupn,))
	var1 = cur.fetchall()
	cur.execute("SELECT * FROM {} ".format(groupn))
	var2 = cur.fetchall()
	conn.commit()
	conn.close()
	if var:
		if var1:
			return render_template('new.html',groupn = groupn,reqst = var1,mems = var2,user = user,send=var)
		else:
			return render_template('new.html',groupn = groupn,message = "No new requests",mems = var2,user = user,send = var)
	else:
		if var1:
			return render_template('new.html',groupn = groupn,reqst = var1,mems = var2,user = user)
		else:
			return render_template('new.html',groupn = groupn,message = "No new requests",mems = var2,user = user)

@app.route('/delg/<user>/<groupn>')
def delg(user,groupn):
	conn = sqlite3.connect('main.db')
	cur = conn.cursor()
	cur.execute("UPDATE users SET adm = ? WHERE usern = ?",("No",user))
	cur.execute("SELECT * FROM {} ".format(groupn))
	var = cur.fetchall()
	for y in var:
		conn = sqlite3.connect('main.db')
		cur = conn.cursor()
		cur.execute("SELECT gmem FROM users WHERE usern = ?",(y[0],))
		var1 = cur.fetchone()
		i = var1[0]
		i -= 1
		cur.execute("UPDATE users SET gmem = ? WHERE usern = ?",(i,user,))
		conn.commit()
		conn.close()
		conn = sqlite3.connect('group.db')
		cur = conn.cursor()
		cur.execute("INSERT INTO delgrus VALUES (?,?)",(groupn,y[0]))
		cur.execute("DELETE FROM {} WHERE grname = ?".format(y[0]),(groupn,))
		conn.commit()
		conn.close()
	conn = sqlite3.connect('main.db')
	cur = conn.cursor()
	cur.execute("DELETE FROM groups WHERE admin = ?",(user,))
	cur.execute("DROP TABLE {}".format(groupn))
	conn.commit()
	conn.close()
	conn = sqlite3.connect('group.db')
	cur = conn.cursor()
	cur.execute("INSERT INTO delgr VALUES (?,?)",(groupn,user))
	cur.execute("DROP TABLE {}".format(groupn))
	conn.commit()
	conn.close()
	conn = sqlite3.connect('main.db')
	cur = conn.cursor()
	cur.execute("SELECT * FROM groups") 
	var2 = cur.fetchall()
	cur.execute("SELECT groupn,admin FROM groups WHERE del = ?",("Yes",))
	vrr = cur.fetchall()
	conn.commit()
	conn.close()
	if vrr:
		return render_template('admin.html',group = var2,req = vrr)
	else:
		return render_template('admin.html',group = var2)

@app.route('/visit/<user>/<visus>',methods =['POST'])
def visit(user,visus):
	conn = sqlite3.connect('main.db')
	cur = conn.cursor()
	cur.execute("SELECT groupn FROM groups WHERE admin = ?",(visus,))
	var = cur.fetchone()
	cur.execute("SELECT usern FROM users WHERE usern = ?",(visus,))
	var2 = cur.fetchone()
	cur.execute("SELECT bod,bio,stud,work FROM {} WHERE usnm = ?".format(visus),(visus,))
	var3 = cur.fetchone()
	conn.commit()
	conn.close()
	conn = sqlite3.connect('group.db')
	cur = conn.cursor()
	cur.execute("SELECT grname FROM {}".format(visus))
	var1 = cur.fetchall()
	conn = sqlite3.connect('main.db')
	cur = conn.cursor()
	if var:
		return render_template('visuser.html',grup = var1,adm = var[0],user = var2,reuser = user,prof = var3)
	else:
		return render_template('visuser.html',grup = var1,user = var2,reuser = user,prof = var3)

@app.route('/feedback',methods =['POST'])
def feedback():
	name = request.form['name']
	email = request.form['email']
	feeds = request.form['feeds']
	conn = sqlite3.connect('feedback.db')
	cur = conn.cursor()
	cur.execute("INSERT INTO feedst VALUES(?,?,?)",(name,email,feeds,))
	conn.commit()
	conn.close()
	return render_template('web.html')

@app.route('/add/<user>',methods =['POST'])
def add(user):
	usern = request.form['usern']
	conn = sqlite3.connect('main.db')
	cur = conn.cursor()
	cur.execute("SELECT groupn FROM groups WHERE admin = ?",(user,))
	var = cur.fetchone()
	cur.execute("INSERT INTO {} VALUES(?)".format(var[0]),(usern,))
	conn.commit()
	conn.close()
	conn = sqlite3.connect('group.db')
	cur = conn.cursor()
	cur.execute("INSERT INTO {} (grname) VALUES(?)".format(usern),(var[0],))
	conn.commit()
	conn.close()
	return render_template('group.html',message = "A member is added",user = user)

@app.route('/list/<user>',methods =['POST'])
def list(user):
	conn = sqlite3.connect('main.db')
	cur = conn.cursor()
	cur.execute("SELECT usern FROM users")
	var = cur.fetchall()
	conn.commit()
	conn.close()
	return render_template('group.html',addmem = var,user = user)

@app.route('/editf/<user>')
def editf(user):
	return render_template('editfam.html',user = user)

@app.route('/updatefm/<user>',methods =['POST'])
def updatefm(user):
	father = request.form['father']
	mother = request.form['mother']
	spouse = request.form['spouse']
	fname = request.form['fname']
	conn = sqlite3.connect('main.db')
	cur = conn.cursor()
	cur.execute("SELECT usnm FROM {} WHERE usnm = ?".format(user),(user,))
	var = cur.fetchone()
	cur.execute("INSERT INTO familydet VALUES(?,?,?,?,?)",(user,father,mother,spouse,fname))
	conn.commit()
	cur.execute("SELECT father,mother,spouse,fmname FROM familydet WHERE usern = ?",(user,))
	var2 = cur.fetchone()
	cur.execute("SELECT bod,bio,stud,work FROM {} WHERE usnm = ?".format(user),(user,))
	var1 = cur.fetchone()
	conn.commit()
	conn.close()
	return render_template('user.html',user = var,prof = var1,fam = var2)

if __name__ == "__main__":
	app.run(debug = True)
	