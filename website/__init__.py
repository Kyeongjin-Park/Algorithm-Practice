from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# Apply for Flask-Migrate
from flask_migrate import Migrate
from sqlalchemy import MetaData

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata) # () -> (metadata=metadata) 추가
DB_NAME = "database.db"

def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = 'semicircle_secret_key'
  app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
  db.init_app(app)

  # Import Blueprint
  from .views import views
  from .auth import auth
  from .mypage_views import mypage_views # mypage 추가

  # Apply Blueprint
  app.register_blueprint(views, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/')
  app.register_blueprint(mypage_views, url_prefix='/') # mypage 추가


  # DB에 사용할 모델 불러오기
  from .models import User, Note # from .models. import *
  with app.app_context():
    db.create_all()

  # flask-login 적용
  login_manager = LoginManager()
  login_manager.login_view = 'auth.sign_in'
  login_manager.init_app(app)

  @login_manager.user_loader
  def load_user(id):
    return User.query.get(id) # primary_key

  # Flask-Migrate 적용
  migrate = Migrate(app, db, render_as_batch=True)

  return app


# 데이터 베이스 생성 함수
def create_database(app):
  # db파일이 확인안될 때만 생성
  if not path.exists('website/' + DB_NAME):
    db.create_all(app=app)
    print('>>> Create DB')