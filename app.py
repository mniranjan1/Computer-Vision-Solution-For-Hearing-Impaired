from flask_wtf.file import FileField, FileAllowed
from flask_security import Security, SQLAlchemyUserDatastore, RoleMixin
import pygame
from flask_admin import Admin
from gtts import gTTS
from script import run_avg, segment
from threading import Thread
from tensorflow.python.keras.backend import set_session
import tensorflow as tf
import numpy as np
import imutils
from tensorflow.keras.models import Sequential, save_model, load_model
import time
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from flask_wtf import FlaskForm
from flask_migrate import Migrate
from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user, login_required
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib import sqla
from flask_admin import Admin, AdminIndexView
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, Response, jsonify, redirect, url_for, request, flash
from flask_cqlalchemy import CQLAlchemy
from ssl import SSLContext, PROTOCOL_TLS, CERT_REQUIRED
from cassandra.auth import PlainTextAuthProvider
import cv2
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, BooleanField
from cassandra.cqlengine.management import sync_table, drop_table
from cassandra.cluster import Cluster
import os
import uuid
import speech_recognition as sr
import logging

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

language = 'en'
IMG_SIZE = 256

pygame.init()


def say(text):
    tts = gTTS(text=text, lang='en')
    filename = "audio1.mp3"
    tts.save(filename)
    pygame.mixer.init()
    pygame.mixer.music.load("audio1.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.quit()
    os.remove(filename)


sess = tf.Session()
graph = tf.get_default_graph()

# IMPORTANT: models have to be loaded AFTER SETTING THE SESSION for keras!
# Otherwise, their weights will be unavailable in the threads after the session there has been set
set_session(sess)
model = load_model('handsign1.h5')
print('model loaded')

pre = []
out_label = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
             'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'space', 'del', 'Love', 'Remember', 'Best of Luck', 'You', 'Rock', 'Like']

text = ''
word = ''
app = Flask(__name__)
cloud_config= {
        'secure_connect_bundle': 'secure-connect-flask.zip'
}
auth_provider = PlainTextAuthProvider(username='weUCOUqsJFWMQzUXlIuDBQaw', password='iZrSkM5t00Ao1fslKMlb1f76laXAAIxfU7Ovx9N,LllOe3duihCio5Z2i7bn.0tYw._W1H8HAjqU307ERtzZugx6gxDLM0q,b8RJt4gvmf7H,pJ544DDbc.Z4ugPbYrH')

app.config['CASSANDRA_HOSTS'] = ['7f3e974e-593e-4870-84cf-cd369a3604ae-us-east1.db.astra.datastax.com']
app.config['CASSANDRA_SETUP_KWARGS'] = dict(cloud=cloud_config,auth_provider=auth_provider)
app.config['CASSANDRA_KEYSPACE'] = "flaskspace"
db = CQLAlchemy(app)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pisces02@localhost:5432/flask'
app.config['SECRET_KEY'] = '\xf2B^q\xb1,Jw\xaf\x83\x9a\x10:\xa8Rc=yK\xb6\xca!\x80'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bootstrap = Bootstrap(app)
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
admin = Admin(app)

class User(UserMixin, db.Model):
    id = db.columns.UUID(primary_key=True)
    first_name = db.columns.Text()
    last_name = db.columns.Text()
    username = db.columns.Text(primary_key=True)
    email = db.columns.Text(primary_key=True)
    password = db.columns.Text(primary_key=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

sync_table(User)

def redirect_dest(fallback):
    dest = request.args.get('next')
    try:
        dest_url = url_for(dest)
    except:
        return redirect(fallback)
    return redirect(dest_url)


@login_manager.unauthorized_handler
def handle_needs_login():
    flash("You have to be logged in to access this page.")
    return redirect(url_for('login', next=request.endpoint))


@login_manager.user_loader
def load_user(user_id): 
    get_id_user = User.filter(id = user_id)
    return get_id_user.get()


class LoginForm(FlaskForm):
    username = StringField('username', validators=[
        InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[
        InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(
        message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[
        InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[
        InputRequired(), Length(min=8, max=80)])


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    first_name = StringField('First Name',
                             validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = (User.filter(username=username.data).allow_filtering()).first()
            if user:
                raise ValidationError(
                    'That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = (User.filter(email=email.data).allow_filtering()).first()
            if user:
                raise ValidationError(
                    'That email is taken. Please choose a different one.')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = (User.filter(username=form.username.data).allow_filtering()).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect_dest(fallback=url_for('index'))

        flash('Invalid Username or password!!!!', "danger")

    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(
            form.password.data, method='sha256')

        new_user = User(username=form.username.data,
                        email=form.email.data, password=hashed_password)
        user = (new_user.filter(email=form.email.data).allow_filtering()).first()
        user1 = (new_user.filter(username=form.username.data).allow_filtering()).first()
        
        if user or user1:
            flash(
                'User name or Email address already exists. Please Login !!!', "danger")
            return redirect(url_for('login'))

        session.execute("INSERT INTO flaskspace.user (id,username,email,password) VALUES (%s,%s,%s,%s)", (uuid.uuid1(),new_user.username,new_user.email,new_user.password ))
        flash("Account has been successfully created!!! You can now login!!! ", "success")
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('dashboard'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
    return render_template('dashboard.html', title='Account', form=form)


@app.route('/')
def index():
    app.logger.debug("debug")
    app.logger.info("info")
    app.logger.warning("warning")
    app.logger.error("error")
    app.logger.critical("critical")
    return render_template('index.html')

@app.route('/speech_text',methods=["GET", "POST"])
@login_required
def speech_text():
    transcript = ""
    if request.method == "POST":
        print("FORM DATA RECEIVED")

        if "file" not in request.files:
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)

        if file:
            recognizer = sr.Recognizer()
            audioFile = sr.AudioFile(file)
            with audioFile as source:
                data = recognizer.record(source)
            transcript = recognizer.recognize_google(data, key=None)

    return render_template('speech_text.html', transcript=transcript)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/camera', methods=['POST', 'GET'])
@login_required
def camera():
    """Video streaming home page."""
    return render_template('camera.html')


def gen():
    camera = cv2.VideoCapture(0)

    # region of interest (ROI) coordinates
    top, right, bottom, left = 100, 350, 400, 650

    # initialize num of frames
    count_same_frame = 0
    num_frames = 0
    aWeight = 0.5
    text = ""
    word = ""
    while(camera.isOpened()):
        (grabbed, fram) = camera.read()

        # resize the frame
        fram = imutils.resize(fram, width=700)

        # flip the frame so that it is not the mirror view
        fram = cv2.flip(fram, 1)

        # clone the frame
        clone = fram.copy()

        # get the height and width of the frame
        (height, width) = fram.shape[:2]

        # get the ROI
        roi = fram[top:bottom, right:left]

        # convert the roi to grayscale and blur it
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)
        contours = ''
        thresh = gray
    # to get the background, keep looking till a threshold is reached
    # so that our running average model gets calibrated
        if num_frames < 20:
            run_avg(gray, aWeight)
        else:
            # segment the hand region
            hand = segment(gray)
            # check whether hand region is segmented
            if hand is not None:
                # if yes, unpack the thresholded image and
                # segmented region
                (thresholded, segmented, tour) = hand
                contours = tour
                thresh = thresholded
                # draw the segmented region and display the frame
                cv2.drawContours(
                    clone, [segmented + (right, top)], -1, (0, 0, 255))
        img = thresh
        img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
        img = np.array(img, dtype=np.float32)
        img = np.reshape(img, (1, IMG_SIZE, IMG_SIZE, 1))
        global sess
        global graph
        with graph.as_default():
            set_session(sess)
            model_out = model.predict([img])[0]
        pred_class = list(model_out).index(max(model_out))
        old_text = text
        if len(contours) > 0:
            contour = max(contours, key=cv2.contourArea)
            if cv2.contourArea(contour) > 10000:
                if((max(model_out))*100) > 80:
                    text = str(out_label[pred_class])
                    xf = str(np.argmax(model_out))+" " + text
                if old_text == text:
                    count_same_frame += 1
                else:
                    count_same_frame = 0

                if count_same_frame > 50:
                    if text == 'space':
                        word += ' '
                    elif text == 'del':
                        word = word[:-1]
                    else:
                        word = word + text
                    count_same_frame = 0
            elif cv2.contourArea(contour) < 1000:
                if word != '':
                    say(word)
                text = ""
                word = ""
        else:
            if word != '':
                say(word)
            text = ""
            word = ""
        blackboard = np.zeros((525, 600, 3), np.uint8)
        cv2.putText(blackboard,
                    "Predicted text- " +
                    text, (30, 100), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 255, 0))
        cv2.putText(blackboard, word, (30, 280),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
        # draw the segmented hand
        cv2.rectangle(clone, (left, top),
                      (right, bottom), (0, 255, 0), 2)
        num_frames += 1
        hor = np.hstack((clone, blackboard))

        frame = cv2.imencode('.jpg', hor)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# admin.add_view(ModelView(User,db.sync_db()))

if __name__ == '__main__':
    app.run(debug=True)
