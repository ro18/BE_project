from flask import Blueprint,render_template

coherence=Blueprint("coherence",__name__,static_folder="static",template_folder="templates")

@video.route("/coherence")
return render_template("<h1>hello coherence</h1>")