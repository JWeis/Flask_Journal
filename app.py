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
@app.route('/entries')
@login_required
def index():
    template = 'index.html'
    entries = models.Entry.select().limit(100)
    return render_template(template, entries=entries)


@app.route('/login', methods=['GET', 'POST'])
def login():
    template = 'login.html'
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Your email or password doesn't match", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You are now logged in!", "succes")
                return redirect(url_for('index'))
            else:
                flash("Your email or password doesn't match!")
    return render_template(template, form=form)


@app.route('/logout', methods=['GET','POST'])
def logout():
    logout_user()
    flash("Your have been logged out!", "success")
    return redirect(url_for('index'))


@app.route('/new-entry', methods=['GET', 'POST'])
@login_required
def new_entry():
    template = 'new.html'
    form = forms.EntryForm()
    if form.validate_on_submit():
        models.Entry.create(
            user=g.user._get_current_object(),
            title = form.title.data.strip(),
            content = form.content.data.strip(),
            date = form.date.data,
            resources_text1=form.resources_text1.data.strip(),
            resources_text2 = form.resources_text2.data.strip(),
            resources_text3 = form.resources_text3.data.strip(),
            resource_link1 = form.resource_link1.data.strip(),
            resource_link2 = form.resource_link2.data.strip(),
            resource_link3 = form.resource_link3.data.strip(),
            time_spent = form.time_spent.data,
            tags = form.tags.data.strip()
        )
        flash("You entry has been created!", "success")
        return redirect(url_for('index'))
    return render_template(template, form=form)


@app.route('/delete/<int:id>')
def delete_entry(id):
    entries = models.Entry.delete().where(models.Entry.id == id)
    entries.execute()
    flash("Entry Deleted")
    return redirect(url_for('index'))


@app.route('/entries/<int:id>')
def view_entry(id):
    template = 'detail.html'
    entries = models.Entry.select().where(models.Entry.id == id)
    if entries.count() == 0:
        abort(404)
    return render_template(template, entries=entries)


@app.route('/entries/edit/<int:id>', methods=['GET','POST'])
@login_required
def edit_entry(id):
    template = 'edit.html'
    form = forms.EntryForm()
    entries = models.Entry.select().where(models.Entry.id == id)
    if form.validate_on_submit():
        update = models.Entry.update(
                title=form.title.data.strip(),
                content=form.content.data.strip(),
                date=form.date.data,
                resources_text1=form.resources_text1.data.strip(),
                resources_text2=form.resources_text2.data.strip(),
                resources_text3=form.resources_text3.data.strip(),
                resource_link1=form.resource_link1.data.strip(),
                resource_link2=form.resource_link2.data.strip(),
                resource_link3=form.resource_link3.data.strip(),
                time_spent=form.time_spent.data,
                tags=form.tags.data.strip()
            ).where(models.Entry.id == id)
        update.execute()
        flash("Your entry has been updated", "success")
        return redirect(url_for('view_entry', id=id))
    return render_template(template, form=form, entries=entries)

@app.route('/entries/<tag>')
def view_by_tag(tag=None):
    template = 'index.html'
    entries = models.Entry.select().where(models.Entry.tags**tag)
    return render_template(template, entries=entries)

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