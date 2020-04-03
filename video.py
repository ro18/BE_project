from flask import Blueprint,render_template

video=Blueprint("video",__name__,static_folder="static",template_folder="templates")

@video.route('/video')
def videofile():
    return render_template("report_video.html")



# import pickle

# pickle.dump(('video.pkl','wb'))
# video=pickle.load(open('video.pkl','rb'))