from flask import render_template, flash, url_for, redirect, request
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User

@bp.route('/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        print("Validated", flush=True)
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))

    return render_template(
        'register.html',
        title='Register',
        form=form
        )

@bp.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Wrong credentials.')
            return redirect(url_for('auth.login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next') # get the user's destination from the URL

        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)

        return redirect(url_for('main.index'))
        flash('Logging in user {}'.format(form.username.data))

    return render_template(
        'login.html',
        title = 'Login',
        form = form
        )

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
