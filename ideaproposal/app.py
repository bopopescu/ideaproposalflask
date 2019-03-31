from flask import Flask, render_template, redirect, request, sessions, session
#from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy

from ocr_core import ocr_core
import pytesseract
import mysql.connector
import os
con = mysql.connector.connect(host="127.0.0.1", database="idea", user="root", password="")

#SECRET_KEY = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:@127.0.0.1/idea'
db=SQLAlchemy(app)
app.secret_key = 'super secret key'

class tbl_idea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sugname = db.Column(db.String(100))
    sugdesc = db.Column(db.String(100))
    username = db.Column(db.String(100))
    votes = db.Column(db.Integer)

    def __repr__(self):
        return f"tbl_idea('{self.id}','{self.sugname}','{self.sugdesc}','{self.username}','{self.votes}')"
class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    emailid = db.Column(db.String(100))
    password = db.Column(db.String(100))
    contact = db.Column(db.String(100))
    github_link = db.Column(db.String(100))
    linkedin_link = db.Column(db.String(100))
    status_user = db.Column(db.String(100))
    idea_no = db.Column(db.String(100))
    ideaname = db.Column(db.String(100))
    ideadesc = db.Column(db.Integer)
    ideatheme = db.Column(db.String(100))
    videopath = db.Column(db.String(100))
    proj_stat = db.Column(db.Integer)


    def __repr__(self):
        return f"tbl_idea('{self.id}','{self.name}','{self.emailid}','{self.password}','{self.contact}'{self.github_link}','{self.linkedin_link}','{self.status_user}','{self.idea_no}'," \
            f"'{self.ideaname}'{self.ideadesc}','{self.ideatheme}','{self.videopath}')"
# define a folder to store and later serve the images
UPLOAD_FOLDER = '/static/uploads/'

# allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


# function to check the file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template("login.html")

@app.route('/register')
def reg():
    return render_template("register.html")

@app.route('/login')
def login():
    cur = con.cursor()
    result = cur.execute("SELECT * FROM users \
                                     WHERE proj_stat = '1' ")
    data = cur.fetchall()
    return render_template("login.html", data=data)

@app.route('/ideasubmit')
def ideasubmit():
    return render_template("ideasubmit.html")

@app.route('/suggestionsubmit')
def suggestionsubmit():
    return render_template("suggestionsubmit.html")

# @app.route('/upload', methods=['GET', 'POST'])
# def upload_page():
#     if request.method == 'POST':
#         # check if there is a file in the request
#         if 'file' not in request.files:
#             return render_template('upload.html', msg='No file selected')
#         file = request.files['file']
#         # if no file is selected
#         if file.filename == '':
#             return render_template('upload.html', msg='No file selected')
#
#         if file and allowed_file(file.filename):
#
#             # call the OCR function on it
#             extracted_text = ocr_core(file)
#
#             # extract the text and display it
#             return render_template('upload.html',
#                                    msg='Successfully processed',
#                                    extracted_text=extracted_text,
#                                    img_src=UPLOAD_FOLDER + file.filename)
#     elif request.method == 'GET':
#         return render_template('upload.html')


@app.route('/reg1', methods=['GET', 'POST'])
def reg1():
    if request.method == 'POST':
        password = request.form['pass']
        if 'file' not in request.files:
            return render_template('register.html', msg='No file selected')
        file = request.files['file']
        # if no file is selected
        if file.filename == '':
            return render_template('register.html', msg='No file selected')

        if file and allowed_file(file.filename):
            # call the OCR function on it
            extracted_text = ocr_core(file)

        cur = con.cursor()
        sql = '''INSERT INTO users(username,password) VALUES (%s,%s)'''
        cur.execute(sql, (extracted_text, password))
        con.commit()

            # extract the text and display it
        return render_template('register.html')
    elif request.method == 'GET':
        return render_template('register.html')

