import sqlite3

from flask import Flask
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import pytz

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)


# login_manager = LoginManager()
# login_manager.init_app(app)


class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(30), nullable=False, unique=True)
    user_password = db.Column(db.String(12), nullable=False)
    user_display_name = db.Column(db.String(30), nullable=False, unique=False)
    user_address = db.Column(db.String(12), nullable=False)
    user_type = db.Column(db.String(12), nullable=False)


# 資産区分,所属名,資産名称,用途,所在地,取得年月日,取得価額等,耐用年数,減価償却累計額,数量,財産区分
class Asset(db.Model):
    asset_id = db.Column(db.Integer, primary_key=True)
    asset_classification = db.Column(db.String(20), nullable=False)
    asset_affiliation = db.Column(db.String(20), nullable=False)
    asset_name = db.Column(db.String(100), nullable=False)
    asset_use = db.Column(db.String(20), nullable=False)
    asset_location = db.Column(db.String(100), nullable=False)
    asset_acquisition_date = db.Column(db.String(100), nullable=False)
    asset_acquisition_price = db.Column(db.String(100), nullable=False)
    asset_useful_life = db.Column(db.String(100), nullable=False)
    asset_accumulated_depreciation = db.Column(db.String(100), nullable=False)
    asset_quantity = db.Column(db.String(100), nullable=False)
    asset_property_classification = db.Column(db.String(100), nullable=False)


# appという名前でFlaskのインスタンスを作成
app = Flask(__name__, static_url_path='/images')
app.config['DEBUG'] = True


@app.route('/', methods=['GET', 'POST'])
def index():  # put application's code here
    return render_template('index.html', title="index")


@app.route('/login', methods=['GET', 'POST'])
def login():  # put application's code here
    return render_template('login.html', title="login")


@app.route('/signup', methods=['GET', 'POST'])
def signup():  # put application's code here
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        user_password = request.form.get('user_password')
        display_name = request.form.get('display_name')
        user_address = request.form.get('user_address')
        user_type = request.form.get('user_type')
        sign_user = User(user_name=user_name,
                         user_password=generate_password_hash(user_password, method='sha256'),
                         user_display_name=display_name,
                         user_address=user_address,
                         user_type=user_type)
        db.session.add(sign_user)
        db.session.commit()
        return redirect('/login')
    else:
        return render_template('signup.html', title="signup")


@app.route('/list/<string:user_name>', methods=['GET', 'POST'])
def user(user_name):  # put application's code here
    return render_template('list.html', title="view_list", html_user_name=user_name)


@app.route('/user_list', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        users = User.query.all()
        return render_template('user_list.html', posts=users)

if __name__ == '__main__':
    app.run()
