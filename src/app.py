from flask import Flask, render_template
from .config import app_config
from .models import db, bcrypt
from .views.videoView import video_api as video_blueprint
from .views.userView import user_api as user_blueprint

def create_app(env_name):
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://postgres:megaevia27@localhost:5432/skripsong"

    bcrypt.init_app(app)
    db.init_app(app)

    app.config.from_object(app_config[env_name])
    app.register_blueprint(video_blueprint, url_prefix='/api/v1/videos')
    app.register_blueprint(user_blueprint, url_prefix='/api/v1/users')

#    @app.route('/', methods=['GET'])
#    def index():
#        return 'selamat datang'

    @app.route('/', methods=['GET'])
    def index_page_landing():
        return render_template('login.html')

    return app