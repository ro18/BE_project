from flask import Flask

from flask_pymongo import PyMongo

from bson.json_util import dumps

from bson.objectid import ObjectId

from flask import jsonify, request, render_template, url_for,session,redirect

from werkzeug.security import generate_password_hash, check_password_hash

from video import video

from text import text

from prosody import prosody

from coherence import coherence

app = Flask(__name__)
app.register_blueprint(video,url_prefix="")
app.register_blueprint(text,url_prefix="")
app.register_blueprint(prosody,url_prefix="")
app.register_blueprint(coherence,url_prefix="")

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

@app.route('/studentPage')
def studentPage():
    return render_template("student2.html")

@app.route('/questions')
def quest():
    return render_template("admin.html")

@app.route('/studentAccess',methods=['POST'])
def studentLogin():
    values = request.form
    _name = values['name']
    _email = values['email']
    _profile = values['comp_profile']
    if 'resume' in request.files:
        resume = request.files['resume']
        mongo.save_file(resume.filename, resume)
    if _name and _profile and _email and request.method == "POST":
        id = mongo.db.student.insert(
            {"name": _name,"email":_email, "comp_profile": _profile, "resume": resume.filename})
        questions = []
        value = mongo.db.profile.find_one({'comp_profile': _profile}, {
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
   

@app.route('/adminAccess',methods=['POST'])
def adminLogin():
    values = request.form
    _username = values['username']
    _password = values['pass']
    session['user']=_username
    print(session['user'])
    if _username  and _password and request.method == "POST":
        valid = mongo.db.admin.find_one({"username": _username, "pass": _password})
        if(valid):
            return render_template("admin.html")
        else:
            return render_template('login.html')
    
# @app.route('/studentAccess',methods=['POST'])
# def studentLogin():
#     values = request.form
#     _name = values['name']
#     _email = values['email']
#     _profile = values['profile']
#     if 'resume' in request.files:
#         resume = request.files['resume']
#         mongo.save_file(resume.filename, resume)
#     if _name and _profile and _email and request.method == "POST":
#         id = mongo.db.student.insert(
#             {"name": _name,"email":_email, "profile": _profile, "resume": resume.filename})
#     return render_template("student2.html")

@app.route('/signup', methods=['POST'])
def adminSignup():
    values = request.form
    _username = values['username']
    _email = values['email']
    _password = values['pass']
    if _username and _email and _password and request.method == "POST":
        id = mongo.db.admin.insert(
            {"username": _username,"email":_email, "password":_password})
    return render_template("login.html")



@app.route('/companyDetails', methods=['POST'])
def companyDetails():
    print("dets")
    values = request.form
    _profile = values['profile']
    _description = values[F'description']
    _keywords = values['keywords']
    _keyword = _keywords.split(',')
    session['profile']=_profile
    # session['description']=_description
    # session['keywords']=_keyword
    print(_profile)
    if  _profile and _description and _keywords and request.method == "POST":
        id = mongo.db.profile.insert({"comp_profile": _profile, "description": _description, "keywords":[ _keyword]},questions:['tell us about yourself'])
    return render_template("admin.html", profile=_profile, description=_description, keywords=_keywords)
    # return redirect(url_for("quest", profile=_profile, description=_description, keywords=_keywords))
    #return redirect(url_for('adminPage',profile=_profile, description=_description, keywords=_keywords))


@app.route('/addQuestion', methods=['POST'])
def addQuestion():
    print("add question")
    values = request.form
    _value = values['quest']
    print(_value)
    if 'user' in session:
        user = session['user']
        print(user)
    if 'profile' in session:
        profileval = session['profile']
        print(profileval)
    if _value and request.method == "POST":
        id = mongo.db.admin.find_one_and_update(
        mongo.db.profile.find_one_and_update({"comp_profile":profileval},{"$push":{ "questions": _value}})
        return redirect(url_for("quest"))
    
@app.route('/video')
def startQuestion():
    print("hello")
    questions = []
    value = mongo.db.profile.find_one({'comp_profile': 'GEP-Tester'}, {'_id': 0, 'description': 0, 'keywords': 0, 'comp_profile': 0})
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

# the below is for displaying next question---REnder it to the loading page in the else
@app.route('/next')
def next():
    if session['questions']:
        myques = session['questions']
        popped = myques.pop(0)
        session['questions'] = myques
        print(popped)
        return render_template("student2.html", question=popped)
    else:
        # add loading page here after all questions
        return("<h1>questions over</h1>")

if __name__ == "__main__":
    # app.run(debug=False)
    app.run(host='http://127.0.0.1:5000/', debug=True, threaded=True)


# this is reference Route -loads the questions in the session ----the below code has been added to route studentLogin