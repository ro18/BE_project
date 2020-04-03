from flask import Blueprint,render_template

text=Blueprint("text",__name__,static_folder="static",template_folder="templates")

@video.route("/text")
return render_template("<h1>hello text/h1>")