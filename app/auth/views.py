<< << << < Updated
upstream
from flask import render_template
from . import  auth

@auth.rout('/login')
def log():
    return render_template('auth/login.html')

== == == =
from flask import render_template, redirect, flash, request, url_for
from . import auth
from flask_login import login_required, login_user, logout_user
from .forms import LoginForm
from ..models import User


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and User.verify_password(form.password.data):
            login_user(user, form.remenber_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password!')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed!'

>> >> >> > Stashed
changes
