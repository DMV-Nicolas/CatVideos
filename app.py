from flask import Flask, render_template, request, redirect, url_for, session, g, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")
db=SQLAlchemy(app)

class Base(db.Model):
	__abstract__ = True
	id = db.Column(db.Integer, primary_key=True)
class User_Profile(Base):
	__tablename__ = "User_Profile"
	username = db.Column(db.String(100), nullable=False)
	password = db.Column(db.String(100), nullable=False)
	videos = db.relationship("User_Videos", backref="user", lazy="dynamic")

class User_Videos(Base):
	__tablename__ = "User_Videos"
	name = db.Column(db.String(100), nullable=False)
	url = db.Column(db.String(500), nullable=False)
	admitted = db.Column(db.String(10), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey("User_Profile.id"), nullable=False)

@app.before_request
def before_request():
    if "username" in session:
        g.user=session["username"]
    else:
        g.user=None

@app.route("/")
def index():
	videoUrlImg = []
	userNumVideos = 0
	videos = User_Videos.query.filter_by(admitted="True").all()
	for video in videos:
		videoUrl = video.url.replace("watch?v=","embed/",1)
		videoKey = videoUrl.replace("https://www.youtube.com/embed/","$",1)
		videoUrlImg.append(f"{videoKey.replace('$','https://img.youtube.com/vi/',1)}/mqdefault.jpg")
	if g.user:
		user = User_Profile.query.filter_by(username=g.user).first()
		if user.videos.all():
			userVideos = User_Videos.query.filter_by(user_id=user.id).all()
			userNumVideos = 0
			for x in userVideos:
				userNumVideos+=1
	return (render_template("index.html",videos=videos, videoUrlImg=videoUrlImg, userNumVideos=userNumVideos))

@app.route("/signup",methods=["GET","POST"])
def signup():
	if request.method=="POST":
		password=generate_password_hash(request.form["password"], method="sha256")
		newUser = User_Profile(username = request.form["username"], password=password)
		db.session.add(newUser)
		db.session.commit()
		return redirect(url_for("login"))
	return (render_template("signup.html"))

@app.route("/login",methods=["GET","POST"])
def login():
	if request.method=="POST":
		user=User_Profile.query.filter_by(username=request.form["username"]).first()
		if user and check_password_hash(user.password, request.form["password"]):
			session["username"]=user.username
			return redirect(url_for("index"))
	return (render_template("login.html"))

@app.route("/logout")
def logout():
	session.pop("username",None)
	return redirect(url_for("index"))

@app.route("/watch/<videoId>")
def watchVideo(videoId):
	video = User_Videos.query.filter_by(id=videoId).first()
	videoName = video.name
	videoUrl = video.url.replace("watch?v=","embed/",1)
	return (render_template("watchVideo.html", videoName=videoName,videoUrl = videoUrl))

@app.route("/addVideo",methods=["GET","POST"])
def addVideo():
	if g.user:
		if request.method=="POST":
			user = User_Profile.query.filter_by(username=g.user).first()
			newVideo = User_Videos(name=request.form["videoName"],url=request.form["videoUrl"],admitted="True",user_id=user.id)
			db.session.add(newVideo)
			db.session.commit()
			flash("Video añadido exitosamente","success")
			return redirect(url_for("index"))
		return render_template("addVideo.html")
	return redirect(url_for("login"))

@app.route("/delete/<videoName>")
def deleteVideo(videoName):
	user = User_Profile.query.filter_by(username=g.user).first()
	video = user.videos.filter_by(name=videoName).first()
	if video:
		db.session.delete(video)
		db.session.commit()
		flash("Video eliminado exitosamente","success")
		return redirect(url_for("index"))
	flash("Video no encontrado","error")
	return redirect(url_for("index"))

if __name__=="__main__":
	db.create_all()
	app.run(debug=True)
