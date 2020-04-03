from flask import Blueprint,render_template

prosody=Blueprint("prosody",__name__,static_folder="static",template_folder="templates")

@video.route("/prosody")
return render_template("<h1>hello prosody </h1>")