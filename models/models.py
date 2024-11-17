from . import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	password = db.Column(db.String(120), nullable=False)
	is_admin = db.Column(db.Boolean, default=False)
	messages = db.relationship('Message', backref='user', lazy=True)
class Area(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	is_private = db.Column(db.Boolean, default=False)
	threads = db.relationship('Thread', backref='area', lazy=True)

class Thread(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(200), nullable=False)
	area_id = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=False)
	messages = db.relationship('Message', backref='thread', lazy =True)

class Message(db.Model):
	__tablenmame__ = 'message'

	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.Text, nullable=True)
	thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	created_at = db.Column(db.DateTime, default=db.func.now())

