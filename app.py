from flask import Flask
import os
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request, render_template, url_for, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from video import video
# from text import text
# from prosody import prosody
from video_audio import destroy
from coherence import coherence_cv
from coherence import coherence_ans
from prosody import prosodyfile
from text import textfile
import collections
import functools
import operator
import ast
import operator
from collections import Counter
import cv2

app = Flask(__name__)
app.register_blueprint(video, url_prefix="")
# app.register_blueprint(text,url_prefix="")
# app.register_blueprint(prosody,url_prefix="")
# app.register_blueprint(coherence,url_prefix="")

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'txt', 'docx', 'png', 'jpg', 'jpeg', 'gif'}

app.secret_key = "secretkey"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['MONGO_URI'] = "mongodb://localhost:27017/interview_training"

mongo = PyMongo(app)


@app.route('/')
def index():
    return render_template("home1.html")


@app.route('/student')
def student():
    prof = []
    profiles = {}

    for x in mongo.db.profile.find({}, {'_id': 0, 'comp_profile': 1}):
        for y in x.values():
            prof.append(y)
    print(prof)

    return render_template("student.html", profiles=prof)


@app.route('/loginForm')
def loginForm():
    return render_template("login.html")


@app.route('/signupForm')
def signupForm():
    return render_template("signup.html")


@app.route('/studentPage')
def studentPage():
    return render_template("student2.html")


@app.route('/adminPage')
def adminPage():
    if 'user' in session:
        return render_template("admin.html")
    else:
        return render_template("login.html")


@app.route('/admin')
def admin():
    return render_template("admin.html")


@app.route('/submitCompany')
def submitCompany():
    return '<h1> add manage profile page </h1>'


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('adminPage'))


@app.route('/studentAccess', methods=['POST'])
def studentAccess():
    values = request.form
    _name = values['name']
    print(_name)
    _email = values['email']
    print(_email)
    _profile = values['comp-profile']
    print(_profile)
    session['stud_profile'] = _profile
    if 'resume' in request.files:
        resume = request.files['resume']
        mongo.save_file(resume.filename, resume)
        filename = secure_filename(resume.filename)
        resume.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    if _name and _profile and _email and request.method == "POST":
        id = mongo.db.student.insert(
            {"name": _name, "email": _email, "comp_profile": _profile, "resume": resume.filename})
    print("hello")
    if 'stud_profile' in session:
        stud = session['stud_profile']
        print(stud)
    keys = mongo.db.profile.find_one({'comp_profile': stud}, {
                                     '_id': 0, 'description': 0, 'comp_profile': 0, 'questions': 0})
    print(keys)
    for key in keys.values():
        session['keywords'] = key
    # session['keywords']=_keyword
    if 'keywords' in session:
        print(session['keywords'])
    questions = []

    value = mongo.db.profile.find_one({'comp_profile': stud}, {
                                      '_id': 0, 'description': 0, 'keywords': 0, 'comp_profile': 0})

    # print(value.values())
    # store all the questions in session
    for value in value.values():
        session['questions'] = value

    # add to the next button to display the next question
    if session['questions']:
        myques = session['questions']
        popped = myques.pop(0)
        session['questions'] = myques
        print(popped)

        return render_template('student2.html', question=popped)


@app.route('/adminAccess', methods=['POST'])
def adminAcess():
    values = request.form
    _username = values['username']
    _password = values['pass']
    session['user'] = _username
    print(session['user'])
    if _username and _password and request.method == "POST":
        valid = mongo.db.admin.find_one(
            {"username": _username, "pass": _password})
        if(valid):
            return redirect(url_for("adminPage"))
        else:
            return redirect(url_for('loginForm'))


@app.route('/signup', methods=['POST'])
def adminSignup():
    values = request.form
    _username = values['username']
    _email = values['email']
    _password = values['pass']
    if _username and _email and _password and request.method == "POST":
        id = mongo.db.admin.insert(
            {"username": _username, "email": _email, "password": _password})
        return render_template("login.html")


@app.route('/description', methods=['POST'])
def description():
    print("desc")
    values = request.form
    _value = values['profile']
    d = []
    desc = mongo.db.profile.find_one({'comp_profile': _value}, {
                                     '_id': 0, 'questions': 0, 'keywords': 0, 'comp_profile': 0})
    for c in desc.values():
        d.append(c)
    print(d)
    return jsonify(description=d)


@app.route('/companyDetails', methods=['POST'])
def companyDetails():
    print("companyDetails")
    values = request.form
    _profile = values['profile']
    _description = values[F'description']
    _keywords = values['keywords']
    _keyword = _keywords.split(',')

    session['comp_profile'] = _profile

    # session['description']=_description
    # session['keywords']=_keyword
    print(_profile)
    if _profile and _description and _keywords and request.method == "POST":
        id = mongo.db.profile.insert(
            {"comp_profile": _profile, "description": _description, "keywords": [_keyword]})
    return render_template("admin.html", profile=_profile, description=_description, keywords=_keywords)
    # return redirect(url_for("quest", profile=_profile, description=_description, keywords=_keywords))
    # return redirect(url_for('adminPage',profile=_profile, description=_description, keywords=_keywords))


