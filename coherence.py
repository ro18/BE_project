from flask import Blueprint,render_template

coherence=Blueprint("coherence",__name__,static_folder="static",template_folder="templates")

@coherence.route("/coherence")
def coherencefile():
    return render_template("<h1>hello coherence</h1>")