import os
from flask import Flask
from dotenv import load_dotenv
from routes import discussion, user, auth, fp, profile
from flask_wtf.csrf import CSRFProtect




csrf = CSRFProtect()
load_dotenv()





def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    app.register_blueprint(profile.bp)
    app.register_blueprint(fp.bp)
    app.register_blueprint(discussion.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(auth.bp)
    
    csrf.init_app(app)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
