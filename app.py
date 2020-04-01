from flask import Flask

from flask_pymongo import PyMongo

from bson.json_util import dumps

from bson.objectid import ObjectId

from flask import jsonify, request, render_template, url_for,session

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = "secretkey"

app.config['MONGO_URI'] = "mongodb://localhost:27017/interview_training"

mongo = PyMongo(app)


@app.route('/')
def index():
    return render_template("home.html")

@app.route('/student')
def student():
    return render_template("student.html")

@app.route('/admin')
def admin():
    return render_template("login.html")

@app.route('/signupForm')
def adminSignupForm():
    return render_template("signup.html")

@app.route('/studentAccess',methods=['POST'])
def studentLogin():
    values = request.form
    _name = values['name']
    _email = values['email']
    _profile = values['profile']
    if 'resume' in request.files:
        resume = request.files['resume']
        mongo.save_file(resume.filename, resume)
    if _name and _profile and _email and request.method == "POST":
        id = mongo.db.student.insert(
            {"name": _name,"email":_email, "profile": _profile, "resume": resume.filename})
    return render_template("student2.html")

@app.route('/adminAccess',methods=['POST'])
def adminLogin():
    values = request.form
    _username = values['username']
    _password = values['pass']
    session['user']=_username
    if _username  and _password and request.method == "POST":
        valid = mongo.db.admin.find_one({"username": _username, "pass": _password})
        if(valid):
            return render_template("admin.html")
        else:
            return render_template('login.html')
    

@app.route('/signup', methods=['POST'])
def adminSignup():
    values = request.form
    _username = values['username']
    _email = values['email']
    _password = values['pass']
    if _username and _email and _password and request.method == "POST":
        id = mongo.db.admin.insert({"username": _username, "email": _email, "pass": _password})
    return render_template("login.html")

@app.route('/companyDetails', methods=['POST'])
def addCompany():
    values = request.form
    _profile = values['profile']
    _description = values['description']
    _keywords = values['keywords']
    session['profile']=_profile
    print(_profile)
    return render_template("admin.html", profile=_profile, description=_description, keywords=_keywords)

@app.route('/addQuestions', methods=['POST'])
def addQuestion():
    print("add question")
    values = request.form
    _value = values['quest']
    print(_value)
    if 'user' in session:
        user = session['user']
    # keywords = values['keywords']
    # _keyword = keywords.split(',')
    print(user)
    if 'profile' in session:
        profile = session['profile']
    if _value and request.method == "POST":
        id = mongo.db.admin.find_one_and_update(
            {"profile":profile},{ "questions": [{'value': _value, "status": "true"}]})
        return redirect(url_for("quest"))

