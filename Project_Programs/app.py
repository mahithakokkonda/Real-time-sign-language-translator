from flask import Flask, render_template, request, jsonify, Response
import backend.mysql as mysql  # Changed from 'mongo' to 'mysql'
import body
import cv2
import webbrowser 

username, email, password, disability, role, dob, slink, llink, glink, bio, gender = "", "", "", "", "", "", "", "", "", "", ""
video_camera = None
global_frame = None
image, pred_img, original, crop_bg, label = None, None, None, None, None

body.cap.release()

app = Flask(__name__)

# Index Page
@app.route('/home')
def index():
    body.cap.release()
    return render_template('index.html')

@app.route("/label")  # for label
def label_text():
    return jsonify(label)

@app.route("/translate")  # for translation
def translate():
    body.cap = body.cv2.VideoCapture(0, cv2.CAP_DSHOW)
    txt = label_text()
    return render_template('video_out.html', txt=txt.json)

def gen_vid():  # Video Stream
    global video_camera, global_frame, label 
    while True:
        global image, pred_img, original, crop_bg, name
        image, pred_img, original, crop_bg, name = body.collectData()
        label = name if name else "--"
        frame = cv2.imencode('.jpg', image)[1].tobytes()
        if frame:
            global_frame = frame
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')

@app.route("/video")
def video():
    return Response(gen_vid(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/about")
def about():
    body.cap.release()
    return render_template('about_us.html')

@app.route("/signup")
def sign_up():
    body.cap.release()
    return render_template('sign_up.html')

@app.route("/")
def login():
    body.cap.release()
    return render_template('login.html', userinfo=None, accept=None)

@app.route("/profile")
def profile():
    body.cap.release()
    userinfo = mysql.show(email)
    return render_template('profile.html', userinfo=userinfo)

@app.route("/choice")
def choice():
    return render_template('choice.html')

@app.route("/audio")
def audio():
    body.cap.release()
    return render_template('audio_out.html')

@app.route('/validate', methods=['POST'])
def validate_sign():
    email = request.form['email']
    password = request.form['password']
    if mysql.validate(email, password):
        userinfo = mysql.show(email)
        return render_template('login.html', accept="success", userinfo=userinfo, email=email, password=password)
    else:
        return render_template('login.html', accept="failed", userinfo=None, email=email, password=None)

@app.route('/signup', methods=['POST'])
def getvalue():
    global username, email, password, disability, role, gender
    username = request.form['name']
    email = request.form['email']
    password = request.form['password']
    disability = request.form['inputDisability']
    role = request.form['inputRole']
    gender = request.form['gender']

    print(username, email, password, disability, role, gender)

    if username and email and password and disability and role:
        if mysql.check(email):  # Check if email exists
            print("Email already exists")
            return render_template('sign_up.html', accept="exist", email=email, username=username)
        else:
            # Directly insert user (NO OTP)
            slink, llink, glink, bio = "https://www.facebook.com/", "https://www.linkedin.com/", "https://www.github.com/", ""
            if mysql.insert(username, email, password, disability, role):
                return render_template('sign_up.html', accept="success", email=email, username=username)
            else:
                return render_template('sign_up.html', accept="failed", email=email, username=username)

webbrowser.open('http://127.0.0.1:5000/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True ,port=5000,debug=False)