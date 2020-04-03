from flask import Blueprint,render_template,Response
from real_time_video import VideoCamera
video=Blueprint("video",__name__,static_folder="static",template_folder="templates")

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n'+frame+b'\r\n')

@video.route('/video')
def videofile():
    return Response(gen(VideoCamera()), mimetype='multipart/x-fixed-replace;boundary-frame')
    # return "<h1> heeloo</h1>"



# import pickle

# pickle.dump(('video.pkl','wb'))
# video=pickle.load(open('video.pkl','rb'))
