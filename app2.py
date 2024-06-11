from flask import Flask, g, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_required, LoginManager, login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import input_required, length, ValidationError
from flask_bcrypt import Bcrypt

from config import Config
class User:
    def user():
        pass    
app = Flask(__name__)
app.config.from_object(Config)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html',)

@app.route('/student')
@login_required
def student():
    return render_template('student.html')


@app.route('/admin')
@login_required
def admin():
    return render_template('Admin.html')

if __name__ == '__main__':
    app.run(debug=True)