@app.route('/addQuestion', methods=['POST'])
def addQuestion():
    print("add question")
    values = request.form
    _value = values['quest']
    print(_value)
    if 'user' in session:
        user = session['user']
    # keywords = values['keywords']
    # _keyword = keywords.split(',')
    # print(user)
    if 'comp_profile' in session:
        pro = session['comp_profile']
    print(pro)
    if _value and request.method == "POST":
        id = mongo.db.profile.find_one_and_update(
            {"comp_profile": pro}, {'$push': {"questions": _value}})
        return redirect(url_for("admin"))


@app.route('/deleteQuestion', methods=['POST'])
def deleteQuestion():
    print("delete question")
    values = request.form
    _value = values['quest']
    print(_value)
    if 'profile' in session:
        pro = session['profile']
        print(pro)
    if _value and request.method == "POST":
        id = mongo.db.profile.find_one_and_delete(
            {"comp_profile": pro}, {"questions": _value})
        return redirect(url_for("admin"))


@app.route('/afterloading')
def afterloading():
    content = []
    print("afterloading")
    # prosody file
    prosodyfile()
    print("ass")
    with open("audio_emotions.txt") as f:
        content = f.read()
    content = content.replace("trainingData/","") 
    content = content.split("\n")
    content = [x.strip() for x in content]
    # print(content)
    with open("audio_coordinates.txt") as f:
        au = f.read()
    au= au.replace("[", "")
    au = au.replace("]","")
    au = au.split("\n")
    au.pop()
    print(au)
    print(type(au))
    resultant=[0,0,0,0,0]
    lenz=len(au)
    for x in au:
        print(x)
        res=list(map(float,x.split()))
        print("res")
        print(res)
        print(res[0])
        for y in range(5):
            print(y)
            resultant[y] = resultant[y] + res[y]
            print("resultant")
            print(resultant)
    au = [r/lenz for r in resultant]
    print("au")
    print(au)
    print("after prosodyfile")
    print("before emotions")
    with open("emotions.txt") as f:
        contente = f.readlines()
    contente = [x.strip() for x in contente]
    print("contente")
    print(contente)
    resultant = {}
    resultant = Counter(resultant)
    with open("emotions_coordinates.txt") as f:
        cp = f.read()
    co = cp.split("\n")
    print(co)
    print(type(co))
    co.pop()
    for x in co:
        res = ast.literal_eval(x)
        res = Counter(res)
        print("res")
        print(res)
        resultant = resultant + res
        print("resultant")
        print(resultant)
    emotion_values = resultant. values()
    emotion_keys = []
    print(emotion_values)
    emotions = ["Angry", "Disgust", "Scared",
                "Happy", "Sad", "Surprised", "Neutral"]
    for x in resultant.keys():
        emotion_keys.append(emotions[x])
    print("emotion_keys")
    print(emotion_keys)
    print("after emotions")
    print(resultant)
    # text file
    cv, ans = textfile()
    #coherence
    if 'keywords' in session:
        k = session['keywords']
    co_cv,co_cv_d = coherence_cv(k)
    co_ans,co_ans_d= coherence_ans(k)
    cv_keys = co_cv_d.keys()
    ans_keys = co_ans_d.keys()
    ans_values = co_cv_d.values()
    cv_values=co_cv_d.values()
    
    return render_template("report.html",cv_keys=cv_keys,ans_keys=ans_keys,ans_values=ans_values,
    cv_values=cv_values, prosody=content, text_cv=cv, text_ans=ans, co_cv=co_cv, 
    co_ans=co_ans, emotions=contente, emotion_keys=emotion_keys, emotion_values=emotion_values,audio_values=au)


@app.route('/loading')
def loading():
    destroy()
    return render_template("loading.html")


# the below is for displaying next question---REnder it to the loading page in the else
@app.route('/next')
def next():
    if session['questions']:
        myques = session['questions']
        popped = myques.pop(0)
        session['questions'] = myques
        # print(popped)
        return render_template("student2.html", question=popped)
    else:
        # add loading page here after all questions

        return redirect(url_for("loading"))

@app.route('/finish')
def finish():
    mydir="./audio"
    filelist = [ f for f in os.listdir(mydir) ]
    for f in filelist:
        os.remove(os.path.join(mydir, f))

if __name__ == "__main__":
    # app.run(debug=False)
    app.run(host='http://127.0.0.1:5000/', debug=True, threaded=True)


# this is reference Route -loads the questions in the session ----the below code has been added to route studentLogin
