from flask import Blueprint,render_template

prosody=Blueprint("prosody",__name__,static_folder="static",template_folder="templates")

@prosody.route("/prosody")
def prosodyfile():
    return render_template("<h1>hello prosody </h1>")