@app.route('/log', methods=['GET', 'POST'])
def log():
    if request.method == 'POST':
        Username = request.form['panid']
        Password = request.form['pass']
        cur = con.cursor()
        result = cur.execute("SELECT username,password FROM users \
                     WHERE username = '%s' and password = '%s'" % \
                                (Username, Password))
        if not cur.fetchone()[0]:
            return "Invalid Credential"
        else:
            data = cur.fetchone()
            session['logged_in'] = True
            session['username'] = Username
            #id = str(data[0])
            #user_role_id = str(data[1])
            user = tbl_idea.query.order_by(tbl_idea.votes.desc())
            return render_template('userhome.html', user=user )
            #Username = data[0]
            Password = data[1]
            #print(Username)

    return render_template('index.html')

@app.route('/logadmin', methods=['GET', 'POST'])
def logadmin():
    if request.method == 'POST':
        Username = request.form['username']
        Password = request.form['pass']
        cur = con.cursor()
        result = cur.execute("SELECT name,password FROM admin_company \
                     WHERE name = '%s' and password = '%s'" % \
                                (Username, Password))
        if not cur.fetchone()[0]:
            return "Invalid Credential"
        else:
            data = cur.fetchone()
            session['logged_in'] = True
            session['username'] = Username
            #id = str(data[0])
            #user_role_id = str(data[1])
            #ide = tbl_idea.query.order_by(tbl_idea.votes.desc())
            #use = users.query.filter_by(status_user='1').all()
            result = cur.execute("SELECT * FROM users \
                                 WHERE status_user = '1' ")
            data = cur.fetchall()
            for row in data:
                print(row)
            return render_template('adminhome.html', data=data)
            #Username = data[0]
            Password = data[1]
            #print(Username)


@app.route('/ideaupload', methods=['GET', 'POST'])
def ideaupload():
    if request.method == 'POST':
        path = os.path.abspath("C://Users//Swaleha//PycharmProjects//ideaproposal//static")
        file1 = request.files['file1']

        file1filename = secure_filename(file1.filename)

        file1path = os.path.join(path, file1filename)

        file1.save(file1path)

        path1 = file1filename
        print(path1)

        ideaname = request.form['ideaname']
        ideadescription = request.form['ideadescription']
        ideatheme = request.form['ideatheme']
        githublink = request.form['githublink']
        linkedinlink = request.form['linkedinlink']

        cur = con.cursor()
        result = cur.execute("""
         UPDATE `users`
         SET `ideaname`=%s, `ideadesc`=%s, `ideatheme`=%s,`videopath`=%s,`github_link`=%s,`linkedin_link`=%s
         WHERE `username`=%s
      """, (ideaname,ideadescription,ideatheme,path1,githublink,linkedinlink,session['username']))

        con.commit()

        if cur.rowcount > 0 :
            return "updated"
        else :
            return "pending"

@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('login.html')

@app.route('/sugupload', methods=['GET', 'POST'])
def sugupload():
    if request.method == 'POST':

        sugname = request.form['sugname']
        sugdescription = request.form['sugdescription']

        cur = con.cursor()
        sql = '''INSERT INTO tbl_idea(sugname,sugdesc,username) VALUES (%s,%s,%s)'''
        cur.execute(sql, (sugname, sugdescription,session['username']))
        con.commit()

        return "inserted"


@app.route('/upvotes', methods=['GET', 'POST'])
def upvotes():
    if request.method == 'POST':

        id = request.form['idofidea']

        cur = con.cursor()
        result = cur.execute("SELECT votes FROM tbl_idea \
                             WHERE id = '%s'" % \
                             (id))

        data = cur.fetchone()[0]
        data1 = int(data)
        data1 = data1 + 1
        data2 = str(data1)

        cur = con.cursor()

        resultt = cur.execute("""
         UPDATE `tbl_idea`
         SET `votes`=%s
         WHERE `id`=%s
      """, (data2,id))

        con.commit()

        if cur.rowcount > 0 :
            return "updated"
        else :
            return "pending"


@app.route('/acceptideas', methods=['GET', 'POST'])
def acceptideas():
    if request.method == 'POST':

        id = request.form['idofpostedidea']

        cur = con.cursor()
        onevalue = 1

        resultt = cur.execute("""
         UPDATE `users`
         SET `proj_stat`=%s
         WHERE `id`=%s
      """, (onevalue,id))

        con.commit()

        if cur.rowcount > 0 :
            return "updated"
        else :
            return "pending"

if __name__ == '__main__':
    app.run()
