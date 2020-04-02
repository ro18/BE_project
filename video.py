from flask import Blueprint,render_template

video=Blueprint("video",__name__,static_folder="static",template_folder="templates")

@video.route("/video")
return render_template("<h1>hello video</h1>")



# import pickle

# pickle.dump(('video.pkl','wb'))
# video=pickle.load(open('video.pkl','rb'))