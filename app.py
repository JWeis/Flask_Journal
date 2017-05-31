from flask import (Flask, g, render_template,flash,
                   redirect, url_for, abort)
from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, login_user, logout_user,
                         login_required, current_user)

import forms
import models

DEBUG = True

app = Flask(__name__)
app.secret_key = '164613165fdsafeu02380hf'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the database before each request"""
    g.db = models.DATABASE
    g.db.get_conn()
    g.user = current_user


@app.after_request
def after_request(response):
    """Close the db after each request"""
    g.db.close()
    return response


@app.route('/')
def index():
    entries = models.Entry.select().limit(100)
    return render_template('entries.html', entries=entries)


if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            username='jamesweis',
            email='jweis@revampagency.com',
            password='password',
            is_admin=True
        )
    except ValueError:
        pass
    app.run(debug=DEBUG)